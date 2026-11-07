"""JANE035: local edge-triggered wave exchange on abstract 27-cycle.

Classical toy-model; 27 occupied vertices, half-edge transitions not vertices.
Two opposing waldos with 27-value field and [-1,0,+1] registers each.
"""
from dataclasses import dataclass, replace
import json
N=27
WAVE='111222333444555555444333222111'
MODES=(-1,0,1)

@dataclass(frozen=True)
class Waldo:
    identity:str
    direction:int
    field:tuple
    register:tuple
    position:int=0
    def __post_init__(self):
        if self.direction not in (-1,1) or len(self.field)!=N or len(self.register)!=3:
            raise ValueError('invalid waldo')

def initial():
    return (Waldo('minus',+1,tuple(float(int(x)) for x in WAVE[:27]),(-3.,.5,2.)),
            Waldo('plus',-1,tuple(float(int(x)) for x in WAVE[3:]),(5.,-.25,-7.)))

def magnitude(pair):
    return sum(v*v for w in pair for v in (*w.field,*w.register))

def next_vertex(w):
    return (w.position+w.direction)%N

def edge_id(a,b):
    if (a+1)%N==b:return a
    if (b+1)%N==a:return b
    raise ValueError('not neighboring')

def edge_encounter(a,b):
    """Local edge sensor: opposite-moving pair enter the same undirected edge."""
    aa,bb=next_vertex(a),next_vertex(b)
    return a.position==bb and b.position==aa and a.position!=b.position

def exchange(a,b):
    """Opposite signed channels only. Involution; no identity/neutral changes."""
    am,az,ap=a.register;bm,bz,bp=b.register
    return replace(a,register=(bp,az,bm)),replace(b,register=(ap,bz,am))

def advance(pair,enable_exchange=True):
    a,b=pair
    event=None
    if edge_encounter(a,b):
        event={'edge':edge_id(a.position,b.position),'midpoint_time':None}
        if enable_exchange:a,b=exchange(a,b)
    return (replace(a,position=next_vertex(a)),replace(b,position=next_vertex(b))),event

def run(cycles=2,exchange_enabled=True):
    if cycles<1:raise ValueError('cycles>=1')
    pair=initial();energy0=magnitude(pair)
    events=[];trace=[];visited={w.identity:set() for w in pair}
    for tick in range(cycles*N):
        for w in pair:visited[w.identity].add(w.position)
        seam_cross=any((w.position,w.direction) in ((26,1),(0,-1)) for w in pair)
        entry={'t':tick,'a_vertex':pair[0].position+1,'b_vertex':pair[1].position+1,
               'energy':magnitude(pair),'seam':seam_cross,'registers':[list(w.register) for w in pair]}
        nxt,event=advance(pair,exchange_enabled)
        if event:
            event.update(tick=tick,midpoint_time=tick+.5,
                         from_vertices=[pair[0].position+1,pair[1].position+1],
                         exchange=exchange_enabled)
            events.append(event)
        trace.append(entry)
        pair=nxt
    return {'n':N,'ternary':list(MODES),'wave':WAVE,'wave_palindrome':WAVE==WAVE[::-1],
            'cycles':cycles,'exchange_enabled':exchange_enabled,
            'events':events,'event_count':len(events),
            'start_registers':[list(w.register) for w in initial()],
            'final_registers':[list(w.register) for w in pair],
            'positions_final':[w.position+1 for w in pair],
            'energy_initial':energy0,'energy_final':magnitude(pair),
            'visited_vertices':{k:len(v) for k,v in visited.items()},
            'restored':pair==initial(),'trace':trace}

if __name__=='__main__':
    print(json.dumps({k:v for k,v in run().items() if k!='trace'},indent=2))
