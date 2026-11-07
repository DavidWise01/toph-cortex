"""Jane 031: locally corroborated distributed learning in a 2 x 72-slot primitive."""
from dataclasses import dataclass
from collections import Counter, defaultdict
import hashlib, json, random

MAX_RECORDS=3
BASE=0.02
OFFSET=0.003

def pack_record(key,value):
    if not 0<=key<512 or not 0<=value<512: raise ValueError("9-bit symbol")
    return (1,)+tuple((key>>i)&1 for i in range(9))+tuple((value>>i)&1 for i in range(9))

def unpack_record(bits):
    if len(bits)!=19 or bits[0]!=1: return None
    return (sum(bits[i+1]<<i for i in range(9)),sum(bits[i+10]<<i for i in range(9)))

class Primitive:
    def __init__(self,index):
        self.index=index
        self.cells=[[BASE]*72 for _ in range(2)]
        self.local=defaultdict(Counter)
        self.candidates=defaultdict(Counter)
        self.provenance=defaultdict(list)
        self.conflicts=[]
        self.history=[]
        self.learned={}
        self.next_seq=0
        self.received_seq=defaultdict(set)
    def _write(self,pair,bit):
        self.cells[0][pair]=BASE+(OFFSET if bit else -OFFSET)
        self.cells[1][pair]=BASE-(OFFSET if bit else -OFFSET)
    def _read(self,pair):
        d=self.cells[0][pair]-self.cells[1][pair]
        return None if abs(d)<OFFSET else int(d>0)
    def encode(self,mapping):
        if len(mapping)>MAX_RECORDS: raise ValueError("capacity")
        for i in range(57):
            self.cells[0][i]=BASE
            self.cells[1][i]=BASE
        for entry,(k,v) in enumerate(sorted(mapping.items())):
            for j,b in enumerate(pack_record(k,v)): self._write(entry*19+j,b)
        self.learned=dict(mapping)
    def decode(self):
        out={}
        for i in range(MAX_RECORDS):
            bits=[self._read(i*19+j) for j in range(19)]
            if any(b is None for b in bits): continue
            rec=unpack_record(bits)
            if rec: out[rec[0]]=rec[1]
        return out
    def observe(self,k,v):
        if not(0<=k<512 and 0<=v<512): raise ValueError("symbol")
        self.history.append((k,v))
        self.local[k][v]+=1
        if len(self.local[k])>1:
            self.conflicts.append(("local",k,tuple(sorted(self.local[k].items()))))
            m=self.decode()
            if k in m: m.pop(k);self.encode(m)
            return
        self._promote(k,v)
    def _promote(self,k,v):
        counts=self.local[k]
        if len(counts)!=1 or counts[v]<1: return
        neighbor=max((n for (sender,out),n in self.candidates[k].items() if out==v),default=0)
        if counts[v]<3 and neighbor<3:return
        m=self.decode()
        if k in m and m[k]!=v:
            self.conflicts.append(("encoded",k,m[k],v));return
        if k not in m and len(m)>=MAX_RECORDS:return
        m[k]=v
        self.encode(m)
    def receive(self,msg):
        if not msg.valid():return "CORRUPT"
        if msg.to!=self.index:return "WRONG_DEST"
        if msg.seq in self.received_seq[msg.src]:return "REPLAY"
        self.received_seq[msg.src].add(msg.seq)
        self.provenance[msg.key].append((msg.src,msg.value,msg.samples,msg.seq))
        if self.local[msg.key] and msg.value not in self.local[msg.key]:
            self.conflicts.append(("neighbor",msg.key,msg.src,msg.value))
            return "CONFLICT"
        self.candidates[msg.key][(msg.src,msg.value)]=max(self.candidates[msg.key][(msg.src,msg.value)],msg.samples)
        self._promote(msg.key,msg.value)
        return "CANDIDATE"
    def message(self,to,key):
        if key not in self.decode():return None
        val=self.decode()[key]
        self.next_seq+=1
        return Message.make(self.index,to,self.next_seq,key,val,self.local[key][val])
    def predict(self,key):return self.decode().get(key)
    def export(self):
        return {"id":self.index,"cells":self.cells,
          "local":{str(k):dict(v) for k,v in self.local.items()},
          "candidates":{str(k):[[s,o,n] for (s,o),n in v.items()] for k,v in self.candidates.items()},
          "provenance":{str(k):v for k,v in self.provenance.items()},
          "next_seq":self.next_seq,"received_seq":{str(k):sorted(v) for k,v in self.received_seq.items()},
          "conflicts":self.conflicts}
    @classmethod
    def restore(cls,data):
        p=cls(data["id"]);p.cells=data["cells"]
        if len(p.cells)!=2 or any(len(c)!=72 for c in p.cells):raise ValueError("shape")
        p.local=defaultdict(Counter,{int(k):Counter({int(v):int(n) for v,n in counts.items()}) for k,counts in data["local"].items()})
        p.candidates=defaultdict(Counter,{int(k):Counter({(s,o):n for s,o,n in entries}) for k,entries in data["candidates"].items()})
        p.provenance=defaultdict(list,{int(k):v for k,v in data["provenance"].items()})
        p.next_seq=data["next_seq"]
        p.received_seq=defaultdict(set,{int(k):set(v) for k,v in data["received_seq"].items()})
        p.conflicts=data["conflicts"];p.learned=p.decode()
        return p

@dataclass(frozen=True)
class Message:
    src:int;to:int;seq:int;key:int;value:int;samples:int;digest:str
    @staticmethod
    def _hash(args):return hashlib.sha256(json.dumps(args,separators=(",",":")).encode()).hexdigest()
    @classmethod
    def make(cls,src,to,seq,key,value,samples):
        args=[src,to,seq,key,value,samples]
        return cls(*args,cls._hash(args))
    def valid(self):
        return self.digest==self._hash([self.src,self.to,self.seq,self.key,self.value,self.samples]) and self.samples>=1 and 0<=self.key<512 and 0<=self.value<512

RULES=((17,68),(68,130),(130,17))
def run(seed=31,loss=.15,contradiction=False):
    rng=random.Random(seed)
    a=Primitive(0);b=Primitive(1);isolated=Primitive(2)
    for k,v in RULES:
        for _ in range(4):a.observe(k,v)
        b.observe(k,v);isolated.observe(k,v)
    messages=[];delivered=0;dropped=0
    for k,_ in RULES:
        m=a.message(1,k)
        if rng.random()<loss:dropped+=1
        else:messages.append(m);delivered+=1
    rng.shuffle(messages)
    for m in messages:b.receive(m)
    if contradiction:
        k,v=RULES[0]
        b.receive(Message.make(3,1,1,k,(v+1)%512,12))
    correct=lambda p:sum(p.predict(k)==v for k,v in RULES)
    return {"learned":correct(b),"isolated":correct(isolated),"source":correct(a),
      "delivered":delivered,"dropped":dropped,"conflicts":len(b.conflicts),
      "memory_bits":57,"positions_per_primitive":144,"source_memory":a.decode(),
      "recipient_memory":b.decode(),"isolation_memory":isolated.decode(),"recipient":b.export()}
if __name__=="__main__":
    for loss in (0,.15,.5,1):
        r=run(loss=loss)
        print(loss,{k:v for k,v in r.items() if k!="recipient"})
