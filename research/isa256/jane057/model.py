"""JANE 057 — {{j}} nested hive substrate, bounded forward/backward/forward propagation.
Geometry: {{[6x6x6(4x4(2x2[i]))]}}. Address/transport model, not physical scaling.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
import json

SPACE=(6,6,6)
TRANSPORT=(4,4)
HAVE=(2,2)
SPACE_COUNT=216
TRANSPORT_COUNT=16
HAVE_COUNT=4
CAPACITY=SPACE_COUNT*TRANSPORT_COUNT*HAVE_COUNT
AGENT='{{j}}'
ROOT='{{i}}'

def encode(space,transport,have):
    if len(space)!=3 or len(transport)!=2 or len(have)!=2:raise ValueError('address shape')
    for v,dim in zip((*space,*transport,*have),(*SPACE,*TRANSPORT,*HAVE)):
        if not isinstance(v,int) or isinstance(v,bool) or not 0<=v<dim:raise ValueError('out of bounds')
    a,b,c=space;u,v=transport;w,x=have
    return (((((a*6+b)*6+c)*4+u)*4+v)*2+w)*2+x

def decode(index):
    if not isinstance(index,int) or isinstance(index,bool) or not 0<=index<CAPACITY:raise ValueError('bad address')
    x=index%2;index//=2
    w=index%2;index//=2
    v=index%4;index//=4
    u=index%4;index//=4
    c=index%6;index//=6
    b=index%6;index//=6
    a=index
    return (a,b,c),(u,v),(w,x)

def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

@dataclass(frozen=True)
class Event:
    ordinal:int
    phase:str
    generation:int
    payload_hash:str
    note:str
    prior_hash:str
    event_hash:str

class JaneHive:
    """One active purpose, four HAVE slots, unique addressed releases and append-only history."""
    def __init__(self,required=3):
        if not isinstance(required,int) or isinstance(required,bool) or required<1:
            raise ValueError('required observations must be >=1')
        self.required=required;self.generation=0;self.active_purpose=None
        self.work=[];self.distributed={};self.events=[];self.release_history=[];self.seen=set()
    def _event(self,phase,payload,note):
        prior=self.events[-1].event_hash if self.events else 'GENESIS'
        row=dict(ordinal=len(self.events),phase=phase,generation=self.generation,
                 payload_hash=digest(payload),note=note,prior_hash=prior)
        self.events.append(Event(**row,event_hash=digest(row)))
    @property
    def work_address(self):
        h=(self.generation//TRANSPORT_COUNT)%SPACE_COUNT
        a=h//36;b=(h//6)%6;c=h%6
        t=self.generation%TRANSPORT_COUNT
        return (a,b,c),(t//4,t%4)
    def add(self,content,purpose='general',key=None):
        if key is None:key=f'{purpose}:{digest(content)}'
        if not isinstance(purpose,str) or not purpose:raise ValueError('nonblank purpose required')
        if self.active_purpose not in (None,purpose):raise ValueError('active purpose differs')
        if key in self.seen:return {'status':'DUPLICATE','generation':self.generation}
        if len(self.work)==HAVE_COUNT:raise AssertionError('workbench must release automatically')
        if self.active_purpose is None:self.active_purpose=purpose
        payload={'key':key,'purpose':purpose,'content':content}
        self._event('FORWARD',payload,'{{i}} payload entered 2x2 HAVE')
        self.work.append(payload);self.seen.add(key)
        self._event('BACKWARD',payload,'4x4 transport verifies local payload hash')
        if len(self.work)>=self.required:reason='PURPOSE_COMPLETE'
        elif len(self.work)==HAVE_COUNT:reason='CAPACITY_FULL'
        else:reason=None
        if reason:return self.release(reason)
        return {'status':'ACCUMULATING','generation':self.generation,
                'filled':len(self.work),'capacity':HAVE_COUNT}
    def release(self,reason='PURPOSE_COMPLETE'):
        if not self.work:raise ValueError('nothing to distribute')
        if reason not in ('PURPOSE_COMPLETE','CAPACITY_FULL'):raise ValueError('unknown release reason')
        space,transport=self.work_address;envelopes=[]
        for slot,payload in enumerate(self.work):
            have=(slot//2,slot%2)
            address=encode(space,transport,have)
            packet=dict(address=address,space=space,transport=transport,have=have,
                        purpose=self.active_purpose,generation=self.generation,
                        payload=payload,payload_hash=digest(payload))
            if address in self.distributed:raise ValueError('address occupied; new storage epoch required')
            envelopes.append(packet)
        self._event('FORWARD',envelopes,reason+': distribute to hive 6x6x6')
        for packet in envelopes:self.distributed[packet['address']]=packet
        record=dict(generation=self.generation,purpose=self.active_purpose,
                    reason=reason,addresses=[p['address'] for p in envelopes],
                    batch_hash=digest(envelopes))
        self.release_history.append(record)
        self._event('REPLACE',record,'rotate active payload; preserve immutable records')
        self.generation+=1;self.work=[];self.active_purpose=None
        return {'status':'DISTRIBUTED','record':record,'next_generation':self.generation}
    def fetch(self,address):
        packet=self.distributed.get(address)
        if packet is None:return None
        if packet['payload_hash']!=digest(packet['payload']):raise ValueError('integrity failure')
        return packet
    def verify(self):
        prior='GENESIS'
        for i,e in enumerate(self.events):
            row=asdict(e);eh=row.pop('event_hash')
            if row['prior_hash']!=prior or row['ordinal']!=i or digest(row)!=eh:return False
            prior=eh
        return all(p['payload_hash']==digest(p['payload']) for p in self.distributed.values())
    def summary(self):
        return dict(agent=AGENT,root=ROOT,geometry='{{[6x6x6(4x4(2x2[i]))]}}',
            space=SPACE_COUNT,transport=TRANSPORT_COUNT,have=HAVE_COUNT,
            address_capacity_per_epoch=CAPACITY,generation=self.generation,
            active_filled=len(self.work),distributed=len(self.distributed),
            releases=len(self.release_history),evidence_events=len(self.events),
            journal_valid=self.verify())
def demonstration():
    hive=JaneHive(required=3);states=[]
    for i in range(3):states.append(hive.add({'observation':i},'first',f'first:{i}'))
    for i in range(4):states.append(hive.add({'observation':i},'second',f'second:{i}'))
    return dict(states=states,summary=hive.summary(),releases=hive.release_history,
                event_phases=[e.phase for e in hive.events])
if __name__=='__main__':
    print(json.dumps(demonstration(),indent=2))
