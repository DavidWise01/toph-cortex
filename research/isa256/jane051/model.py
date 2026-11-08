"""JANE 051: grouped observation reconciliation on a symbolic ternary state.

Classical simulation. The verifier NEVER reads ground truth, only evidence.
The evaluation harness knows truth to score error. Source-group identifiers are
assumed accurate, not authenticated.
"""
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import random, json

TERNARY=(-1,0,1)
WAVE='111222333444555555444333222111'
POS=27

@dataclass(frozen=True)
class Reading:
    source: str
    root: str
    sample: int
    value: int
    kind: str='sensor'
    def __post_init__(self):
        if self.value not in TERNARY: raise ValueError('nonternary')


def naive(readings, claim=1):
    """Repeated readings each vote separately (vulnerable to pseudoreplication)."""
    evidence=[claim]+[r.value for r in readings]
    n=Counter(evidence);top=max(n.values())
    winners=[v for v,c in n.items() if c==top]
    return winners[0] if len(winners)==1 else None


def group_aware(readings, claim=1, min_roots=3):
    """At most one vote per claimed root. Mixed readings in a root abstain.

    Require >=min_roots unanimous independent root votes AND agreement
    with claim, else ABSTAIN/CONFLICT. This sacrifices availability.
    """
    groups=defaultdict(set)
    for r in readings:groups[r.root].add(r.value)
    clean={root: next(iter(values)) for root,values in groups.items() if len(values)==1}
    mixed=len(groups)-len(clean)
    tally=Counter(clean.values())
    if mixed:return {'status':'CONFLICT','decision':None,'roots':len(clean),'mixed':mixed}
    if not tally:return {'status':'INSUFFICIENT','decision':None,'roots':0,'mixed':mixed}
    if len(tally)>1:return {'status':'CONFLICT','decision':None,'roots':len(clean),'mixed':mixed}
    vote=next(iter(tally))
    if len(clean)<min_roots:return {'status':'INSUFFICIENT','decision':None,'roots':len(clean),'mixed':mixed}
    if vote!=claim:return {'status':'CONFLICT','decision':None,'roots':len(clean),'mixed':mixed}
    return {'status':'CORROBORATED','decision':vote,'roots':len(clean),'mixed':mixed}


def trial(seed=11,mode='independent',repeat=9,groups=3,error=.12,shared_error=.2):
    """One truth=-1 / signed historical claim=+1 case: check whether false
    claims are falsely corroborated. Each sensor group's bias is latent.
    When mode='independent', groups have independent errors. When cloned,
    all readings use one common root and latent result. When correlated,
    distinct roots share a common upstream failure, showing limitation.
    """
    if mode not in ('independent','cloned','correlated'):raise ValueError('mode')
    if repeat<1 or groups<1 or not(0<=error<=1) or not(0<=shared_error<=1):raise ValueError('parameters')
    rng=random.Random(seed)
    truth=-1;claim=1
    readings=[]
    correlated_flip=rng.random()<shared_error
    root_count=1 if mode=='cloned' else groups
    clones_flip=rng.random()<error
    for g in range(root_count):
        flip=clones_flip if mode=='cloned' else ((mode=='correlated' and correlated_flip) or rng.random()<error)
        v=1 if flip else -1
        for i in range(repeat):readings.append(Reading(f'sensor-{g}',f'root-{g}',i,v))
    rng.shuffle(readings)
    n=naive(readings,claim)
    g=group_aware(readings,claim)
    return {'truth':truth,'claim':claim,'readings':readings,'naive':n,
            'group':g,'false_naive':int(n==claim),'false_group':int(g['decision']==claim),
            'roots':root_count}


def run_batch(seeds=1000,error=.12,repeat=9,groups=3,shared_error=.2):
    rows=[]
    for mode in ('independent','cloned','correlated'):
        data=[trial(seed=10001+i,mode=mode,repeat=repeat,groups=groups,
                    error=error,shared_error=shared_error) for i in range(seeds)]
        rows.append({'mode':mode,'trials':seeds,'readings':data[0]['roots']*repeat,
                     'roots':data[0]['roots'],
                     'false_naive':sum(d['false_naive'] for d in data),
                     'false_group':sum(d['false_group'] for d in data),
                     'group_abstained':sum(d['group']['decision'] is None for d in data),
                     'group_conflict':sum(d['group']['status']=='CONFLICT' for d in data)})
    return rows


def healthy_trial(seed=11,mode='independent',repeat=9,groups=3,error=.12):
    rng=random.Random(seed);truth=claim=1;readings=[]
    ng=1 if mode=='cloned' else groups
    for g in range(ng):
        v=-1 if rng.random()<error else 1
        for i in range(repeat):readings.append(Reading(f's-{g}',f'root-{g}',i,v))
    return group_aware(readings,claim)['status']


def healthy_batch(seeds=1000,error=.12):
    return [{'mode':mode,'corroborated':sum(healthy_trial(10001+i,mode,error=error)=='CORROBORATED' for i in range(seeds))}
            for mode in ('independent','cloned')]

if __name__=='__main__':
    print(json.dumps({'false_claim':run_batch(),'correct_claim':healthy_batch()},indent=2))
