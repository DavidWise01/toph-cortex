"""JANE 036: exact rational asynchronous two-waldo wave transport (classical)."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
import json
N=27
LEVELS="111222333444555555444333222111"
INITIAL_A=(-3.0,0.5,2.0)
INITIAL_B=(5.0,-0.25,-7.0)
PATH_A=tuple(map(float,LEVELS[:27]))
PATH_B=tuple(map(float,LEVELS[3:]))
@dataclass(frozen=True)
class Carrier:
    identity:str
    field:tuple
    register:tuple
def initial():
    return Carrier("minus",PATH_A,INITIAL_A),Carrier("plus",PATH_B,INITIAL_B)
def exchange(a,b):
    return (Carrier(a.identity,a.field,(b.register[2],a.register[1],b.register[0])),
            Carrier(b.identity,b.field,(a.register[2],b.register[1],a.register[0])))
def energy(a,b):
    return sum(x*x for x in (*a.field,*b.field,*a.register,*b.register))
def parse_ratio(q,r):
    if not isinstance(q,int) or not isinstance(r,int) or q<1 or r<1 or gcd(q,r)!=1:
        raise ValueError("require positive coprime integer q,r for v+=r/q")
    return Fraction(r,q)
def encounter_times(q,r):
    """All nonorigin encounters during first simultaneous positional return."""
    v=parse_ratio(q,r)
    period=Fraction(N*q,1)
    events=[]
    for k in range(1,q+r):
        t=Fraction(N*q*k,q+r)
        x=t%N
        assert 0<x<N and (-(v*t))%N==x
        events.append((t,x))
    return period,events
def run(q,r,cycles=2):
    if not 1<=cycles<=5:raise ValueError("cycles 1..5")
    period,events=encounter_times(q,r)
    a,b=initial()
    initial_energy=energy(a,b)
    log=[]
    for cycle in range(cycles):
        for t,x in events:
            moment=t+cycle*period
            before=(a.register,b.register)
            a,b=exchange(a,b)
            log.append(dict(time=float(moment),time_exact=str(moment),position=float(x),
                position_exact=str(x),direction="edge" if x.denominator!=1 else "vertex",
                exchanged=True,registers_before=before,registers_after=(a.register,b.register),
                conserved=energy(a,b)==initial_energy))
    return dict(q=q,r=r,v_plus=str(Fraction(r,q)),v_minus="1",
        spatial_period=float(period),spatial_period_exact=str(period),
        encounter_count=len(events),parity="even" if len(events)%2==0 else "odd",
        first_encounter=log[0] if log else None,
        energy=initial_energy,energy_after=energy(a,b),
        states_after_cycles="original" if len(events)*cycles%2==0 else "exchanged",
        full_closure_time=float(period*(1 if len(events)%2==0 else 2)),
        full_closure_exact=str(period*(1 if len(events)%2==0 else 2)),
        restored=(a,b)==initial(),seam="27→27.5→1",events=log)
def summary(q,r):
    _,ev=encounter_times(q,r)
    return dict(q=q,r=r,speed=f"{r}/{q}",encounters=len(ev),
        first_time=str(ev[0][0]),first_position=str(ev[0][1]),
        period=str(N*q),full_closure=str(N*q*(2 if len(ev)%2 else 1)),
        after_one_lap="original" if len(ev)%2==0 else "exchanged",
        vertex_meetings=sum(x.denominator==1 for _,x in ev),
        edge_meetings=sum(x.denominator!=1 for _,x in ev))
if __name__=="__main__":
    print(json.dumps([summary(*p) for p in [(1,1),(5,4),(5,3),(5,2),(7,6),(4,1)]],indent=2))
