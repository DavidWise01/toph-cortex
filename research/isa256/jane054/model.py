"""JANE054 — finite-history predictive drift and recurrence experiment.

The truth label only generates observations and scores predictions. No internal
monitor or source-grouping function receives ground truth.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from collections import deque
import hashlib,json,random,math

SOURCES='ABCDE'
OLD=(0,1,2)
NEW=(0,3,4)
PAIRS=list(combinations(range(5),2))
W=40
START=100
END=600
THRESHOLD=.075

def generate(seed,scenario='periodic',end=END):
    if scenario not in ('steady','abrupt','gradual','periodic','transient'): raise ValueError(scenario)
    rng=random.Random(seed)
    out=[]
    for t in range(end):
        if scenario=='steady': q=0
        elif scenario=='abrupt':q=int(t>=260)
        elif scenario=='gradual':q=min(1,max(0,(t-220)/180))
        elif scenario=='transient':q=int(270<=t<330)
        else:q=int((t//110)%2==1)
        regime=NEW if rng.random()<q else OLD
        truth=rng.randrange(2)
        shared=int(rng.random()<.28)
        reads=[]
        for i in range(5):
            wrong=(shared ^ int(rng.random()<.012)) if i in regime else int(rng.random()<.13)
            reads.append(truth ^ wrong)
        out.append({'time':t,'reads':tuple(reads),'truth':truth,'regime':int(regime==NEW)})
    return out

def fingerprint(rows):
    if not rows:raise ValueError('empty observations')
    return tuple(sum(a['reads'][i]!=a['reads'][j] for a in rows)/len(rows) for i,j in PAIRS)

def distance(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)

def groups(rows,threshold=THRESHOLD):
    f=fingerprint(rows)
    pair=dict(zip(PAIRS,f))
    remaining=list(range(5));part=[]
    while remaining:
        first=remaining.pop(0);cluster=[first]
        for c in tuple(remaining):
            if all(pair[tuple(sorted((c,j)))]<=threshold for j in cluster):
                cluster.append(c);remaining.remove(c)
        part.append(tuple(cluster))
    return tuple(part)

def group_names(part):return [''.join(SOURCES[i] for i in g) for g in part]

def supports(reads,partition,claim):
    supports=0
    for g in partition:
        yes=sum(reads[i]==claim for i in g)
        if yes*2>len(g):supports+=1
    return supports>=2

def digest(n,source,part,prev):
    s=json.dumps([n,source,part,prev],sort_keys=True,separators=(',',':'))
    return hashlib.sha256(s.encode()).hexdigest()

@dataclass(frozen=True)
class Version:
    n:int
    epoch:int
    partition:tuple
    previous:str
    hash:str

class Monitor:
    def __init__(self,training,window=W,limit=.09,confirm=2,probation=20):
        if len(training)<window:raise ValueError('insufficient training')
        self.window=window;self.limit=limit;self.confirm=confirm;self.probation=probation
        baseline=tuple(training[-window:]);part=groups(baseline)
        genesis='0'*64
        self.versions=[Version(0,training[-1]['time'],part,genesis,digest(0,training[-1]['time'],part,genesis))]
        self.prototypes=[fingerprint(baseline)]
        self.window_rows=deque(baseline,maxlen=window)
        self.mode='STABLE';self.pending=None;self.streak=0;self.probation_count=0
        self.events=[];self.revisits=0;self.revisions=0;self.abstentions=0
        self.active=0;self.seen_fingerprint=fingerprint(baseline)
    def history_valid(self):
        prev='0'*64
        for v in self.versions:
            if v.previous!=prev or v.hash!=digest(v.n,v.epoch,v.partition,v.previous):return False
            prev=v.hash
        return True
    def checkpoint(self,t,part):
        prev=self.versions[-1].hash;n=len(self.versions)
        self.versions.append(Version(n,t,part,prev,digest(n,t,part,prev)))
    def step(self,row):
        self.window_rows.append(row)
        if row['time']%10!=0:
            return self.versions[self.active].partition,self.mode
        window=list(self.window_rows);f=fingerprint(window)
        distances=[distance(f,p) for p in self.prototypes]
        best=min(range(len(distances)),key=lambda j:distances[j])
        if self.mode=='STABLE':
            current=distances[self.active]
            other=distances[best]
            changed=current>self.limit and (best!=self.active and other+self.limit/4<current or best==self.active)
            self.streak=self.streak+1 if changed else 0
            if self.streak>=self.confirm:
                self.mode='UNCERTAIN';self.probation_count=0;self.pending=best
                self.events.append({'time':row['time'],'kind':'FLAG','from':self.active,'candidate':best,'distance':round(current,3)})
                self.streak=0
        else:
            self.probation_count+=10
            if self.probation_count>=self.probation:
                f=fingerprint(list(self.window_rows))
                distances=[distance(f,p) for p in self.prototypes]
                best=min(range(len(distances)),key=lambda j:distances[j])
                if best!=self.active and distances[best]<=self.limit:
                    self.active=best;self.revisits+=1
                    self.events.append({'time':row['time'],'kind':'REVISIT','version':best})
                elif distances[self.active]<=self.limit:
                    self.events.append({'time':row['time'],'kind':'RETAIN','version':self.active})
                else:
                    part=groups(list(self.window_rows))
                    self.checkpoint(row['time'],part);self.prototypes.append(f);self.active=len(self.prototypes)-1
                    self.revisions+=1
                    self.events.append({'time':row['time'],'kind':'NEW_VERSION','version':self.active,'groups':group_names(part)})
                self.mode='STABLE';self.probation_count=0
        return self.versions[self.active].partition,self.mode

def evaluate(seed,scenario,method):
    if method not in ('frozen','rolling','versioned'):raise ValueError(method)
    data=generate(seed,scenario)
    m=Monitor(data[:START]);initial=m.versions[0].partition
    records=[]
    for row in data[START:]:
        if method=='versioned':part,mode=m.step(row)
        elif method=='rolling':
            part=groups(data[max(0,row['time']-W+1):row['time']+1]);mode='STABLE'
        else:part=initial;mode='STABLE'
        accept_false=mode=='STABLE' and supports(row['reads'],part,1-row['truth'])
        accept_true=mode=='STABLE' and supports(row['reads'],part,row['truth'])
        records.append({'t':row['time'],'false':int(accept_false),'true':int(accept_true),'abstain':int(mode!='STABLE')})
    r={'scenario':scenario,'method':method,'seed':seed,'false':sum(x['false'] for x in records),'correct':sum(x['true'] for x in records),'uncertain':sum(x['abstain'] for x in records),
       'versions':len(m.versions) if method=='versioned' else None,
       'revisits':m.revisits if method=='versioned' else None,
       'events':m.events if method=='versioned' else [],'chain_valid':m.history_valid(),
       'original':group_names(initial),'final':group_names(m.versions[m.active].partition) if method=='versioned' else None}
    return r

def sweep(trials=35):
    out=[]
    for scenario in ('steady','abrupt','gradual','periodic','transient'):
        for method in ('frozen','rolling','versioned'):
            runs=[evaluate(4096+i,scenario,method) for i in range(trials)]
            out.append({'scenario':scenario,'method':method,'trials':trials,'evaluations':trials*(END-START),
                        'false':sum(a['false'] for a in runs),'correct':sum(a['correct'] for a in runs),
                        'uncertain':sum(a['uncertain'] for a in runs),'new_versions':sum((a['versions'] or 1)-1 for a in runs),
                        'revisits':sum(a['revisits'] or 0 for a in runs),'invalid_chain':sum(not a['chain_valid'] for a in runs)})
    return out
if __name__=='__main__': print(json.dumps(sweep(),indent=2))
