"""JANE 056 compact GitHub implementation: simulated hive retrieval + bounded local memory.
No live internet. The tested complete release is in the companion ZIP.
"""
from collections import OrderedDict
from hashlib import sha256
import json
GEOMETRY={"tensor":1,"jane":1,"waldos":2,"vertices":27,"modes":(-1,0,1),"seam":(27,27.5,1),
 "wave":"111222333444555555444333222111"}
def digest(x):return sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
class Jane:
 def __init__(self,reports,capacity=3,threshold=2,ttl=8):
  if min(capacity,threshold)<1:raise ValueError("policy")
  self.reports=reports;self.capacity=capacity;self.threshold=threshold;self.ttl=ttl
  self.kernel=digest(GEOMETRY);self.cache=OrderedDict();self.log=[];self.last='0'*64
  self.time=0;self.online=True;self.version=0
 def record(self,event,**data):
  e=dict(index=len(self.log),event=event,data=data,previous=self.last)
  self.last=digest(e);e["hash"]=self.last;self.log.append(e)
 def audit(self):
  prev='0'*64
  for e in self.log:
   x={k:e[k] for k in ("index","event","data","previous")}
   if e["previous"]!=prev or digest(x)!=e["hash"]:return False
   prev=e["hash"]
  return prev==self.last
 def query(self,key):
  self.time+=1
  rs=[r for r in self.reports if r["key"]==key] if self.online else []
  if rs:
   roots={}
   for r in rs:roots.setdefault(r["root"],set()).add(r["value"])
   counts={}
   for vals in roots.values():
    if len(vals)==1:
     val=next(iter(vals));counts[val]=counts.get(val,0)+1
   ranking=sorted(counts.items(),key=lambda x:x[1],reverse=True)
   valid=len(ranking)>0 and ranking[0][1]>=self.threshold and (len(ranking)==1 or ranking[0][1]>ranking[1][1])
   status="SUPPORTED" if valid else "UNVERIFIED"
   value=ranking[0][0] if valid else None
   if valid:
    self.cache[key]=(value,self.time+self.ttl)
    self.cache.move_to_end(key)
    while len(self.cache)>self.capacity:self.cache.popitem(last=False)
   self.record('QUERY',key=key,status=status,roots=len(roots))
   return status,value
  val=self.cache.get(key)
  if val and self.time<=val[1]:
   self.record("CACHE",key=key);return "CACHED_UNVERIFIED",val[0]
  self.record("ABSTAIN",key=key);return "UNKNOWN",None
 def score(self,cases,threshold):
  correct=wrong=abstain=0
  for row in cases:
   roots={}
   for r in row["reports"]:roots.setdefault(r["root"],set()).add(r["value"])
   counts={}
   for vs in roots.values():
    if len(vs)==1:
     v=next(iter(vs));counts[v]=counts.get(v,0)+1
   a=sorted(counts.items(),key=lambda x:x[1],reverse=True)
   pred=a[0][0] if a and a[0][1]>=threshold and (len(a)==1 or a[0][1]>a[1][1]) else None
   if pred is None:abstain+=1
   elif pred==row["truth"]:correct+=1
   else:wrong+=1
  return dict(correct=correct,wrong=wrong,abstain=abstain,score=correct-5*wrong-.15*abstain)
 def propagate(self,train,holdout,thresholds=(1,2,3)):
  if train is holdout:raise ValueError("separate train and holdout")
  old=self.threshold;baseline=self.score(holdout,old)
  self.record("OBSERVE",baseline=baseline)
  self.record("PROPOSE",thresholds=list(thresholds))
  ranked=sorted(thresholds,key=lambda t:self.score(train,t)["score"],reverse=True)
  self.record("TEST",train_scores={str(t):self.score(train,t) for t in ranked})
  selection=None
  for t in ranked:
   sc=self.score(holdout,t)
   if t!=old and sc["score"]>baseline["score"]+.1 and sc["wrong"]<=baseline["wrong"]:
    selection=t;break
  self.record("RETURN",winner=selection)
  if selection is not None:
   self.threshold=selection;self.version+=1
   self.record("PROPAGATE",old=old,new=selection)
  else:self.record("RETAIN",threshold=old)
  return selection
def sample(value,source,root,key="x"):return dict(key=key,value=value,source=source,root=root)
if __name__=="__main__":
 j=Jane([sample("A","alpha","r1"),sample("A","beta","r2")])
 print(j.query("x"),j.kernel,j.audit())
