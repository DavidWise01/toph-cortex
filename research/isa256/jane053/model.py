"""JANE 053: label-free drift detection among five synthetic observers.

Truth is used only to generate and score observations, never for grouping or drift detection.
"""
from dataclasses import dataclass
from collections import deque
import hashlib,json,random
SOURCES=('A','B','C','D','E')
OLD_CLONE=(0,1,2)
NEW_CLONE=(0,3,4)
OLD_TRAIN=180
CHANGE=280
N_EVENTS=630
WINDOW=64
THRESHOLD=.09
DRIFT_THRESHOLD=.17
CONFIRM=12
MIN_AFTER=48
def emit(seed=11,switch=True,length=N_EVENTS,common=.29,idiosyncratic=.015,solo=.13):
    rng=random.Random(seed);rows=[]
    for t in range(length):
        truth=rng.randrange(2)
        active=NEW_CLONE if switch and t>=CHANGE else OLD_CLONE
        shared=int(rng.random()<common)
        reads=[]
        for i in range(5):
            wrong=(shared ^ int(rng.random()<idiosyncratic)) if i in active else int(rng.random()<solo)
            reads.append(truth ^ wrong)
        rows.append({'time':t,'reads':tuple(reads),'truth':truth})
    return rows
def mismatch(rows,i,j):
    return sum(r['reads'][i]!=r['reads'][j] for r in rows)/len(rows)
def groups(rows,threshold=THRESHOLD):
    if not rows:raise ValueError('empty window')
    available=list(range(len(SOURCES)));out=[]
    while available:
        cluster=[available.pop(0)]
        for i in list(available):
            if all(mismatch(rows,i,j)<=threshold for j in cluster):
                cluster.append(i);available.remove(i)
        out.append(tuple(cluster))
    return tuple(out)
def group_names(partition):
    return [''.join(SOURCES[i] for i in group) for group in partition]
def assess(reads,partition,claim):
    votes=[]
    for cluster in partition:
        support=sum(reads[i]==claim for i in cluster)
        votes.append(True if support*2>len(cluster) else False if support*2<len(cluster) else None)
    return sum(v is True for v in votes)>=2
def digest(version,epoch,partition,previous):
    raw=json.dumps({'version':version,'epoch':epoch,'groups':partition,'previous':previous},sort_keys=True,separators=(',',':'))
    return hashlib.sha256(raw.encode()).hexdigest()
@dataclass(frozen=True)
class Snapshot:
    version:int
    epoch:int
    partition:tuple
    previous:str
    hash:str
class DriftMonitor:
    def __init__(self,baseline,window=WINDOW,threshold=THRESHOLD,drift_threshold=DRIFT_THRESHOLD,confirm=CONFIRM,min_after=MIN_AFTER):
        self.window=window;self.threshold=threshold;self.drift_threshold=drift_threshold
        self.confirm=confirm;self.min_after=min_after
        self.initial=groups(baseline[-window:],threshold)
        h=digest(0,0,self.initial,'0'*64)
        self.versions=[Snapshot(0,0,self.initial,'0'*64,h)]
        self.buffer=deque(baseline[-window:],maxlen=window)
        self.streak=0;self.mode='STABLE';self.candidate=[];self.change_events=[]
        self.flag_time=None;self.transition_time=None;self.vote_partition=self.initial
    def history_valid(self):
        prev='0'*64
        for s in self.versions:
            if s.previous!=prev or digest(s.version,s.epoch,s.partition,s.previous)!=s.hash:return False
            prev=s.hash
        return True
    def step(self,row):
        self.buffer.append(row)
        if len(self.buffer)<self.window:return self.vote_partition,self.mode
        pairs=[(a,b) for group in self.versions[-1].partition for a in group for b in group if a<b]
        m=max((mismatch(tuple(self.buffer),a,b) for a,b in pairs),default=0)
        if self.mode=='STABLE':
            self.streak=self.streak+1 if m>=self.drift_threshold else 0
            if self.streak>=self.confirm:
                self.mode='UNCERTAIN';self.flag_time=row['time']
                self.change_events.append({'event':'FLAG','time':row['time'],'max_pair_disagreement':round(m,4)})
                self.candidate=[];self.transition_time=row['time'];self.streak=0
        elif self.mode=='UNCERTAIN':
            self.candidate.append(row)
            if len(self.candidate)>=self.min_after:
                new=groups(self.candidate[-self.window:],self.threshold)
                old=self.versions[-1]
                if new!=old.partition:
                    version=old.version+1
                    h=digest(version,row['time'],new,old.hash)
                    self.versions.append(Snapshot(version,row['time'],new,old.hash,h))
                    self.vote_partition=new
                    self.change_events.append({'event':'REVISE','time':row['time'],'from':group_names(old.partition),'to':group_names(new)})
                else:self.change_events.append({'event':'RETAIN','time':row['time']})
                self.mode='STABLE';self.streak=0;self.candidate=[]
        return self.vote_partition,self.mode
