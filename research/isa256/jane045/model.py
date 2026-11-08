"""JANE 045 — independently authenticated checkpoints for two append-only waldo logs.
Compact GitHub edition. Trust: anchor HMAC key + pinned witness ID lie outside waldo compromise.
For the exact original 36-test local edition, use the packaged release in conversation.
"""
import hashlib,hmac,json,os
from pathlib import Path
from tempfile import TemporaryDirectory

BASELINE=741.3125
GENESIS="0"*64
KEY=b"JANE045-DEMO-KEY-NOT-FOR-DEPLOYMENT"
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"))
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def mac(x,key=KEY):return hmac.new(key,canonical(x).encode(),hashlib.sha256).hexdigest()

class Chain:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.path.touch(exist_ok=True)
    def inspect(self,signed=False,key=KEY):
        contents=self.path.read_bytes()
        if contents and not contents.endswith(b"\n"):return None,"TRUNCATED"
        rows=[];previous=GENESIS
        for i,line in enumerate(contents.splitlines()):
            try:r=json.loads(line)
            except (ValueError,UnicodeDecodeError):return None,"INVALID_JSON"
            if signed:
                if set(r)!={"body","mac"} or r["body"].get("prev")!=previous or r["body"].get("id")!=i+1:return None,"BROKEN_CHAIN"
                if not hmac.compare_digest(r["mac"],mac(r["body"],key)):return None,"MAC_FAIL"
                previous=digest(r)
            else:
                if set(r)!={"seq","prev","body","hash"} or r["seq"]!=i or r["prev"]!=previous:return None,"BROKEN_CHAIN"
                if r["hash"]!=digest({k:r[k] for k in ("seq","prev","body")}):return None,"HASH_FAIL"
                previous=r["hash"]
            rows.append(r)
        return rows,None
    def append(self,body,signed=False,key=KEY):
        rows,error=self.inspect(signed,key)
        if error:raise ValueError(error)
        if signed:
            content={"id":len(rows)+1,"prev":digest(rows[-1]) if rows else GENESIS,**body}
            record={"body":content,"mac":mac(content,key)}
        else:
            record={"seq":len(rows),"prev":rows[-1]["hash"] if rows else GENESIS,"body":body}
            record["hash"]=digest(record)
        with self.path.open("ab") as f:
            f.write((canonical(record)+"\n").encode());f.flush();os.fsync(f.fileno())
        return record
class System:
    def __init__(self,folder,key=KEY):
        folder=Path(folder)
        self.waldos={w:Chain(folder/"waldos"/(w+".jsonl")) for w in ("A","B")}
        self.witness=Chain(folder/"independent"/"anchors.jsonl")
        self.key=key
    def event(self,who,body):return self.waldos[who].append(body)
    def checkpoint(self):
        heads={}
        for k,j in self.waldos.items():
            rows,err=j.inspect()
            if err:raise ValueError(err)
            heads[k]={"count":len(rows),"hash":rows[-1]["hash"] if rows else GENESIS}
        return self.witness.append({"heads":heads,"baseline":BASELINE},True,self.key)["body"]["id"]
    def verify(self,pinned=None):
        checkpoints,err=self.witness.inspect(True,self.key)
        if err:return "INVALID","WITNESS_"+err
        if pinned is not None and len(checkpoints)<pinned:return "INVALID","WITNESS_ROLLBACK"
        if not checkpoints:return "UNANCHORED","NO_CHECKPOINT"
        latest=checkpoints[-1]["body"]
        suffix=False
        for k,j in self.waldos.items():
            rows,e=j.inspect()
            if e:return "INVALID","JOURNAL_"+k+"_"+e
            head=latest["heads"][k]
            if len(rows)<head["count"]:return "INVALID","ROLLBACK_"+k
            old=rows[head["count"]-1]["hash"] if head["count"] else GENESIS
            if old!=head["hash"]:return "INVALID","REWRITE_"+k
            suffix |= len(rows)>head["count"]
        return ("VERIFIED_PREFIX","UNANCHORED_SUFFIX") if suffix else ("VERIFIED","ANCHORED_PREFIX")
def run_attack(attack):
    with TemporaryDirectory() as d:
        s=System(d)
        for k in ("A","B"):
            s.event(k,{"kind":"STAGE","payload":"WAVE-"+k})
            s.event(k,{"kind":"FINAL","payload":"WAVE-"+k})
        pin=s.checkpoint()
        if attack=="erase_both":
            for j in s.waldos.values():j.path.write_bytes(b"")
        elif attack=="rollback_A":
            j=s.waldos["A"];j.path.write_bytes(j.path.read_bytes().splitlines()[0]+b"\n")
        elif attack=="rewrite_rehashed":
            j=s.waldos["A"];rows,_=j.inspect();j.path.write_bytes(b"")
            for row in rows:
                body=dict(row["body"]);body["payload"]="ALTERED";j.append(body)
        elif attack=="rollback_anchor":s.witness.path.write_bytes(b"")
        elif attack=="none":pass
        else:raise ValueError(attack)
        return {"attack":attack,"result":s.verify(pinned=pin),"baseline":BASELINE}
if __name__=="__main__":
    for name in ("none","erase_both","rollback_A","rewrite_rehashed","rollback_anchor"):
        print(run_attack(name))
