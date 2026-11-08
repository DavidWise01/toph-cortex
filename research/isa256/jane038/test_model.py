import unittest
from model import *
class Test038(unittest.TestCase):
    def test_shape(self): self.assertEqual(N,27)
    def test_palindrome(self): self.assertEqual(WAVE,WAVE[::-1])
    def test_wave_30(self): self.assertEqual(len(WAVE),30)
    def test_ternary_accounting(self): self.assertEqual(N+3,30)
    def test_sixfold(self): self.assertTrue(all(WAVE.count(str(k))==6 for k in range(1,6)))
    def test_baseline_energy(self): self.assertEqual(energy(A0,B0),741.3125)
    def test_prepare(self): self.assertTrue(Waldo('a',list(A0)).prepare('x'))
    def test_unprepared_commit(self): self.assertEqual(Waldo('a',list(A0)).commit('x',B0),'NOT_PREPARED')
    def test_idempotent_prepare(self):
        w=Waldo('a',list(A0));w.prepare('x');w.prepare('x');self.assertEqual(len(w.prepared),1)
    def test_idempotent_commit(self):
        w=Waldo('a',list(A0));w.prepare('x');self.assertEqual(w.commit('x',B0),'APPLIED')
        r=tuple(w.register);self.assertEqual(w.commit('x',B0),'DUPLICATE');self.assertEqual(tuple(w.register),r)
    def test_neutral_unchanged(self):
        w=Waldo('a',list(A0));w.prepare('x');w.commit('x',B0);self.assertEqual(w.register[1],A0[1])
    def test_abort_uncommitted(self):
        w=Waldo('a',list(A0));w.prepare('x');self.assertTrue(w.abort('x'));self.assertFalse(w.prepare('x'))
    def test_cannot_abort_committed(self):
        w=Waldo('a',list(A0));w.prepare('x');w.commit('x',B0);self.assertFalse(w.abort('x'))
    def test_clean_close(self):
        r=acknowledged(seed=5,loss=0,duplicate=0);self.assertEqual(r['state'],'CLOSED')
    def test_clean_exact_once(self):
        r=acknowledged(seed=5,loss=0,duplicate=0);self.assertTrue(r['exact_once'])
    def test_clean_energy(self):
        r=acknowledged(seed=5,loss=0,duplicate=0);self.assertEqual(r['energy'],r['energy_start'])
    def test_clean_both_apply(self):
        r=acknowledged(seed=5,loss=0,duplicate=0);self.assertEqual((r['applied_a'],r['applied_b']),(1,1))
    def test_duplicate_delivery(self):
        r=acknowledged(seed=5,loss=0,duplicate=1);self.assertEqual(r['state'],'CLOSED')
    def test_duplicate_exact_once(self):
        r=acknowledged(seed=5,loss=0,duplicate=1);self.assertEqual((r['applied_a'],r['applied_b']),(1,1))
    def test_complete_drop_abort(self):
        r=acknowledged(seed=5,loss=1);self.assertEqual(r['state'],'ABORTED')
    def test_complete_drop_preserves(self):
        r=acknowledged(seed=5,loss=1);self.assertEqual(r['registers'],(A0,B0))
    def test_partition_in_doubt(self):
        r=acknowledged(seed=5,loss=0,permanent_partition=True);self.assertEqual(r['state'],'IN_DOUBT')
    def test_partition_energy_not_guaranteed(self):
        r=acknowledged(seed=5,loss=0,permanent_partition=True);self.assertNotEqual(r['energy'],r['energy_start'])
    def test_crash_in_doubt(self):
        r=acknowledged(seed=5,loss=0,crash_after_one_commit=True);self.assertEqual(r['state'],'IN_DOUBT')
    def test_zero_loss_naive(self): self.assertTrue(naive(seed=5,loss=0,duplicate=0)['matches_one_swap'])
    def test_naive_duplicate_failure(self): self.assertFalse(naive(seed=5,loss=0,duplicate=1)['matches_one_swap'])
    def test_checksum_corruption_discard(self):
        r=acknowledged(seed=5,loss=0,corruption=1);self.assertEqual(r['state'],'ABORTED')
    def test_fault_repeatability(self):
        self.assertEqual(acknowledged(seed=42,loss=.2,duplicate=.2),acknowledged(seed=42,loss=.2,duplicate=.2))
    def test_fault_link_counts(self):
        f=FaultLink(random.Random(3),0,1,0);self.assertEqual(len(f.send('PREPARE','x')),2);self.assertEqual(f.duplicates,1)
    def test_batch_totals(self):
        for r in sweep(10):self.assertEqual(r['protocol_closed']+r['protocol_aborted']+r['protocol_in_doubt'],10)
    def test_naive_energy(self):
        for i in range(10):self.assertEqual(naive(i,duplicate=1)['energy'],741.3125)
    def test_durable_id_in_process(self):
        w=Waldo('a',list(A0));w.prepare('tx');w.commit('tx',B0);self.assertEqual(w.commit('tx',B0),'DUPLICATE')
if __name__=='__main__':unittest.main()
