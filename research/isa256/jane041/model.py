"""JANE041 — coordinator-free peer voting; compact runnable edition."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,os,random
N=27
WAVE="111222333444555555444333222111"
MODES=(-1,0,1)
A=(-3.,.5,2.);B=(5.,-.25,-7.)
F1=tuple(map(float,WAVE[:27]));F2=tuple(map(float,WAVE[3:]))
def energy(a,b):return sum(v*v for v in (*F1,*F2,*a,*b))
class Peer:
 def __init__(self,name,path,own,other):
  self.name=name;self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.path.touch(exist_ok=True)
  self.own=own;self.other=other
 def events(self):return [json.loads(x) for x in self.path.read_text().splitlines() if x]
 def add(self,event,**k):
  with self.path.open('a') as f:
   f.write(json.dumps(dict(event=event,**k),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 def own_vote(self):
  vals=[e['vote'] for e in self.events() if e['event']=='VOTE']
  return vals[0] if vals else None
 def peer_vote(self):
  vals=[e['vote'] for e in self.events() if e['event']=='PEER']
  return vals[0] if vals else None
 def cast(self,vote):
  if vote not in ('YES','NO'):raise ValueError(vote)
  old=self.own_vote()
  if old is not None and old!=vote:raise ValueError('immutable vote')
  if old is None:self.add('VOTE',vote=vote)
 def receive(self,vote):
  if vote not in ('YES','NO'):raise ValueError(vote)
  old=self.peer_vote()
  if old is not None and old!=vote:return False
  if old is None:self.add('PEER',vote=vote)
  return True
 def decision(self):
  a,b=self.own_vote(),self.peer_vote()
  if a=='NO' or b=='NO':return 'ABORT'
  if a=='YES' and b=='YES':return 'COMMIT'
  return None
 def applied(self):return any(x['event']=='APPLY' for x in self.events())
 def apply(self):
  d=self.decision()
  if d is None:return False
  if not self.applied():self.add('APPLY',decision=d)
  return True
 def register(self):
  return (self.other[2],self.own[1],self.other[0]) if self.applied() and self.decision()=='COMMIT' else self.own
class Pair:
 def __init__(self,path):
  path=Path(path);self.minus=Peer('-',path/'minus.jsonl',A,B);self.plus=Peer('+',path/'plus.jsonl',B,A)
 def restart(self):return Pair(self.minus.path.parent)
 def vote(self,a='YES',b='YES'):self.minus.cast(a);self.plus.cast(b)
 def communicate(self,to='both'):
  if to in ('both','minus') and self.plus.own_vote():self.minus.receive(self.plus.own_vote())
  if to in ('both','plus') and self.minus.own_vote():self.plus.receive(self.minus.own_vote())
 def apply(self,to='both'):
  if to in ('both','minus'):self.minus.apply()
  if to in ('both','plus'):self.plus.apply()
 def state(self):
  if self.minus.applied() and self.plus.applied():
   return 'CLOSED' if self.minus.decision()==self.plus.decision()=='COMMIT' else 'ABORTED'
  return 'IN_DOUBT'
 def energy(self):return energy(self.minus.register(),self.plus.register())
def simulate(seed=1,loss=.2,case='YES_YES',attempts=40):
 if not 0<=loss<=1:raise ValueError(loss)
 if case not in ('YES_YES','YES_NO','PARTITION','HALF'):raise ValueError(case)
 rng=random.Random(seed)
 with TemporaryDirectory() as path:
  p=Pair(path);p.vote('YES','NO' if case=='YES_NO' else 'YES')
  if case=='HALF':p.communicate('minus');p.apply('minus')
  partial=p.energy();p=p.restart()
  for _ in range(attempts):
   if case=='PARTITION':break
   if rng.random()>=loss:p.communicate('minus')
   if rng.random()>=loss:p.communicate('plus')
   if rng.random()>=loss:p.apply('minus')
   if rng.random()>=loss:p.apply('plus')
   p=p.restart()
   if p.state()!='IN_DOUBT':break
  return dict(state=p.state(),partial_energy=partial,final_energy=p.energy(),
              minus=p.minus.decision(),plus=p.plus.decision())
if __name__=='__main__':
 for loss in (0,.1,.2,.4,1):
  runs=[simulate(i+2000,loss) for i in range(200)]
  print(loss,sum(x['state']=='CLOSED' for x in runs),sum(x['state']=='IN_DOUBT' for x in runs))
