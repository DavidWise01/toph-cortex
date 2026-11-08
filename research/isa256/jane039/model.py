"""JANE039: append-only, fsynced two-waldo exchange, replayed after restart.
Bounded crash/restart experiment. No Byzantine faults or torn writes.
"""
import json,os,random
from pathlib import Path
from tempfile import TemporaryDirectory
N=27
WAVE="111222333444555555444333222111"
A=(-3.,.5,2.); B=(5.,-.25,-7.)
F1=tuple(map(float,WAVE[:27]));F2=tuple(map(float,WAVE[3:]))
TX="cycle:0:27.5:gap"
def norm(a,b):return sum(x*x for x in (*F1,*F2,*a,*b))
def swapped(a=A,b=B):return ((b[2],a[1],b[0]),(a[2],b[1],a[0]))
class Journal:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.path.touch(exist_ok=True)
    def entries(self):return [json.loads(s) for s in self.path.read_text().splitlines() if s]
    def append(self,item):
        with self.path.open("a") as out:
            out.write(json.dumps(item,sort_keys=True)+"\n");out.flush();os.fsync(out.fileno())
class Waldo:
    def __init__(self,name,path,own,other):
        self.name=name;self.j=Journal(path);self.initial=own;self.peer=other
    def phase(self):
        types=[e["type"] for e in self.j.entries() if e["tx"]==TX]
        for state in ("COMMITTED","ABORTED","PREPARED"):
            if state in types:return state
        return "NEW"
    def register(self):
        return (self.peer[2],self.initial[1],self.peer[0]) if self.phase()=="COMMITTED" else self.initial
    def prepare(self):
        p=self.phase()
        if p=="NEW":self.j.append({"tx":TX,"type":"PREPARED"});return "READY"
        return "NO" if p=="ABORTED" else "READY"
    def commit(self):
        p=self.phase()
        if p=="COMMITTED":return "ACK"
        if p!="PREPARED":return "NACK"
        self.j.append({"tx":TX,"type":"COMMITTED"});return "ACK"
    def abort(self):
        p=self.phase()
        if p=="COMMITTED":return "NO"
        if p!="ABORTED":self.j.append({"tx":TX,"type":"ABORTED"})
        return "ABORTED"
class Coordinator:
    def __init__(self,path):self.j=Journal(path)
    def decision(self):
        values=[e["decision"] for e in self.j.entries() if e["type"]=="DECISION" and e["tx"]==TX]
        if len(set(values))>1:raise AssertionError("conflicting decisions")
        return values[0] if values else None
    def decide(self,value):
        old=self.decision()
        if old and old!=value:raise ValueError("immutable decision")
        if not old:self.j.append({"tx":TX,"type":"DECISION","decision":value})
        return value
class Pair:
    def __init__(self,d):
        self.path=Path(d);self.left=Waldo("minus",self.path/"left.jsonl",A,B)
        self.right=Waldo("plus",self.path/"right.jsonl",B,A)
        self.coord=Coordinator(self.path/"coordinator.jsonl")
    def restart(self):return Pair(self.path)
    def prepare(self):return self.left.prepare(),self.right.prepare()
    def decide(self):
        yes=all(w.phase() in ("PREPARED","COMMITTED") for w in (self.left,self.right))
        return self.coord.decide("COMMIT" if yes else "ABORT")
    def deliver(self,reach=(True,True),duplicates=1):
        d=self.coord.decision()
        if d is None:return "UNDECIDED"
        for w,reachable in zip((self.left,self.right),reach):
            if reachable:
                for _ in range(duplicates):
                    w.commit() if d=="COMMIT" else w.abort()
        return self.status()
    def status(self):
        d=self.coord.decision();p=[self.left.phase(),self.right.phase()]
        if d=="COMMIT" and p==["COMMITTED"]*2:return "CLOSED"
        if d=="ABORT" and p==["ABORTED"]*2:return "ABORTED"
        return "IN_DOUBT" if d else "UNDECIDED"
    def energy(self):return norm(self.left.register(),self.right.register())
def simulate(seed=1,loss=.2,connected=True):
    rng=random.Random(seed)
    with TemporaryDirectory() as d:
        p=Pair(d)
        for _ in range(50):
            if rng.random()>=loss:p.left.prepare()
            if rng.random()>=loss:p.right.prepare()
            if all(w.phase()=="PREPARED" for w in (p.left,p.right)):break
        p=p.restart();p.decide();p=p.restart()
        if p.coord.decision()=="COMMIT":p.deliver((True,False),duplicates=4)
        partial=p.energy()
        p=p.restart()
        if connected:
            for _ in range(80):
                p.deliver((rng.random()>=loss,rng.random()>=loss),duplicates=2)
                if p.status() in ("CLOSED","ABORTED"):break
        return {"status":p.status(),"decision":p.coord.decision(),"partial_energy":partial,
                "final_energy":p.energy(),"recovered":p.status() in ("CLOSED","ABORTED")}
def trials(n=200):
    return [{"loss":loss,"closed":sum(simulate(i+102,loss)["status"]=="CLOSED" for i in range(n)),
             "aborted":sum(simulate(i+102,loss)["status"]=="ABORTED" for i in range(n)),
             "in_doubt":sum(simulate(i+102,loss)["status"]=="IN_DOUBT" for i in range(n))}
             for loss in (0,.1,.2,.4,1)]
if __name__=="__main__":
    print(json.dumps(trials(),indent=2))