def run(seed=1,switch=True,length=N_EVENTS,method='adaptive',error_rate=.13):
    if method not in ('adaptive','frozen','instant'):raise ValueError(method)
    data=emit(seed,switch,length,solo=error_rate)
    mon=DriftMonitor(data[:OLD_TRAIN]);baseline=mon.initial
    outcomes=[]
    for r in data[OLD_TRAIN:]:
        if method=='adaptive':
            partition,state=mon.step(r)
            accepted=False if state=='UNCERTAIN' else assess(r['reads'],partition,1-r['truth'])
            accepted_true=False if state=='UNCERTAIN' else assess(r['reads'],partition,r['truth'])
        elif method=='frozen':
            partition=baseline
            accepted=assess(r['reads'],partition,1-r['truth'])
            accepted_true=assess(r['reads'],partition,r['truth'])
        else:
            partition=groups(data[max(0,r['time']-WINDOW+1):r['time']+1])
            accepted=assess(r['reads'],partition,1-r['truth'])
            accepted_true=assess(r['reads'],partition,r['truth'])
        outcomes.append({'time':r['time'],'accepted':accepted,'accepted_true':accepted_true,'state':mon.mode if method=='adaptive' else method})
    pre=[x for x in outcomes if x['time']<CHANGE]
    post=[x for x in outcomes if x['time']>=CHANGE+90]
    return {'method':method,'seed':seed,'baseline':group_names(baseline),
        'final':group_names(mon.vote_partition) if method=='adaptive' else (group_names(baseline) if method=='frozen' else group_names(partition)),
        'false_approvals_pre':sum(x['accepted'] for x in pre),
        'false_approvals_post':sum(x['accepted'] for x in post),
        'true_approvals_post':sum(x['accepted_true'] for x in post),
        'pre_trials':len(pre),'post_trials':len(post),
        'first_flag':mon.flag_time,'versions':len(mon.versions),
        'events':mon.change_events,'history_valid':mon.history_valid(),
        'uncertain_events':sum(x['state']=='UNCERTAIN' for x in outcomes),
        'outcomes':outcomes}
def sweep(trials=100):
    results=[]
    for scenario,switch in [('changed',True),('unchanged',False)]:
        for method in ('adaptive','frozen','instant'):
            batch=[run(seed=7000+i,switch=switch,method=method) for i in range(trials)]
            flagged=[x['first_flag'] for x in batch if x['first_flag'] is not None]
            results.append({'scenario':scenario,'method':method,'trials':trials,
                'post_samples':sum(x['post_trials'] for x in batch),
                'false_post':sum(x['false_approvals_post'] for x in batch),
                'true_post':sum(x['true_approvals_post'] for x in batch),
                'false_pre':sum(x['false_approvals_pre'] for x in batch),
                'flags':len(flagged),'revisions':sum(x['versions']>1 for x in batch),
                'mean_first_flag':round(sum(flagged)/len(flagged),2) if flagged else None})
    return results
if __name__=='__main__':print(json.dumps(sweep(),indent=2))
