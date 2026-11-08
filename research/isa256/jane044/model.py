"""JANE 044: proof-carrying transfer with independent hash-chain journals.

Classical, benign-peer, unkeyed-hash experiment. In-flight ownership is a
logical state, not physical wave transport or an authenticated signature.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, os, random

WAVE = '111222333444555555444333222111'
POSITIONS = 27
TERNARY = (-1, 0, 1)
A = (-3., .5, 2.)
B = (5., -.25, -7.)
F_A = tuple(map(float, WAVE[:27]))
F_B = tuple(map(float, WAVE[3:]))
GENESIS = '0' * 64
BASELINE = sum(x*x for x in (*F_A,*F_B,*A,*B))
# Four distinct signed payloads; neutral registers remain local.
PAYLOADS = {'A_MINUS': (-3., 'A','B', 'PLUS'), 'A_PLUS': (2., 'A','B','MINUS'),
            'B_MINUS': (5., 'B','A','PLUS'), 'B_PLUS': (-7.,'B','A','MINUS')}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',',':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


class AuditError(Exception):
    pass


@dataclass(frozen=True)
class Audit:
    valid: bool
    records: tuple
    reason: str = ''


class Journal:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def audit(self):
        records = []
        prev = GENESIS
        data = self.path.read_bytes()
        if data and not data.endswith(b'\n'):
            return Audit(False, tuple(records), 'TRUNCATED_TAIL')
        for idx, raw in enumerate(data.splitlines()):
            try:
                record = json.loads(raw)
            except (ValueError, UnicodeDecodeError):
                return Audit(False, tuple(records), 'INVALID_JSON')
            if not isinstance(record, dict) or set(record) != {'seq','prev','body','hash'}:
                return Audit(False, tuple(records), 'BAD_SHAPE')
            if record['seq'] != idx or record['prev'] != prev:
                return Audit(False, tuple(records), 'BROKEN_CHAIN')
            if not isinstance(record['body'],dict):
                return Audit(False, tuple(records), 'BAD_BODY')
            expected = digest({'seq':record['seq'],'prev':record['prev'],'body':record['body']})
            if record['hash'] != expected:
                return Audit(False, tuple(records), 'HASH_MISMATCH')
            records.append(record)
            prev = record['hash']
        return Audit(True, tuple(records))

    def append(self, body):
        audit = self.audit()
        if not audit.valid:
            raise AuditError(audit.reason)
        idx = len(audit.records)
        prev = audit.records[-1]['hash'] if idx else GENESIS
        row = {'seq':idx,'prev':prev,'body':body}
        row['hash'] = digest(row)
        with self.path.open('ab') as f:
            f.write((canonical(row)+'\n').encode('utf-8'))
            f.flush(); os.fsync(f.fileno())
        return row

    def body(self):
        a = self.audit()
        if not a.valid:raise AuditError(a.reason)
        return [x['body'] for x in a.records]


class Pair:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.logs = {k:Journal(self.folder / f'{k}.jsonl') for k in ('A','B')}

    def restart(self):return Pair(self.folder)

    def audit(self):return {k:j.audit() for k,j in self.logs.items()}

    def _events(self, who):return self.logs[who].body()

    def _find(self, who, kind, payload):
        return [e for e in self._events(who) if e.get('op')==kind and e.get('id')==payload]

    def stage(self, pid):
        value,sender,recipient,slot = PAYLOADS[pid]
        found = self._find(sender,'STAGE',pid)
        if found:return found[0]
        body={'op':'STAGE','id':pid,'value':value,'sender':sender,'recipient':recipient,'dest_slot':slot}
        self.logs[sender].append(body)
        return body

    def accept(self, pid):
        value,sender,recipient,_ = PAYLOADS[pid]
        stage = self._find(sender,'STAGE',pid)
        if not stage:return None
        existing = self._find(recipient,'ACCEPT',pid)
        if existing:return existing[0]
        body={'op':'ACCEPT','id':pid,'stage_hash':digest(stage[0]),'value':value}
        self.logs[recipient].append(body)
        return body

    def release(self, pid):
        value,sender,recipient,_ = PAYLOADS[pid]
        acc = self._find(recipient,'ACCEPT',pid)
        stage = self._find(sender,'STAGE',pid)
        if not stage or not acc or acc[0]['stage_hash']!=digest(stage[0]):return None
        old = self._find(sender,'RELEASE',pid)
        if old:return old[0]
        body={'op':'RELEASE','id':pid,'receipt_hash':digest(acc[0])}
        self.logs[sender].append(body)
        return body

    def finalize(self, pid):
        value,sender,recipient,_=PAYLOADS[pid]
        acc=self._find(recipient,'ACCEPT',pid)
        rel=self._find(sender,'RELEASE',pid)
        if not acc or not rel or rel[0]['receipt_hash']!=digest(acc[0]):return None
        existing=self._find(recipient,'FINAL',pid)
        if existing:return existing[0]
        body={'op':'FINAL','id':pid,'release_hash':digest(rel[0])}
        self.logs[recipient].append(body)
        return body

    def trace(self, pid):
        value,sender,recipient,_=PAYLOADS[pid]
        stage=self._find(sender,'STAGE',pid)
        accept=self._find(recipient,'ACCEPT',pid)
        release=self._find(sender,'RELEASE',pid)
        final=self._find(recipient,'FINAL',pid)
        if len(stage)>1 or len(accept)>1 or len(release)>1 or len(final)>1:
            return 'INVALID_DUPLICATE'
        if accept and (not stage or accept[0]['stage_hash']!=digest(stage[0])):
            return 'INVALID_RECEIPT'
        if release and (not accept or release[0]['receipt_hash']!=digest(accept[0])):
            return 'INVALID_RELEASE'
        if final and (not release or final[0]['release_hash']!=digest(release[0])):
            return 'INVALID_FINAL'
        if final:return 'RECEIVED'
        if release:return 'IN_FLIGHT'
        if accept:return 'PROVISIONAL'
        if stage:return 'STAGED'
        return 'SENDER'

    def accounting(self):
        reports=self.audit()
        if not all(v.valid for v in reports.values()):
            return {'valid':False, 'reason':{k:a.reason for k,a in reports.items() if not a.valid}}
        buckets={'sender':0.,'gap':0.,'receiver':0.}
        states={}
        for pid,(value,_,_,_) in PAYLOADS.items():
            state=self.trace(pid)
            states[pid]=state
            if state.startswith('INVALID'):return {'valid':False,'reason':state,'states':states}
            target='gap' if state=='IN_FLIGHT' else 'receiver' if state=='RECEIVED' else 'sender'
            buckets[target]+=value*value
        stable=sum(x*x for x in (*F_A,*F_B,A[1],B[1]))
        total=stable+sum(buckets.values())
        return {'valid':True,'states':states,'buckets':buckets,'stable':stable,
                'total':total,'closed':all(s=='RECEIVED' for s in states.values()),
                'all_proven':all(s=='RECEIVED' for s in states.values())}

    def drive(self, rng=None, loss=0, steps=200):
        if rng is None:rng=random.Random(0)
        for _ in range(steps):
            for pid in PAYLOADS:
                for op in (self.stage,self.accept,self.release,self.finalize):
                    if rng.random()>=loss:op(pid)
            result=self.accounting()
            if result.get('closed'):break
        return self.accounting()


def experiment(seed=1, loss=.2, steps=100):
    with TemporaryDirectory() as folder:
        p=Pair(folder)
        rng=random.Random(seed)
        p=p.restart()
        result=p.drive(rng,loss,steps)
        return {'closed':result.get('closed',False), 'valid':result['valid'],
                'states':result.get('states'), 'total':result.get('total'),
                'history':[len(p.logs[k].body()) for k in ('A','B')]}


def trial_table(n=100):
    out=[]
    for loss in (0,.1,.2,.4,1):
        runs=[experiment(seed=i+1044,loss=loss) for i in range(n)]
        out.append({'loss':loss,'trials':n,'closed':sum(x['closed'] for x in runs),
            'valid':sum(x['valid'] for x in runs),'mass_ok':sum(x['total']==BASELINE for x in runs)})
    return out

if __name__=='__main__':
    print(json.dumps({'baseline':BASELINE,'trials':trial_table()},indent=2))
