"""JANE042 — [0] escrow: executable compact model of classical signed-payload transfers.
Python standard library. Complete 46-test release is available as jane_042.zip.
"""
import json,os,hashlib,tempfile
from pathlib import Path
WAVE="111222333444555555444333222111"
N=27
SOURCES=("a-","a+","b-","b+")
DEST={"a-":"b+","a+":"b-","b-":"a+","b+":"a-"}
START={"a":[-3.,.5,2.],"b":[5.,-.25,-7.]}
FIELDS=[list(map(float,WAVE[:27])),list(map(float,WAVE[3:]))]
BASE=741.3125
def slot(state,key):
    return state["regs"][key[0]][0 if key[1]=="-" else 2]
def put(state,key,value):
    state["regs"][key[0]][0 if key[1]=="-" else 2]=value
def norm(state):
    return sum(v*v for field in FIELDS for v in field)+sum(x*x for c in state["regs"].values() for x in c)+sum(v*v for v in state["gap"].values())
def digest(row):return hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
class Exchange:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.path.touch(exist_ok=True)
        self.state=dict(regs=json.loads(json.dumps(START)),gap={},staged=[],delivered=[],phase="NEW",seq=0)
        for line in self.path.read_text().splitlines():
            entry=json.loads(line);body={"seq":entry["seq"],"state":entry["state"]}
            if entry["hash"]!=digest(body) or entry["seq"]!=self.state["seq"]+1:raise ValueError("broken journal")
            self.state=entry["state"]
        self.check()
    def check(self):
        s=self.state
        if set(s["gap"])!=set(s["staged"])-set(s["delivered"]):raise ValueError("gap mismatch")
        if abs(norm(s)-BASE)>1e-9:raise ValueError("not conserved")
    def persist(self,state):
        state["seq"]=self.state["seq"]+1
        body={"seq":state["seq"],"state":state}
        with self.path.open("a") as f:
            f.write(json.dumps({**body,"hash":digest(body)},sort_keys=True)+"\n");f.flush();os.fsync(f.fileno())
        self.state=state;self.check()
    def prepare(self):
        if self.state["phase"]!="NEW":return False
        s=json.loads(json.dumps(self.state));s["phase"]="PREPARED";self.persist(s);return True
    def stage(self,key):
        if key not in SOURCES:raise ValueError(key)
        if self.state["phase"] not in ("PREPARED","STAGING") or key in self.state["staged"]:return False
        s=json.loads(json.dumps(self.state));s["gap"][key]=slot(s,key);put(s,key,0.)
        s["staged"].append(key);s["phase"]="STAGING";self.persist(s);return True
    def deliver(self,key):
        if key not in SOURCES:raise ValueError(key)
        if len(self.state["staged"])!=4 or key in self.state["delivered"]:return False
        s=json.loads(json.dumps(self.state))
        dest=DEST[key]
        if slot(s,dest)!=0.:raise ValueError("occupied destination")
        put(s,dest,s["gap"].pop(key));s["delivered"].append(key)
        s["phase"]="CLOSED" if len(s["delivered"])==4 else "DELIVERING"
        self.persist(s);return True
    def recover(self):
        if self.state["phase"]=="NEW":return "NEW"
        for k in SOURCES:self.stage(k)
        for k in SOURCES:self.deliver(k)
        return self.state["phase"]
    def stats(self):
        return {"phase":self.state["phase"],"regs":self.state["regs"],"gap":self.state["gap"],
                "register_norm":norm({**self.state,"gap":{}}),
                "gap_norm":sum(x*x for x in self.state["gap"].values()),"combined":norm(self.state)}
def trial():
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"escrow.jsonl";x=Exchange(path);trace=[x.stats()]
        x.prepare();trace.append(x.stats())
        for k in SOURCES:
            x.stage(k);trace.append(x.stats());x=Exchange(path)
        for k in SOURCES:
            x.deliver(k);trace.append(x.stats());x=Exchange(path)
        return trace
if __name__=="__main__":print(json.dumps(trial(),indent=2))
