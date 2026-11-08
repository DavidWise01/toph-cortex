"""JANE037: two independently jittering waldos, finite overlap and local sensor debounce.
Classical simulation, not a physical wave equation. Standard library only.
"""
import random,math,json
N=27
WAVE="111222333444555555444333222111"
A0=(-3.,.5,2.)
B0=(5.,-.25,-7.)
F0=tuple(map(float,WAVE[:27]))
F1=tuple(map(float,WAVE[3:]))
def swap(a,b):
    a[0],b[2]=b[2],a[0]
    a[2],b[0]=b[0],a[2]
def norm(a,b):
    return sum(x*x for x in (*F0,*F1,*a,*b))
def dist(a,b):
    d=(a-b)%N
    return min(d,N-d)
def run(seed=1,jitter=.08,width=.28,sensor_error=0.,method="debounce",duration=50.,dt=.02,speed_ratio=1.,drop_rate=0.):
    if not (0<=jitter<1 and 0<width<3 and 0<=sensor_error<.5 and 0<=drop_rate<=1 and .005<=dt<=.1 and speed_ratio>0 and duration>0):
        raise ValueError("invalid simulation parameters")
    if method not in ("raw","latch","debounce","oracle"):raise ValueError("method")
    rng=random.Random(seed)
    a,b=list(A0),list(B0)
    x=y=0.
    armed=False # initially overlapped at common origin, not a new encounter
    clear=hits=0
    true_count=actual=0
    events=[]
    base=norm(a,b)
    for i in range(1,round(duration/dt)+1):
        old=x-y
        x+=dt*(1+jitter*rng.uniform(-1,1))
        y-=dt*speed_ratio*(1+jitter*rng.uniform(-1,1))
        crossing=math.floor((x-y)/N)>math.floor(old/N)
        true_count+=int(crossing)
        overlap=dist(x,y)<=width
        sensed=(not overlap) if rng.random()<sensor_error else overlap
        trigger=False
        if method=="oracle": trigger=crossing
        elif method=="raw": trigger=sensed
        elif method=="latch":
            if not sensed:armed=True
            if sensed and armed:
                trigger=True;armed=False
        elif method=="debounce":
            if sensed:
                hits+=1;clear=0
                if hits>=3 and armed:
                    trigger=True;armed=False
            else:
                clear+=1;hits=0
                if clear>=3:armed=True
        if trigger and rng.random()>=drop_rate:
            swap(a,b)
            actual+=1
            events.append({"time":round(i*dt,4),"phase":round(x%N,4),"distance":round(dist(x,y),4)})
    return {"true_crossings":true_count,"triggered_exchanges":actual,
            "energy_start":base,"energy_end":norm(a,b),
            "restored":tuple(a)==A0 and tuple(b)==B0,
            "records":events}
def sweep(trials=100):
    out=[]
    for jitter in (0.,.04,.12):
        for sensor_error in (0.,.002,.01,.03):
            for method in ("raw","latch","debounce","oracle"):
                data=[run(seed=51+i,jitter=jitter,sensor_error=sensor_error,method=method) for i in range(trials)]
                out.append({"jitter":jitter,"sensor_error":sensor_error,"method":method,
                    "mean_exchanges":sum(x["triggered_exchanges"] for x in data)/trials,
                    "exact_count":sum(x["true_crossings"]==x["triggered_exchanges"] for x in data),
                    "conserved":all(x["energy_start"]==x["energy_end"] for x in data)})
    return out
if __name__=="__main__":print(json.dumps(sweep(),indent=2))
