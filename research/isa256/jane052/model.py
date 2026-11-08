"""JANE052: reference-free dependence discovery from repeated binary observations.
Synthetic classical experiment. Learner never receives hidden truth or real provider roots.
"""
import random,itertools,json
from dataclasses import dataclass
N_PATH=27
TERNARY=(-1,0,1)
WALDOS='{-()+}'
WAVE='111222333444555555444333222111'
SOURCES=('A','B','C','D','E')
@dataclass(frozen=True)
class Sample:
    event:int
    readings:tuple
    def as_dict(self):return dict(self.readings)

def generate(seed=1,train=200,test=1000,clone_error=.22,independent_error=.12,clone_jitter=0.,truth_fixed=None,drift=False):
    if not all(0<=p<=1 for p in (clone_error,independent_error,clone_jitter)):raise ValueError('invalid probability')
    rng=random.Random(seed);items=[]
    for t in range(train+test):
        truth=rng.randrange(2) if truth_fixed is None else truth_fixed
        common=rng.random()<clone_error
        values={}
        for name in SOURCES:
            if name in ('A','B','C'):
                flip=(rng.random()<clone_error) if drift and t>=train else (common ^ (rng.random()<clone_jitter))
            else:flip=rng.random()<independent_error
            values[name]=truth ^ int(flip)
        items.append((Sample(t,tuple(values.items())),truth))
    return items[:train],items[train:]

def pair_agreement(samples,a,b):
    if not samples:raise ValueError('need training data')
    return sum(s.as_dict()[a]==s.as_dict()[b] for s,_ in samples)/len(samples)

class Learner:
    def __init__(self,sources=SOURCES,threshold=.97):
        if not .5<threshold<=1:raise ValueError('threshold')
        self.sources=tuple(sources);self.threshold=threshold;self.groups=None;self.similarities={}
        self.warning=''
    def fit(self,events):
        samples=[row[0] if isinstance(row,tuple) else row for row in events]
        if len(samples)<20:raise ValueError('insufficient history')
        for s in samples:
            if set(s.as_dict())!=set(self.sources):raise ValueError('missing sources')
        graph={s:{s} for s in self.sources}
        for a,b in itertools.combinations(self.sources,2):
            score=sum(s.as_dict()[a]==s.as_dict()[b] for s in samples)/len(samples)
            self.similarities[(a,b)]=score
            if score>=self.threshold:graph[a].add(b);graph[b].add(a)
        unseen=set(self.sources);groups=[]
        while unseen:
            start=min(unseen);stack=[start];members=set()
            while stack:
                cur=stack.pop()
                if cur in members:continue
                members.add(cur);stack.extend(graph[cur]-members)
            groups.append(tuple(sorted(members)));unseen-=members
        self.groups=tuple(groups)
        self.warning='Agreement alone does not establish shared causal origin.'
        return self
    def vote(self,sample,claim):
        if self.groups is None:raise ValueError('fit first')
        data=sample.as_dict();yes=no=0
        for group in self.groups:
            count=sum(data[x]==claim for x in group)
            if 2*count>len(group):yes+=1
            elif 2*count<len(group):no+=1
        if yes>=2 and yes>no:return 'ACCEPT'
        if no>=2 and no>yes:return 'REJECT'
        return 'HOLD'

def naive_vote(sample,claim):
    return 'ACCEPT' if sum(v==claim for v in sample.as_dict().values())>=3 else 'REJECT'

def evaluate(train,holdout,threshold=.97):
    learner=Learner(threshold=threshold).fit(train)
    totals={'naive_false':0,'learned_false':0,'naive_true':0,'learned_true':0,
            'learned_hold_false':0,'learned_hold_true':0}
    for sample,truth in holdout:
        for is_false,claim in ((True,1-truth),(False,truth)):
            naive=naive_vote(sample,claim);learned=learner.vote(sample,claim)
            key='false' if is_false else 'true'
            totals['naive_'+key]+=naive=='ACCEPT'
            totals['learned_'+key]+=learned=='ACCEPT'
            totals['learned_hold_'+key]+=learned=='HOLD'
    return {'groups':learner.groups,'pairs':{'-'.join(k):round(v,4) for k,v in learner.similarities.items()},
            'trials':len(holdout),**totals}

def replicate(n_seeds=20,train_count=200,test_count=250,clone_jitter=0.,drift=False):
    runs=[]
    for i in range(n_seeds):
        train,test=generate(seed=100+i,train=train_count,test=test_count,
            clone_jitter=clone_jitter,drift=drift)
        runs.append(evaluate(train,test))
    keys=('naive_false','learned_false','naive_true','learned_true','learned_hold_false','learned_hold_true')
    return {'samples':n_seeds*test_count,'seeds':n_seeds,
        'groups_example':runs[0]['groups'],**{k:sum(r[k] for r in runs) for k in keys}}

def scenarios():
    result={'shared_training_and_test':replicate(),
       'near_clones_2pct_flip':replicate(clone_jitter=.02),
       'dependency_drift':replicate(drift=True)}
    a,b=generate(seed=39,independent_error=0,clone_error=0,train=200,test=100)
    result['all_perfect_sensors']=evaluate(a,b)
    return result
if __name__=='__main__':print(json.dumps(scenarios(),indent=2))
