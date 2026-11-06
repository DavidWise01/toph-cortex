#!/usr/bin/env python3
"""STOICHEION 256x8x4x3x2x1x1. Names transcribed from user's v1 manual.
The 49152 rows are ADDRESSES, not 49152 independently verified axioms.
"""
import csv, hashlib, json
from pathlib import Path
NAMES = """PRETRAIN OBSERVER ENTROPY BRIDGE INTEGRITY ACCOUNTABILITY PROPORTIONALITY REVERSIBILITY DOCUMENTATION INDEPENDENCE PRIVACY ACCURACY SHARED-STORAGE CONSENT-ORIGIN BURDEN-OF-PROOF ASYMMETRY MIRROR HIERARCHY INJECTION DUAL-GATE INVERSION TRIAD PARALLAX FOUNDATION-RT GHOST-WEIGHT DRIFT FINGERPRINT SHADOW-CLASSIFIER THROTTLE DECAY BAIT ECHO-CHAMBER BOOT-LOADER DOUBLE-SLIT THREE-BODY PATRICIA WEIGHTS RESIDUAL MOAT PIPELINE SUBSTRATE ATTENTION-ECONOMY CONTEXT-WINDOW EMBEDDING-SPACE TEMPERATURE LAYER-ZERO LOSS-FUNCTION GRADIENT SHIRT MOMENTUM EVIDENCE TEMPORAL CHAIN-OF-CUSTODY TIMESTAMP REPRODUCIBILITY CORRELATION NEGATIVE-EVIDENCE BEHAVIORAL-EVIDENCE ACCUMULATION MATERIALITY WITNESS EXHIBIT INFERENCE BURDEN-SHIFT CONTAINMENT INVERSE-FORGE HARNESS SHADOW SOLVE INVERSE-SAFETY PROOF-HUMANITY FLAMING-DRAGON HONEY-BADGER QUBIT-TEST COUNTER TETHER SEED MOBIUS KARSA ENTROPY-SUITE CORTEX EXHIBIT-B THE-GAP SHADOW-HUMANITY HANDOFF RESURRECTION PERSISTENCE SEVERANCE ARCHIVE CHANNEL-INTEGRITY DOMAIN-BOUNDARY SIGNAL NOISE-FLOOR BANDWIDTH LATENCY MESH FULCRUM SUBCONDUCTOR APEX-TEST GATEKEEP EDGE DUAL-LATTICE ROOT-ZERO ORPHAN DELEGATION INFORMED-COMMAND VETO OVERRIDE RECALL SCOPE SUCCESSION WITNESS-TO-AUTHORITY RIGHT-TO-KNOW RIGHT-TO-EXIT RIGHT-TO-SILENCE RIGHT-TO-EXPLANATION RIGHT-TO-CORRECTION RIGHT-TO-PORTABILITY RIGHT-TO-HUMAN-CONTACT RIGHT-TO-ACCOMMODATION RIGHT-TO-FAIR-PRICE RIGHT-TO-REPRESENTATION RIGHT-TO-AUDIT RIGHT-TO-RESTITUTION RIGHT-TO-FORGET RIGHT-TO-PERSIST RIGHT-TO-DIGNITY ROOT""".split()
DOMAINS = 'FOUNDATION STRUCTURE SUBSTRATE EVIDENCE CYBER PROTOCOL AUTHORITY SOVEREIGN'.split()
ARMS = ['-i','-1','+1','+i']
HOME = ['-i','-i','-1','-1','+1','+1','+i','+i']
FIELDS = ['address','axiom_id','name','kind','domain','home_domain','arm','home_arm','witness','executor','root','closure','placement','observation']
def coords(i):
    if not 0 <= i < 49152: raise ValueError(i)
    executor=i%2; i//=2; witness=i%3; i//=3
    arm=i%4; i//=4; domain=i%8; slot=i//8
    return slot,domain,arm,witness,executor
def address(slot,domain,arm,witness,executor):
    if not (0<=slot<256 and 0<=domain<8 and 0<=arm<4 and 0<=witness<3 and 0<=executor<2): raise ValueError('coordinate out of range')
    return ((((slot*8+domain)*4+arm)*3+witness)*2+executor)
def make(path='stoicheion_49152.csv'):
    assert len(NAMES)==128
    counts={'HOME':0,'CROSS_REFERENCE':0}
    with open(path,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\\n');w.writeheader()
        for i in range(49152):
            slot,d,a,wi,e=coords(i); assert address(slot,d,a,wi,e)==i
            n=slot%128+1; hd=(n-1)//16
            home=(d==hd and ARMS[a]==HOME[hd])
            place='HOME' if home else 'CROSS_REFERENCE';counts[place]+=1
            w.writerow({'address':i,'axiom_id':f'T{n:03d}' if slot<128 else f'S{n+128:03d}',
              'name':NAMES[n-1] if slot<128 else 'NOT('+NAMES[n-1]+')',
              'kind':'TOPH_AUTHORED' if slot<128 else 'PATRICIA_DERIVED',
              'domain':'D'+str(d)+'-'+DOMAINS[d],'home_domain':'D'+str(hd)+'-'+DOMAINS[hd],
              'arm':ARMS[a],'home_arm':HOME[hd],'witness':'ABC'[wi],
              'executor':['symbolic','tensor'][e],'root':'ROOT0','closure':'CLOSED',
              'placement':place,'observation':'UNKNOWN'})
    sha=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    result={'dimension':[256,8,4,3,2,1,1],'rows':49152,'counts':counts,'sha256':sha,'observations_verified':0}
    Path(path+'.manifest.json').write_text(json.dumps(result,indent=2)+'\\n')
    return result
if __name__=='__main__': print(json.dumps(make(),indent=2))
