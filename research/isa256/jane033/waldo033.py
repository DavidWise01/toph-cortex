"""JANE033: two opposite waldos on a 27-vertex cyclic path.
The equal-speed, shared-start assumption is an experimental interpretation of {-()+}.
The user's 27→27.5→1 is a distinct closure transition.
"""
N=27
def positions(t,start=0):
    """Zero-based fractional indices; at integer times results are vertices."""
    return ((start+t)%N,(start-t)%N)
def vertex_meet(t):
    if int(t)!=t: return False
    a,b=positions(t)
    return a==b
def edge_swap(t):
    """Two waldos traverse same undirected edge in opposite directions from t to t+1."""
    a,b=positions(t);aa,bb=positions(t+1)
    return (a==bb and b==aa and a!=b)
def test():
    assert len({positions(t)[0] for t in range(27)})==27
    assert len({positions(t)[1] for t in range(27)})==27
    assert [t for t in range(27) if vertex_meet(t)]==[0]
    assert [t for t in range(27) if edge_swap(t)]==[13]
    assert positions(13)==(13,14)
    assert positions(14)==(14,13)
    assert positions(13.5)==(13.5,13.5)
    assert positions(27)==positions(0)
    assert sum(vertex_meet(t) for t in range(27))==1
    assert all(not vertex_meet(t) for t in range(1,27))
if __name__=="__main__":
    test()
    print("10/10 checks passed; edge meeting at t=13.5")
