"""JANE 049: Trust-root closure; deterministic classical evidence model."""
import hashlib,hmac,json
from dataclasses import dataclass
PRIMITIVE='{brace[box(cell())]}'
POSITIONS=27
TERNARY=(-1,0,1)
WAVE="111222333444555555444333222111"
SEAM='27 -> 27.5 -> 1'
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
@dataclass(frozen=True)
class Root:
    name:str
    domain:str
    key:str
@dataclass(frozen=True)
class Record:
    root:str
    domain:str
    epoch:int
    prev:str
    claim:str
    signature:str
    def payload(self):return dict(root=self.root,domain=self.domain,epoch=self.epoch,prev=self.prev,claim=self.claim)
    def id(self):return digest(dict(**self.payload(),signature=self.signature))
def issue(root,epoch,prev,claim):
    payload=dict(root=root.name,domain=root.domain,epoch=epoch,prev=prev,claim=claim)
    signature=hmac.new(root.key.encode(),digest(payload).encode(),hashlib.sha256).hexdigest()
    return Record(**payload,signature=signature)
def authentic(record,root):
    if record.root!=root.name or record.domain!=root.domain:return False
    expected=hmac.new(root.key.encode(),digest(record.payload()).encode(),hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,record.signature)
@dataclass(frozen=True)
class TrustPin:
    root:str
    trusted_epoch:int
    trusted_id:str
def verify_chain(root,records,pin=None):
    if not records:return 'MISSING_HISTORY'
    prev='GENESIS'
    for epoch,record in enumerate(records,start=1):
        if record.epoch!=epoch or record.prev!=prev:return 'BROKEN_CHAIN'
        if not authentic(record,root):return 'INVALID_AUTHORITY'
        prev=record.id()
    if pin is not None:
        if pin.root!=root.name:return 'PIN_MISMATCH'
        if len(records)<pin.trusted_epoch:return 'ROLLBACK'
        if records[pin.trusted_epoch-1].id()!=pin.trusted_id:return 'HISTORY_CONFLICT'
    return 'VERIFIED'
def source_aware_quorum(root_sets,reports,needed=2):
    supporters={}
    for witness,claim in reports.items():
        roots=root_sets.get(witness,())
        if roots:supporters.setdefault(claim,[]).append(set(roots))
    accepted=[]
    for claim,dependencies in supporters.items():
        best=0
        for mask in range(1<<len(dependencies)):
            chosen=[dependencies[i] for i in range(len(dependencies)) if mask&(1<<i)]
            if all(chosen[i].isdisjoint(chosen[j]) for i in range(len(chosen)) for j in range(i+1,len(chosen))):
                best=max(best,len(chosen))
        if best>=needed:accepted.append(claim)
    return accepted[0] if len(accepted)==1 else 'INSUFFICIENT' if not accepted else 'CONFLICT'
def anchors():
    return (Root('R-A','A-physical','anchor-key-a-049'),
            Root('R-B','B-physical','anchor-key-b-049'),
            Root('R-C','C-physical','anchor-key-c-049'))
def scenario(name):
    a,b,c=anchors()
    good=[issue(a,1,'GENESIS','wave=1')]
    good.append(issue(a,2,good[-1].id(),'wave=2'))
    pin=TrustPin(a.name,2,good[-1].id())
    if name=='clean':
        return dict(status=verify_chain(a,good,pin),fact='wave=2',note='Pinned root history verified.')
    if name=='tamper':
        x=good[:]
        x[-1]=Record(**dict(good[-1].payload(),signature='0'*64))
        return dict(status=verify_chain(a,x,pin),fact='wave=999',note='Signature is invalid.')
    if name=='rollback_pinned':
        return dict(status=verify_chain(a,good[:1],pin),fact='wave=1',note='Trusted epoch 2 pin exposes rollback to epoch 1.')
    if name=='rollback_unpinned':
        return dict(status=verify_chain(a,good[:1]),fact='wave=1',note='Without the pin epoch 1 appears valid.')
    if name in ('key_compromise_pinned','key_compromise_unpinned','pin_compromised'):
        stolen=Root(a.name,a.domain,a.key)
        forged=[issue(stolen,1,'GENESIS','wave=1')]
        forged.append(issue(stolen,2,forged[-1].id(),'wave=999'))
        if name=='key_compromise_pinned':
            result=verify_chain(a,forged,pin)
            note='Authentic forged chain conflicts with trusted digest pin.'
        elif name=='key_compromise_unpinned':
            result=verify_chain(a,forged)
            note='Compromised key signs a fully consistent false history.'
        else:
            forged_pin=TrustPin(a.name,2,forged[-1].id())
            result=verify_chain(a,forged,forged_pin)
            note='Key plus pin compromised: verifier cannot distinguish rewritten trust root.'
        return dict(status=result,fact='wave=999',note=note)
    if name=='shared_root':
        result=source_aware_quorum({'A':['shared'],'B':['shared'],'C':['shared']},
            {'A':'wave=999','B':'wave=999','C':'wave=999'})
        return dict(status=result,fact='wave=999',note='Three reports reduce to one root domain.')
    if name=='independent_roots':
        result=source_aware_quorum({'A':['ra'],'B':['rb'],'C':['rc']},
            {'A':'wave=2','B':'wave=2','C':'wave=999'})
        return dict(status=result,fact='wave=2',note='Two distinct roots corroborate the same report.')
    if name=='colluding_roots':
        result=source_aware_quorum({'A':['ra'],'B':['rb'],'C':['rc']},
            {'A':'wave=999','B':'wave=999','C':'wave=2'})
        return dict(status=result,fact='wave=999',note='Two independent but compromised roots agree on a false claim.')
    if name=='absent_root':
        result=source_aware_quorum({'A':[],'B':[],'C':[]},
            {'A':'wave=2','B':'wave=2','C':'wave=2'})
        return dict(status=result,fact='wave=2',note='No anchored source can support the claim.')
    if name=='broken_link':
        wrong=[good[0],issue(a,2,'UNKNOWN','wave=2')]
        return dict(status=verify_chain(a,wrong,pin),fact='wave=2',note='Broken previous-record link.')
    raise ValueError(name)
SCENARIOS=('clean','tamper','rollback_pinned','rollback_unpinned',
 'key_compromise_pinned','key_compromise_unpinned','shared_root',
 'independent_roots','colluding_roots','pin_compromised',
 'absent_root','broken_link')
def full_report():
    return dict(primitive=PRIMITIVE,positions=POSITIONS,ternary=TERNARY,
        counted_components=POSITIONS+len(TERNARY),wave=WAVE,seam=SEAM,
        scenarios={name:scenario(name) for name in SCENARIOS},
        assumptions=['Keys secret unless compromised','Pinned history trusted unless compromised',
        'Declared root domains independent unless shared','Claims labelled with synthetic truth for evaluation'])
if __name__=='__main__':
    print(json.dumps(full_report(),indent=2))
