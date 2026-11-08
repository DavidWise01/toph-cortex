"""JANE038 — two-party acknowledged ternary exchange, standard-library simulation.

In-process durable-id ledger; bounded retries; crash atomicity NOT implemented.
"""
from dataclasses import dataclass, field
import random
N=27
WAVE="111222333444555555444333222111"
A0=(-3., .5, 2.)
B0=(5., -.25, -7.)
FIELD_A=tuple(map(float,WAVE[:27]))
FIELD_B=tuple(map(float,WAVE[3:]))
def energy(a,b):
    return sum(x*x for x in (*FIELD_A,*FIELD_B,*a,*b))
@dataclass
class Waldo:
    identity:str
    register:list
    prepared:set=field(default_factory=set)
    applied:set=field(default_factory=set)
    aborted:set=field(default_factory=set)
    def prepare(self,tid):
        if tid in self.aborted:return False
        self.prepared.add(tid);return True
    def commit(self,tid,peer_original):
        if tid in self.applied:return "DUPLICATE"
        if tid not in self.prepared or tid in self.aborted:return "NOT_PREPARED"
        old=list(self.register)
        self.register=[peer_original[2],old[1],peer_original[0]]
        self.applied.add(tid)
        return "APPLIED"
    def abort(self,tid):
        if tid in self.applied:return False
        self.aborted.add(tid)
        self.prepared.discard(tid)
        return True
@dataclass
class FaultLink:
    rng:random.Random
    loss:float=0.
    duplicate:float=0.
    corrupt:float=0.
    tx:int=0
    delivered:int=0
    dropped:int=0
    duplicates:int=0
    corruptions:int=0
    def send(self,kind,tid,data=None):
        self.tx+=1
        if self.rng.random()<self.loss:
            self.dropped+=1
            return []
        copies=2 if self.rng.random()<self.duplicate else 1
        self.duplicates+=copies-1
        out=[]
        for _ in range(copies):
            if self.rng.random()<self.corrupt:
                self.corruptions+=1
                continue
            out.append((kind,tid,data))
            self.delivered+=1
        return out
def naive(seed=1,loss=.1,duplicate=.1,corruption=.0,retries=5):
    f=FaultLink(random.Random(seed),loss,duplicate,corruption)
    a,b=list(A0),list(B0)
    applied=0
    for _ in range(retries+1):
        msgs=f.send("SWAP",1)
        for _ in msgs:
            a,b=[b[2],a[1],b[0]],[a[2],b[1],a[0]]
            applied+=1
        if msgs and f.send("ACK",1):break
    return {"applied":applied,"state":(tuple(a),tuple(b)),
            "matches_one_swap":(tuple(a),tuple(b))==((B0[2],A0[1],B0[0]),(A0[2],B0[1],A0[0])),
            "energy":energy(a,b)}
def pack(a,b,link,decision,logs,original):
    target=((original[1][2],original[0][1],original[1][0]),
            (original[0][2],original[1][1],original[0][0]))
    actual=(tuple(a.register),tuple(b.register))
    status="CLOSED" if decision=="COMMIT" and actual==target else ("ABORTED" if decision=="UNDECIDED" else "IN_DOUBT")
    return {"decision":decision,"state":status,"correct":status in ("CLOSED","ABORTED"),
            "exact_once":actual==target,
            "applied_a":len(a.applied),"applied_b":len(b.applied),
            "attempts":len({v[0] for v in logs}),
            "registers":actual,"energy":energy(a.register,b.register),
            "energy_start":energy(*original),
            "messages":link.tx,"delivered":link.delivered,"dropped":link.dropped,
            "duplicates":link.duplicates,"corrupted":link.corruptions,"logs":logs}
def acknowledged(seed=1,loss=.1,duplicate=.1,corruption=.0,retries=8,
                 permanent_partition=False,crash_after_one_commit=False):
    link=FaultLink(random.Random(seed),loss,duplicate,corruption)
    a=Waldo("minus",list(A0));b=Waldo("plus",list(B0))
    original=(tuple(a.register),tuple(b.register))
    tid="gap-13.5:cycle-0"
    logs=[];decision="UNDECIDED"
    for attempt in range(retries+1):
        for node in (a,b):
            requests=link.send("PREPARE",tid)
            if requests and node.prepare(tid):
                if link.send("READY",tid): logs.append((attempt,"READY",node.identity))
        if all(any(t=="READY" and who==n.identity for _,t,who in logs) for n in (a,b)):
            decision="COMMIT"
            break
    if decision!="COMMIT":
        for node in (a,b):node.abort(tid)
        return pack(a,b,link,decision,logs,original)
    for attempt in range(retries+1):
        for i,node in enumerate((a,b)):
            if i==1 and (permanent_partition or crash_after_one_commit):continue
            for _ in link.send("COMMIT",tid):
                result=node.commit(tid,original[1-i])
                logs.append((attempt,result,node.identity))
                if link.send("ACK",tid):logs.append((attempt,"ACK",node.identity))
        if all(any(t=="ACK" and who==n.identity for _,t,who in logs) for n in (a,b)):break
    return pack(a,b,link,decision,logs,original)
def sweep(trials=200):
    rows=[]
    for loss,duplicate,corrupt in ((0,0,0),(.1,.1,0),(.2,.25,.01),(.4,.25,.03)):
        nn=[naive(seed=i+101,loss=loss,duplicate=duplicate,corruption=corrupt) for i in range(trials)]
        aa=[acknowledged(seed=i+101,loss=loss,duplicate=duplicate,corruption=corrupt) for i in range(trials)]
        rows.append({"loss":loss,"duplicate":duplicate,"corrupt":corrupt,"trials":trials,
            "naive_correct":sum(r["matches_one_swap"] for r in nn),
            "protocol_closed":sum(r["state"]=="CLOSED" for r in aa),
            "protocol_aborted":sum(r["state"]=="ABORTED" for r in aa),
            "protocol_in_doubt":sum(r["state"]=="IN_DOUBT" for r in aa),
            "protocol_globally_conserved":sum(abs(r["energy"]-r["energy_start"])<1e-10 for r in aa)})
    return rows
if __name__=="__main__":
    import json
    print(json.dumps(sweep(),indent=2))
