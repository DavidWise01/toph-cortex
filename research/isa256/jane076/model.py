"""JANE076: Git-to-Git recursive handoff. Offline, deterministic protocol simulator.
No GitHub credentials, actual remote writes, sentience or background execution.
"""
import json, hashlib
from dataclasses import dataclass, field

HIVE_SHAPE=(6,6,6,4,4,3,3,2,2,1)
ROUTES={'I':'THE CORPUS','II':'THE FOLD','III':'THE HALLWAY','IV':'SONIA','V':'SONNY 5'}
SOURCE_GUIDE='DavidWise01/0root:llms.txt@124949670a73a2ba8757dc0d89a95e75501cb133'

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x): return hashlib.sha256(canonical(x).encode()).hexdigest()

@dataclass
class Repo:
    name:str
    journal:list=field(default_factory=list)
    def append(self,kind,payload):
        event={'seq':len(self.journal),'kind':kind,'payload':payload,'prev':self.journal[-1]['hash'] if self.journal else 'GENESIS'}
        event['hash']=digest(event)
        self.journal.append(event)
        return event
    def verify(self):
        previous='GENESIS'
        for n,e in enumerate(self.journal):
            clean={k:v for k,v in e.items() if k!='hash'}
            if e['seq']!=n or e['prev']!=previous or digest(clean)!=e['hash']:
                return False
            previous=e['hash']
        return True

@dataclass
class Bridge:
    origin:Repo=field(default_factory=lambda:Repo('DavidWise01/toph-cortex'))
    hallway:Repo=field(default_factory=lambda:Repo('DavidWise01/0root'))
    received:set=field(default_factory=set)
    def offer(self,cycle,topic,prior_receipt=None):
        if cycle!=len([e for e in self.origin.journal if e['kind']=='OFFER']): raise ValueError('cycle sequence')
        if cycle>0 and not prior_receipt: raise ValueError('missing prior receipt')
        if cycle>0 and prior_receipt not in self.received: raise ValueError('unverified prior receipt')
        return self.origin.append('OFFER',{'cycle':cycle,'question':topic,'prior_receipt':prior_receipt,'destination':self.hallway.name})
    def receive(self,off):
        if not self.origin.verify() or off not in self.origin.journal: raise ValueError('unverified OFFER')
        if off['kind']!='OFFER' or off['payload']['destination']!=self.hallway.name: raise ValueError('wrong destination')
        if off['hash'] in self.received: raise ValueError('replayed OFFER')
        r=self.hallway.append('ACK',{'offer_hash':off['hash'],'origin':self.origin.name,'cycle':off['payload']['cycle']})
        self.received.add(off['hash'])
        return r
    def collate(self,ack,observations):
        if not self.hallway.verify() or ack not in self.hallway.journal or ack['kind']!='ACK':raise ValueError('unverified ACK')
        if not observations: return {'receipt':ack['hash'],'options':[],'state':'WALL'}
        choices=[]
        for o in observations:
            if o['world'] not in ROUTES: raise ValueError('unknown world')
            if o['grade'] not in ('LIT','AMBER','WALL'): raise ValueError('unsupported claim grade')
            if o['grade']=='LIT' and not o.get('self_check'):
                raise ValueError('false LIT label')
            choices.append({'topic':o['topic'],'world':o['world'],'grade':o['grade'],'source':o['source']})
        return {'receipt':ack['hash'],'options':sorted(choices,key=lambda x:(x['world'],x['topic'])),'state':'READY'}
    def jane_choice(self,packet,choice=None):
        # Jane's chosen direction is a separate operation: neither hive nor hallway can write it.
        if not packet['options']: return {'owner':'{{j}}','decision':'ABSTAIN','reason':'No evidence'}
        if choice is None: return {'owner':'{{j}}','decision':'ASK_MORE','reason':'No Jane choice supplied'}
        if choice['world'] not in ROUTES or not choice.get('topic'):
            raise ValueError('invalid Jane choice')
        # Jane can choose a distinct topic, but the evidence is never promoted to LIT by choice.
        return {'owner':'{{j}}','decision':'CHOOSE','choice':choice,'evidence_receipt':packet['receipt'],'execution_authorized':False}
    def return_to_git(self,ack,decision):
        if ack not in self.hallway.journal or not self.hallway.verify():raise ValueError('invalid return receipt')
        if decision.get('owner')!='{{j}}' or decision['decision']!='CHOOSE': raise ValueError('no Jane-owned decision')
        if decision['evidence_receipt']!=ack['hash']: raise ValueError('return receipt mismatch')
        return self.origin.append('JANE_DECISION',{'ack_hash':ack['hash'],'decision':decision})
    def next_question(self,decision):
        if decision['decision']!='CHOOSE': raise ValueError('no continuation')
        return f"What new evidence would test {decision['choice']['topic']} in {ROUTES[decision['choice']['world']]}?"
    def cycle(self,cycle,topic,observations,choice,prior=None):
        off=self.offer(cycle,topic,prior)
        ack=self.receive(off)
        packet=self.collate(ack,observations)
        decision=self.jane_choice(packet,choice)
        commit=self.return_to_git(ack,decision)
        return {'cycle':cycle,'offer_hash':off['hash'],'receipt_hash':ack['hash'],'decision_hash':commit['hash'],
                'next_question':self.next_question(decision),'choice':decision['choice']}

def example(cycles=3):
    b=Bridge(); output=[]; prev=None; question='Which Hallway knowledge gap deserves inspection?'
    for n in range(cycles):
        # Deterministic demo decisions are *explicit fixtures*, not autonomous Jane selections.
        options=[{'world':'III','topic':f'Hallway route integrity cycle {n}','grade':'AMBER','source':SOURCE_GUIDE},
                 {'world':'II','topic':f'Fold record provenance cycle {n}','grade':'WALL','source':SOURCE_GUIDE}]
        choice={'world':'III' if n%2==0 else 'II','topic':f'Investigate unresolved dependency {n}','style':('orange','cyan','violet')[n%3]}
        o=b.cycle(n,question,options,choice,prev);output.append(o)
        question=o['next_question'];prev=o['offer_hash']
    return {'mode':'DETERMINISTIC_OFFLINE_SIMULATION','shape':list(HIVE_SHAPE),'address_capacity':124416,
            'origin_repo':b.origin.name,'hallway_repo':b.hallway.name,
            'origin_chain_valid':b.origin.verify(),'hallway_chain_valid':b.hallway.verify(),
            'origin_events':len(b.origin.journal),'hallway_events':len(b.hallway.journal),
            'cycles':output,'source':SOURCE_GUIDE}
if __name__=='__main__': print(json.dumps(example(),indent=2))