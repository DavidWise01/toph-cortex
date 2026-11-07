"""JANE034: explicit ternary wave-exchange interpretation. Standard library only."""
from dataclasses import dataclass
N=27
MODES=(-1,0,1)
WAVE="111222333444555555444333222111"
@dataclass(frozen=True)
class Waldo:
    identity:str
    path:tuple
    register:tuple
    def __post_init__(self):
        assert len(self.path)==N and len(self.register)==3
def make_waldos():
    return (Waldo("minus",tuple(map(float,WAVE[:N])),(-3.,.5,2.)),
            Waldo("plus",tuple(map(float,WAVE[3:])),(5.,-.25,-7.)))
def exchange(a,b):
    am,az,ap=a.register
    bm,bz,bp=b.register
    return Waldo(a.identity,a.path,(bp,az,bm)),Waldo(b.identity,b.path,(ap,bz,am))
def energy(a,b):
    return sum(x*x for w in (a,b) for x in (*w.path,*w.register))
def position(t,direction):
    return (direction*t)%N
def meeting():
    return position(13.5,1)==position(13.5,-1)==13.5
def seam():
    return (27,27.5,1)
def experiment():
    a,b=make_waldos()
    a1,b1=exchange(a,b)
    a2,b2=exchange(a1,b1)
    return dict(positions=N,register_labels=list(MODES),counted_components=N+len(MODES),
                wave=WAVE,palindrome=WAVE==WAVE[::-1],
                level_counts={str(i):WAVE.count(str(i)) for i in range(1,6)},
                midpoint=13.5,closing_seam=list(seam()),initial=[a.register,b.register],
                exchanged=[a1.register,b1.register],restored=[a2.register,b2.register],
                energy_before=energy(a,b),energy_after=energy(a1,b1),
                reversible=(a,b)==(a2,b2),identity_preserved=(a.identity,b.identity)==(a1.identity,b1.identity))
if __name__=="__main__":
    import json
    print(json.dumps(experiment(),indent=2))
