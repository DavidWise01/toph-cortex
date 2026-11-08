"""JANE 043: distributed two-waldo ledger, one owner for each in-flight wave payload.
No central gap log; deterministic protocol simulation, not physical quantum tunneling.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json, os, random, copy

WAVE='111222333444555555444333222111'
N=27
A=(-3.0,.5,2.0)
B=(5.0,-.25,-7.0)
FIELD_A=tuple(map(float,WAVE[:27]))
FIELD_B=tuple(map(float,WAVE[3:]))
FIXED=sum(v*v for v in (*FIELD_A,*FIELD_B)) + A[1]**2+B[1]**2
PAYLOADS=(('Aminus','A','B',A[0],'plus'),('Aplus','A','B',A[2],'minus'),
          ('Bminus','B','A',B[0],'plus'),('Bplus','B','A',B[2],'minus'))
TOTAL=FIXED+sum(p[3]**2 for p in PAYLOADS)

class Journal:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.path.touch(exist_ok=True)
    def append(self,entry):
        # A modelled append+fsync atomic record: torn records and physical disk loss excluded.
        with self.path.open('a',encoding='utf8') as out:
            out.write(json.dumps(entry,sort_keys=True)+'\n');out.flush();os.fsync(out.fileno())
    def entries(self):return [json.loads(x) for x in self.path.read_text().splitlines() if x]

class Pair:
    def __init__(self,root):
        root=Path(root);self.root=root
        self.j={x:Journal(root/(x+'.jsonl')) for x in ('A','B')}
    def restart(self):return Pair(self.root)
    def records(self,peer,pid):return [r for r in self.j[peer].entries() if r['pid']==pid]
    def has(self,peer,pid,typ):return any(x['op']==typ for x in self.records(peer,pid))
    def payload(self,pid):
        for rec in PAYLOADS:
            if rec[0]==pid:return rec
        raise ValueError(pid)
    def stage(self,pid):
        _,src,dst,value,target=self.payload(pid)
        if not self.has(src,pid,'STAGED'):
            self.j[src].append(dict(pid=pid,op='STAGED',value=value,target=target))
        return True
    def accept(self,pid):
        _,src,dst,value,target=self.payload(pid)
        if not self.has(src,pid,'STAGED'):return False
        if not self.has(dst,pid,'ACCEPTED'):
            self.j[dst].append(dict(pid=pid,op='ACCEPTED',value=value,source=src))
        return True
    def release(self,pid):
        _,src,dst,value,target=self.payload(pid)
        if not self.has(dst,pid,'ACCEPTED'):return False
        if not self.has(src,pid,'RELEASED'):
            self.j[src].append(dict(pid=pid,op='RELEASED',ack_source=dst))
        return True
    def confirm(self,pid):
        _,src,dst,value,target=self.payload(pid)
        if not self.has(src,pid,'RELEASED'):return False
        if not self.has(dst,pid,'CONFIRMED'):
            self.j[dst].append(dict(pid=pid,op='CONFIRMED'))
        return True
    def stage_all(self):
        for pid,*_ in PAYLOADS:self.stage(pid)
    def step_all(self,stage):
        for pid,*_ in PAYLOADS:getattr(self,stage)(pid)
    def ownership(self,pid):
        _,src,dst,val,target=self.payload(pid)
        if self.has(src,pid,'RELEASED'):
            if not self.has(dst,pid,'ACCEPTED'):raise AssertionError('invalid release without acceptance')
            return dst
        return src
    def energy_parts(self):
        # Includes stable fields, local registers and sender-owned / receiver-owned escrow.
        origin_registers=0.;sender_escrow=0.;receiver_escrow=0.;delivered=0.
        for pid,src,dst,val,target in PAYLOADS:
            q=val*val
            if not self.has(src,pid,'STAGED'):origin_registers+=q
            elif not self.has(src,pid,'RELEASED'):sender_escrow+=q
            elif not self.has(dst,pid,'CONFIRMED'):receiver_escrow+=q
            else:delivered+=q
        return {'fixed':FIXED,'origin_registers':origin_registers,'sender_escrow':sender_escrow,
                'receiver_escrow':receiver_escrow,'delivered':delivered,
                'total':FIXED+origin_registers+sender_escrow+receiver_escrow+delivered}
    def audit(self):
        violations=[]
        for pid,src,dst,*_ in PAYLOADS:
            if self.has(dst,pid,'ACCEPTED') and not self.has(src,pid,'STAGED'):
                violations.append(pid+':accepted_without_source')
            if self.has(dst,pid,'CONFIRMED') and not self.has(src,pid,'RELEASED'):
                violations.append(pid+':confirmed_without_release')
        return {'valid':not violations,'violations':violations}
    def local_view(self,peer):
        # Important: local view cannot tell if a remote release was appended after ACK.
        own=[];unknown=[]
        for pid,src,dst,val,target in PAYLOADS:
            if src==peer:
                own.append(pid if not self.has(peer,pid,'RELEASED') else None)
            elif dst==peer:
                if self.has(peer,pid,'CONFIRMED'):own.append(pid)
                elif self.has(peer,pid,'ACCEPTED'):unknown.append(pid)
        return {'certain_owned':[p for p in own if p], 'unconfirmed_accepts':unknown}
    def report(self):
        return {'parts':self.energy_parts(),
                'completed':sum(self.has(dst,pid,'CONFIRMED') for pid,src,dst,*_ in PAYLOADS),
                'staged':sum(self.has(src,pid,'STAGED') for pid,src,dst,*_ in PAYLOADS),
                'released':sum(self.has(src,pid,'RELEASED') for pid,src,dst,*_ in PAYLOADS)}

def run(seed=43,drop=.2,rounds=40,partition=False,missing_log=False):
    if not 0<=drop<=1:raise ValueError('drop')
    rng=random.Random(seed)
    with TemporaryDirectory() as d:
        p=Pair(d);history=[]
        p.stage_all();history.append(dict(phase='STAGED',**p.report()))
        for tick in range(rounds):
            for pid,*_ in PAYLOADS:
                if not partition and rng.random()>=drop:p.accept(pid)
                if not partition and rng.random()>=drop:p.release(pid)
                if not partition and rng.random()>=drop:p.confirm(pid)
            if tick==1:p=p.restart()
            history.append(dict(phase='RETRY_'+str(tick),**p.report()))
            if p.report()['completed']==4:break
        lost=None
        if missing_log:
            p.j['A'].path.unlink()
            # A fresh Pair recreates absent local journal; information cannot be reconstructed.
            lost=Pair(d).audit()
        return {'completed':p.report()['completed'],'conserved':all(abs(x['parts']['total']-TOTAL)<1e-9 for x in history),
                'energy_total':TOTAL,'lost_log_audit':lost,'history':history}

def sweep(trials=100):
    return [{'drop':v,'closed':sum(run(seed=2000+i,drop=v)['completed']==4 for i in range(trials)),
             'conserved':sum(run(seed=2000+i,drop=v)['conserved'] for i in range(trials))}
             for v in (0,.1,.2,.4,1)]
if __name__=='__main__':print(json.dumps(sweep(),indent=2))
