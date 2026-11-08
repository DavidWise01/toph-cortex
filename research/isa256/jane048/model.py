"""JANE048: checkpoint provenance, source dependency and rollback boundaries."""
import hashlib,hmac,json
from collections import Counter
KEYS={"alpha":b"independent-anchor-alpha","beta":b"independent-anchor-beta","gamma":b"independent-anchor-gamma"}
ROOT_KEY=b"local-registry-editor"
TRUSTED_DOMAINS={"alpha":"root-a","beta":"root-b","gamma":"root-c"}
def canonical(o):return json.dumps(o,sort_keys=True,separators=(",",":")).encode()
def digest(o):return hashlib.sha256(canonical(o)).hexdigest()
def sign(k,o):return hmac.new(k,canonical(o),hashlib.sha256).hexdigest()
def registry(seq=8,deps=None):
 if deps is None:deps={"w1":["s1"],"w2":["s2"],"w3":["s3"]}
 body={"seq":seq,"dependencies":deps}
 return {**body,"signature":sign(ROOT_KEY,body)}
def verify_registry_signature(r):
 body={"seq":r.get("seq"),"dependencies":r.get("dependencies")}
 return hmac.compare_digest(sign(ROOT_KEY,body),r.get("signature",""))
def anchor(name,r,domain=None,forged=False):
 if name not in KEYS:raise ValueError(name)
 body={"anchor":name,"domain":domain or TRUSTED_DOMAINS[name],"seq":r["seq"],
       "root":digest({"seq":r["seq"],"dependencies":r["dependencies"]})}
 return {**body,"signature":sign(b"fake-key" if forged else KEYS[name],body)}
def verify_anchor(a):
 n=a.get("anchor")
 if n not in KEYS or a.get("domain")!=TRUSTED_DOMAINS[n]:return False
 body={k:a.get(k) for k in ("anchor","domain","seq","root")}
 return hmac.compare_digest(sign(KEYS[n],body),a.get("signature",""))
def independent_quorum(anchors,root,seq,minimum=2):
 seen={}
 for a in anchors:
  if verify_anchor(a) and a["root"]==root and a["seq"]==seq:seen[a["domain"]]=a["anchor"]
 return len(seen)>=minimum,len(seen)
def verify(r,anchors,minimum_seq=0,known_dependencies=None):
 if not verify_registry_signature(r):return {"status":"TAMPERED","quorum":0}
 if r["seq"]<minimum_seq:return {"status":"ROLLBACK","quorum":0}
 root=digest({"seq":r["seq"],"dependencies":r["dependencies"]})
 ok,n=independent_quorum(anchors,root,r["seq"])
 if not ok:return {"status":"INSUFFICIENT","quorum":n}
 if known_dependencies is not None and r["dependencies"]!=known_dependencies:
  return {"status":"CONTRADICTED","quorum":n}
 return {"status":"ANCHORED","quorum":n}
def approval(r,anchors,claims,minimum_seq=0,known_dependencies=None):
 v=verify(r,anchors,minimum_seq,known_dependencies)
 if v["status"]!="ANCHORED":return {**v,"approval":False}
 groups={}
 for witness,claim in claims.items():
  deps=frozenset(r["dependencies"].get(witness,[]))
  for source in deps:groups.setdefault(claim,set()).add(source)
 return {**v,"approval":max(map(len,groups.values()),default=0)>=2}
def scenarios():
 r=registry();a=[anchor(k,r) for k in KEYS]
 stale=registry(seq=7)
 rewritten=registry(deps={"w1":["single"],"w2":["single"],"w3":["single"]})
 liar=registry(seq=9)
 truth={"w1":["shared"],"w2":["shared"],"w3":["shared"]}
 return {"independent_valid":verify(r,a,8),"one_missing":verify(r,a[:2],8),
  "single_anchor":verify(r,a[:1],8),
  "rollback_pinned":verify(stale,[anchor(k,stale) for k in KEYS],8),
  "rollback_unpinned":verify(stale,[anchor(k,stale) for k in KEYS],0),
  "rewritten_old_anchors":verify(rewritten,a,8),
  "forged_anchor":verify(r,[anchor("alpha",r),anchor("beta",r,forged=True)],8),
  "shared_domain_claim":verify(r,[anchor("alpha",r),anchor("beta",r,domain="root-a")],8),
  "two_keys_lying":verify(liar,[anchor("alpha",liar),anchor("beta",liar)],8),
  "two_keys_contradicted":verify(liar,[anchor("alpha",liar),anchor("beta",liar)],8,known_dependencies=truth)}
def monte_carlo(trials=1000,seed=481):
 import random
 rng=random.Random(seed);rows=[]
 for mode in ("clean","edit","rollback","one_anchor","two_colluding_signers"):
  counts=Counter()
  for _ in range(trials):
   seq=8+rng.randrange(3);r=registry(seq);aa=[anchor(k,r) for k in KEYS]
   if mode=="edit":r={**r,"dependencies":{"w1":["cloned"],"w2":["cloned"],"w3":["cloned"]}}
   elif mode=="rollback":r=registry(seq-1);aa=[anchor(k,r) for k in KEYS]
   elif mode=="one_anchor":aa=aa[:1]
   elif mode=="two_colluding_signers":
    r=registry(seq,{"w1":["fake-a"],"w2":["fake-b"],"w3":["fake-c"]})
    aa=[anchor(k,r) for k in ("alpha","beta")]
   counts[verify(r,aa,seq)["status"]]+=1
  rows.append({"case":mode,**counts})
 return rows
if __name__=="__main__":print(json.dumps({"scenarios":scenarios(),"trials":monte_carlo()},indent=2))
