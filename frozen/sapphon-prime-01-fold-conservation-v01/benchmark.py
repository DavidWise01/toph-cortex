#!/usr/bin/env python3
import random
SEED="-+-00K00+-+"
FIB="00112358"

def fold(seed):
    k=seed.index("K")
    return seed[:k][::-1],"K",seed[k+1:]

def unfold(f):
    a,k,b=f
    return a[::-1]+k+b

def rotate(s,n):
    n%=len(s)
    return s[n:]+s[:n]

def align_k_toroid(s):
    if s.count("K")!=1: raise ValueError("K must be unique")
    target=SEED.index("K"); current=s.index("K")
    return rotate(s,current-target)

def flay(ref,obs):
    return [i for i,(a,b) in enumerate(zip(ref,obs)) if a!=b] if len(ref)==len(obs) else ["length"]

def run():
    top=[]
    def ck(name,cond,detail=None):
        top.append({"name":name,"pass":bool(cond),"detail":detail})
        if not cond: raise AssertionError(name)
    ck("literal_seed",SEED=="-+-00K00+-+",SEED)
    ck("unique_K",SEED.count("K")==1 and SEED.index("K")==5,SEED.index("K"))
    ck("fold_unfold_roundtrip",unfold(fold(SEED))==SEED,fold(SEED))
    ck("all_toroidal_rotations_realign",
       all(align_k_toroid(rotate(SEED,r))==SEED for r in range(len(SEED))),len(SEED))
    alphabet="-+0K12358"
    cases=0; bad=0
    for i,old in enumerate(SEED):
        for new in alphabet:
            if new==old: continue
            cases+=1
            obs=SEED[:i]+new+SEED[i+1:]
            if flay(SEED,obs)!=[i]: bad+=1
    ck("flay_single_mutator_exact",bad==0,{"cases":cases,"failures":bad})
    k=SEED.index("K")
    ck("pinned_K_corruption_detected",
       all(flay(SEED,SEED[:k]+c+SEED[k+1:])==[k] for c in "-+012358"),7)
    vals=list(map(int,FIB))
    ck("fibonacci_pack_00112358",vals==[0,0,1,1,2,3,5,8],vals)
    rng=random.Random(0); undetected=0
    for _ in range(100000):
        chars=list(SEED)
        for i in rng.sample(range(len(SEED)),rng.randint(1,5)):
            chars[i]=rng.choice([c for c in alphabet if c!=chars[i]])
        if not flay(SEED,"".join(chars)): undetected+=1
    ck("random_corruption_detection",undetected==0,{"trials":100000,"undetected":undetected})
    carrier=[1,2,1,2,-1,1,1,2,1,2]
    ck("carrier_center_balance",carrier[4]+carrier[5]==0,{"path_sum":sum(carrier)})
    ck("antistropic_residual",((-3)+2,2+(-3))==(-1,-1),(-1,-1))
    return {"status":"PASS","seed":SEED,"fib_pack":FIB,
            "tests_total":len(top),"tests_passed":sum(t["pass"] for t in top),"tests":top}

if __name__=="__main__":
    r=run()
    print("0e / PASS / top_tests=%d / seed=%s"%(r["tests_total"],r["seed"]))
