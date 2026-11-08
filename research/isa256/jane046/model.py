"""JANE046 — authenticated witness-divergence checkpoint simulation.
Educational HMAC quorum with 27-position primitive and pinned genesis.
"""
from dataclasses import dataclass, replace
import hashlib,hmac,json
N=27
STATES=(-1,0,1)
WAVE="111222333444555555444333222111"
ROOT0=hashlib.sha256(b"Jane 045: pinned genesis").hexdigest()
KEYS={w:hashlib.sha256(("demo-private-key:"+w).encode()).digest() for w in "ABC"}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def advance(prev,epoch,payload):return digest(dict(prev=prev,epoch=epoch,payload=payload))
ROOT1=advance(ROOT0,1,"signed wave closure")
FORK1=advance(ROOT0,1,"different payload")
ROOT2=advance(ROOT1,2,"second transaction")
def mac(w,data):return hmac.new(KEYS[w],json.dumps(data,sort_keys=True,separators=(",",":")).encode(),hashlib.sha256).hexdigest()
@dataclass(frozen=True)
class Checkpoint:
 witness:str
 epoch:int
 prev:str
 root:str
 signature:str
 def payload(self):return dict(witness=self.witness,epoch=self.epoch,prev=self.prev,root=self.root)
def attest(w,epoch,prev,root):
 fields=dict(witness=w,epoch=epoch,prev=prev,root=root)
 return Checkpoint(**fields,signature=mac(w,fields))
def authenticated(cp):
 return cp.witness in KEYS and hmac.compare_digest(cp.signature,mac(cp.witness,cp.payload()))
class Verifier:
 def __init__(self,anchor_epoch=0,anchor_root=ROOT0,threshold=2):
  self.anchor_epoch=anchor_epoch;self.anchor_root=anchor_root;self.threshold=threshold
 def evaluate(self,records,known_links=None):
  known_links=known_links or {}
  accepted=[];rejected=[];equivocations=set();by_witness={}
  for cp in records:
   if not authenticated(cp):rejected.append((cp.witness,"INVALID_MAC"));continue
   if cp.epoch<=self.anchor_epoch:rejected.append((cp.witness,"STALE_OR_REPLAY"));continue
   if cp.witness in by_witness:
    prior=by_witness[cp.witness]
    if cp.epoch==prior.epoch and cp.root!=prior.root:equivocations.add(cp.witness)
    else:rejected.append((cp.witness,"DUPLICATE_OR_MULTI_EPOCH"))
    continue
   by_witness[cp.witness]=cp
  for cp in by_witness.values():
   if cp.witness in equivocations:rejected.append((cp.witness,"EQUIVOCATION"));continue
   if cp.epoch==self.anchor_epoch+1:anchored=cp.prev==self.anchor_root
   else:
    prev=cp.prev;anchored=False
    for e in range(cp.epoch-1,self.anchor_epoch,-1):
     match=[v for (ep,r),v in known_links.items() if ep==e and r==prev]
     if len(match)!=1:break
     prev=match[0]
    else:anchored=prev==self.anchor_root
   if not anchored:rejected.append((cp.witness,"UNANCHORED_OR_MISSING_CHAIN"));continue
   accepted.append(cp)
  groups={}
  for cp in accepted:groups.setdefault((cp.epoch,cp.root),[]).append(cp.witness)
  winning=[(k,w) for k,w in groups.items() if len(w)>=self.threshold]
  if len(winning)>1:status="CONFLICT";chosen=None
  elif winning:
   chosen=winning[0][0]
   status="VERIFIED" if len(accepted)==len(winning[0][1]) else "VERIFIED_WITH_DIVERGENCE"
  elif accepted and len(groups)>1:status="CONFLICT";chosen=None
  else:status="INSUFFICIENT";chosen=None
  return dict(status=status,selected=dict(epoch=chosen[0],root=chosen[1]) if chosen else None,
   valid=len(accepted),total=len(records),
   groups=[dict(epoch=e,root=r[:12],witnesses=sorted(w)) for (e,r),w in sorted(groups.items())],
   rejected=[dict(witness=w,reason=why) for w,why in rejected],
   equivocation=sorted(equivocations))
def case(name):
 v=Verifier();good=[attest(w,1,ROOT0,ROOT1) for w in KEYS]
 if name=="unanimous":records=good
 elif name=="two_agree":records=good[:2]
 elif name=="split":records=[good[0],attest("B",1,ROOT0,FORK1)]
 elif name=="majority_with_fork":records=[good[0],good[1],attest("C",1,ROOT0,FORK1)]
 elif name=="tampered_mac":records=[good[0],replace(good[1],root=FORK1)]
 elif name=="replayed_old":records=[good[0],attest("B",0,ROOT0,ROOT0)]
 elif name=="missing_chain":records=[attest("A",2,ROOT1,ROOT2),attest("B",2,ROOT1,ROOT2)]
 elif name=="known_chain":
  records=[attest("A",2,ROOT1,ROOT2),attest("B",2,ROOT1,ROOT2)]
  return v.evaluate(records,{(1,ROOT1):ROOT0})
 elif name=="equivocation":records=[good[0],attest("A",1,ROOT0,FORK1),good[1]]
 elif name=="two_corrupt":records=[attest("A",1,ROOT0,FORK1),attest("B",1,ROOT0,FORK1),good[2]]
 elif name=="missing_all":records=[]
 else:raise ValueError(name)
 return v.evaluate(records)
CASES=("unanimous","two_agree","split","majority_with_fork","tampered_mac","replayed_old","missing_chain","known_chain","equivocation","two_corrupt","missing_all")
if __name__=="__main__":
 print(json.dumps({k:case(k) for k in CASES},indent=2))
