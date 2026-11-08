"""JANE 047: common-cause witness verification; self-contained Python model."""
from dataclasses import dataclass
from collections import Counter
import hashlib,hmac,json,random

TRUE="JANE047:27->27.5->1:-1,0,+1"
FALSE="JANE047:FORGED-CHECKPOINT"
KEYS={n:("local-key-"+n).encode() for n in "ABC"}

@dataclass(frozen=True)
class Witness:
    name:str
    dependencies:frozenset
    key_root:str

@dataclass(frozen=True)
class Attestation:
    witness:str
    epoch:int
    digest:str
    signature:str

def sign(name,epoch,digest,keys=KEYS):
    msg=json.dumps([name,epoch,digest],separators=(",",":")).encode()
    return Attestation(name,epoch,digest,hmac.new(keys[name],msg,hashlib.sha256).hexdigest())

def authentic(a,keys=KEYS):
    if a.witness not in keys or a.epoch<0:return False
    return hmac.compare_digest(a.signature,sign(a.witness,a.epoch,a.digest,keys).signature)

def registry(kind):
    if kind=="independent": d=[["A"],["B"],["C"]]
    elif kind=="paired": d=[["shared-source"],["shared-source"],["independent-C"]]
    elif kind=="cloned": d=[["shared-source"]]*3
    elif kind=="shared-key": d=[["signer-root"]]*3
    elif kind=="overlap": d=[["upstream-X","provider-Y"],["upstream-X"],["provider-Y"]]
    else:raise ValueError(kind)
    return {name:Witness(name,frozenset(d[i]),"shared" if kind=="shared-key" else name)
            for i,name in enumerate("ABC")}

def dependencies(w):return w.dependencies|frozenset({"key:"+w.key_root})

def verify(records,reg,epoch,source_aware=True,pinned=None,min_epoch=0,keys=KEYS):
    if epoch<min_epoch:return {"status":"ROLLBACK","digest":None}
    seen={};blocked=set()
    for a in records:
        if a.witness not in reg or a.epoch!=epoch or not authentic(a,keys):continue
        if a.witness in blocked:continue
        if a.witness in seen and seen[a.witness].digest!=a.digest:
            del seen[a.witness];blocked.add(a.witness)
        else:seen[a.witness]=a
    groups={}
    for a in seen.values():groups.setdefault(a.digest,[]).append(a.witness)
    qualifying=[]
    for digest,names in groups.items():
        if any((not source_aware or dependencies(reg[x]).isdisjoint(dependencies(reg[y])))
               for i,x in enumerate(names) for y in names[i+1:]):
            qualifying.append(digest)
    if pinned is not None and any(d!=pinned for d in qualifying):
        return {"status":"ANCHOR_CONFLICT","digest":None}
    if len(qualifying)>1:return {"status":"CONFLICT","digest":None}
    if len(qualifying)==1:return {"status":"VERIFIED","digest":qualifying[0]}
    return {"status":"CONFLICT_NO_QUORUM" if len(groups)>1 else "INSUFFICIENT","digest":None}

def trial(kind,rng,aware,common=.08,individual=.08):
    reg=registry(kind);domains={}
    for w in reg.values():
        for d in w.dependencies:
            if d not in domains:domains[d]=rng.random()<common
    keys={n:(b"shared-signing-secret" if kind=="shared-key" else KEYS[n]) for n in "ABC"}
    items=[sign(n,47,FALSE if any(domains[d] for d in w.dependencies) or rng.random()<individual else TRUE,keys)
           for n,w in reg.items()]
    result=verify(items,reg,47,aware,keys=keys)
    if result["status"]!="VERIFIED":return "ABSTAIN"
    return "FALSE_ACCEPT" if result["digest"]==FALSE else "TRUE_ACCEPT"

def sweep(trials=1000,seed=4700):
    rows=[]
    for kind in ("independent","paired","cloned","shared-key","overlap"):
        for aware in (False,True):
            rng=random.Random(seed)
            c=Counter(trial(kind,rng,aware) for _ in range(trials))
            rows.append(dict(config=kind,verifier="source-aware" if aware else "naive",trials=trials,
                             **{k:c[k] for k in ("TRUE_ACCEPT","FALSE_ACCEPT","ABSTAIN")}))
    return rows

if __name__=="__main__":print(json.dumps(sweep(),indent=2))
