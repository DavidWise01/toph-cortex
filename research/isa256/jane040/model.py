"""JANE040: peer-led recovery, durable local decision copies, no coordinator during recovery."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,os,random
N=27
TERNARY=(-1,0,1)
WAVE="111222333444555555444333222111"
A=(-3.,.5,2.);B=(5.,-.25,-7.)
F1=tuple(map(float,WAVE[:27]));F2=tuple(map(float,WAVE[3:]))
TX="27/27.5/1:wave-exchange:0"
def energy(a,b):return sum(x*x for x in (*F1,*F2,*a,*b))
class Log:
 def __init__(self,p):
  self.p=Path(p);self.p.parent.mkdir(parents=True,exist_ok=True);self.p.touch(exist_ok=True)
 def write(self,kind,**kw):
  with self.p.open('a') as f:
   f.write(json.dumps({"tx":TX,"kind":kind,**kw},sort_keys=True)+"\n");f.flush();os.fsync(f.fileno())
 def rows(self):return [json.loads(s) for s in self.p.read_text().splitlines() if s]
class Peer:
 def __init__(self,name,path,own,other):self.name=name;self.log=Log(path);self.own=own;self.other=other
 def decision(self):
  ds={x["decision"] for x in self.log.rows() if x["kind"]=="DECISION_COPY"}
  return "CONFLICT" if len(ds)>1 else next(iter(ds),None)
 def state(self):
  kinds=[x["kind"] for x in self.log.rows()]
  for state,kind in (("COMMITTED","APPLIED"),("ABORTED","ABORTED"),("PREPARED","PREPARED")):
   if kind in kinds:return state
  return "NEW"
 def prepare(self):
  if self.state()=="NEW":self.log.write("PREPARED")
  return self.state()=="PREPARED"
 def copy(self,d):
  if d not in ("COMMIT","ABORT"):raise ValueError(d)
  old=self.decision()
  if old=="CONFLICT" or (old and old!=d):return False
  if (d=="COMMIT" and self.state()=="ABORTED") or (d=="ABORT" and self.state()=="COMMITTED"):return False
  if not old:self.log.write("DECISION_COPY",decision=d)
  return True
 def apply(self):
  d=self.decision();s=self.state()
  if d=="COMMIT" and s=="PREPARED":self.log.write("APPLIED");return True
  if d=="ABORT" and s in ("NEW","PREPARED"):self.log.write("ABORTED");return True
  return (d=="COMMIT" and s=="COMMITTED") or (d=="ABORT" and s=="ABORTED")
 def register(self):return (self.other[2],self.own[1],self.other[0]) if self.state()=="COMMITTED" else self.own
class Pair:
 def __init__(self,path):
  p=Path(path);self.left=Peer("-",p/"minus.jsonl",A,B);self.right=Peer("+",p/"plus.jsonl",B,A);self.coord=Log(p/"coord.jsonl")
 def restart(self):return Pair(self.left.log.p.parent)
 def prepare(self):return self.left.prepare(),self.right.prepare()
 def decide(self,d):
  ds={x["decision"] for x in self.coord.rows() if x["kind"]=="DECISION"}
  if ds and ds!={d}:raise ValueError("conflicting decision")
  if not ds:self.coord.write("DECISION",decision=d)
 def seed(self,side,d):
  if not any(x["kind"]=="DECISION" and x["decision"]==d for x in self.coord.rows()):raise ValueError("no durable coordinator decision")
  return getattr(self,side).copy(d)
 def recover(self,connected=True,retries=1):
  if connected:
   a,b=self.left,self.right;da,db=a.decision(),b.decision()
   if not ("CONFLICT" in (da,db) or (da and db and da!=db)):
    d=da or db
    if d:
     for _ in range(retries):a.copy(d);b.copy(d);a.apply();b.apply()
  return self.status()
 def status(self):
  a,b=self.left,self.right;da,db=a.decision(),b.decision()
  if "CONFLICT" in (da,db) or (da and db and da!=db):return "CONFLICT"
  if a.state()==b.state()=="COMMITTED":return "CLOSED"
  if a.state()==b.state()=="ABORTED":return "ABORTED"
  return "IN_DOUBT"
 def energy(self):return energy(self.left.register(),self.right.register())
def scenario(kind="recover",loss=.2,seed=3):
 rng=random.Random(seed)
 with TemporaryDirectory() as d:
  p=Pair(d);p.prepare()
  if kind in ("recover","no_copy","partition","partial"):
   p.decide("COMMIT")
   if kind!="no_copy":p.seed("left","COMMIT")
   if kind=="partial":p.left.apply()
  elif kind=="abort":p.decide("ABORT");p.seed("right","ABORT")
  else:raise ValueError(kind)
  before=p.energy();p=p.restart()
  for _ in range(40):
   if kind=="partition":break
   if rng.random()>=loss:p.recover(retries=2)
   if p.status() in ("CLOSED","ABORTED","CONFLICT"):break
  return {"status":p.status(),"before":before,"after":p.energy()}
if __name__=="__main__":
 print(json.dumps([{"loss":loss,"closed":sum(scenario(loss=loss,seed=i+101)["status"]=="CLOSED" for i in range(200))} for loss in (0,.1,.2,.4,1)],indent=2))
