import unittest,tempfile
from model import *
class Tests(unittest.TestCase):
 def test_27(self):self.assertEqual(N,27)
 def test_ternary(self):self.assertEqual(MODES,(-1,0,1))
 def test_30(self):self.assertEqual(N+len(MODES),30)
 def test_wave(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_six_each(self):self.assertTrue(all(WAVE.count(str(i))==6 for i in range(1,6)))
 def test_energy(self):self.assertEqual(energy(A,B),741.3125)
 def test_commit(self):self.assertEqual(simulate(loss=0)['state'],'CLOSED')
 def test_abort(self):self.assertEqual(simulate(loss=0,case='YES_NO')['state'],'ABORTED')
 def test_partition(self):self.assertEqual(simulate(case='PARTITION')['state'],'IN_DOUBT')
 def test_loss(self):self.assertEqual(simulate(loss=1)['state'],'IN_DOUBT')
 def test_half_energy(self):self.assertNotEqual(simulate(case='HALF',loss=1)['partial_energy'],741.3125)
 def test_repaired(self):self.assertEqual(simulate(case='HALF',loss=0)['final_energy'],741.3125)
 def test_deterministic(self):self.assertEqual(simulate(11,.3),simulate(11,.3))
 def test_restart(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.vote();p.communicate();p.apply();self.assertEqual(p.restart().state(),'CLOSED')
 def test_no_unilateral(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.vote();self.assertFalse(p.minus.apply())
 def test_no_central_decider(self):
  with tempfile.TemporaryDirectory() as d:self.assertFalse(hasattr(Pair(d),'coordinator'))
 def test_vote_immutable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.minus.cast('YES')
   with self.assertRaises(ValueError):p.minus.cast('NO')
 def test_duplicate_apply(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.vote();p.communicate();p.apply();p.apply()
   self.assertEqual(len([e for e in p.minus.events() if e['event']=='APPLY']),1)
 def test_immutable_peer_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.minus.receive('YES');self.assertFalse(p.minus.receive('NO'))
 def test_invalid(self):
  with self.assertRaises(ValueError):simulate(loss=1.2)
if __name__=='__main__':unittest.main()
