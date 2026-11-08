"""JANE050: signed claim against an independent local ternary observation.
Synthetic classical signals; authenticated source is not proof of truth.
"""
import hashlib,hmac,json,random
from dataclasses import dataclass
N=27
TERNARY=(-1,0,1)
WAVE='111222333444555555444333222111'
GEOMETRY='{brace[box(cell())]} / {-()+} / 27->27.5->1'
@dataclass(frozen=True)
class Claim:
    asserted:int
    epoch:int
    signature:str
def sign(asserted,epoch,key):
    msg=f'{epoch}:{asserted}'.encode()
    return Claim(asserted,epoch,hmac.new(key,msg,hashlib.sha256).hexdigest())
def authentic(claim,key):
    return hmac.compare_digest(sign(claim.asserted,claim.epoch,key).signature,claim.signature)
def classify(claim,observed,key,pinned_epoch=10):
    if not authentic(claim,key):return 'INVALID_SIGNATURE'
    if claim.epoch<pinned_epoch:return 'ROLLBACK'
    if observed is None:return 'INSUFFICIENT'
    if observed not in TERNARY:return 'INVALID_SENSOR'
    return 'CORROBORATED' if claim.asserted==observed else 'CONFLICT'
def experiment(truth=1,forge=False,sensor_flip=False,joint=False,
               missing_sensor=False,stolen_key=False,pin=10,epoch=10):
    key=b'jane-050-pinned-secret-not-production'
    wrong_claim=forge or joint
    wrong_sensor=sensor_flip or joint
    asserted=-truth if wrong_claim else truth
    obs=None if missing_sensor else (-truth if wrong_sensor else truth)
    signing_key=key if stolen_key or not wrong_claim else b'untrusted-signing-key'
    claim=sign(asserted,epoch,signing_key)
    outcome=classify(claim,obs,key,pin)
    return dict(truth=truth,claim=asserted,observed=obs,status=outcome,
       claim_correct=asserted==truth,
       sensor_correct=obs==truth if obs is not None else None,
       false_corroboration=outcome=='CORROBORATED' and asserted!=truth)
def trial_batch(trials=1000,seed=50,claim_error=.08,sensor_error=.08,common_error=0):
    rng=random.Random(seed)
    counters=dict.fromkeys(('CORROBORATED','CONFLICT','INVALID_SIGNATURE','ROLLBACK',
       'INSUFFICIENT','INVALID_SENSOR','false_corroboration','true_corroboration','caught_wrong_claim'),0)
    key=b'jane-050-test-key'
    for _ in range(trials):
        truth=rng.choice((-1,1))
        shared=rng.random()<common_error
        wrong_claim=shared or rng.random()<claim_error
        wrong_sensor=shared or rng.random()<sensor_error
        asserted=-truth if wrong_claim else truth
        obs=-truth if wrong_sensor else truth
        status=classify(sign(asserted,10,key),obs,key)
        counters[status]+=1
        counters['false_corroboration']+=int(status=='CORROBORATED' and asserted!=truth)
        counters['true_corroboration']+=int(status=='CORROBORATED' and asserted==truth)
        counters['caught_wrong_claim']+=int(status=='CONFLICT' and asserted!=truth)
    return dict(trials=trials,claim_error=claim_error,sensor_error=sensor_error,
                shared_error=common_error,counts=counters)
def scenarios():
    return dict(clean=experiment(),valid_wrong_claim=experiment(forge=True,stolen_key=True),
       bad_signature=experiment(forge=True),bad_sensor=experiment(sensor_flip=True),
       both_wrong_agree=experiment(joint=True,stolen_key=True),
       missing_sensor=experiment(missing_sensor=True),rolled_back=experiment(epoch=9))
if __name__=='__main__':
    print(json.dumps(dict(scenarios=scenarios(),
       batches=[trial_batch(common_error=x) for x in (0,.05,.2)]),indent=2))
