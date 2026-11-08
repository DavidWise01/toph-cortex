import unittest,tempfile
from model import *
class TestPeerRecovery(unittest.TestCase):
 def test_geometry(self):self.assertEqual(N,27)
 def test_ternary(self):self.assertEqual(TERNARY,(-1,0,1))
 def test_count(self):self.assertEqual(N+len(TERNARY),30)
 def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_norm(self):self.assertEqual(energy(A,B),741.3125)
 def test_recover(self):self.assertEqual(scenario(loss=0)["status"],"CLOSED")
 def test_doubt_without_copy(self):self.assertEqual(scenario("no_copy",loss=0)["status"],"IN_DOUBT")
 def test_permanent_partition(self):self.assertEqual(scenario("partition")["status"],"IN_DOUBT")
 def test_half_commit_norm(self):self.assertEqual(scenario("partial")["before"],802.3125)
 def test_half_commit_recover(self):self.assertEqual(scenario("partial",loss=0)["after"],741.3125)
 def test_abort(self):self.assertEqual(scenario("abort",loss=0)["status"],"ABORTED")
 def test_full_loss(self):self.assertEqual(scenario(loss=1)["status"],"IN_DOUBT")
 def test_repeat(self):self.assertEqual(scenario(seed=42),scenario(seed=42))
 def test_no_conflicting_decision(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.decide("COMMIT")
   with self.assertRaises(ValueError):p.decide("ABORT")
 def test_no_unlogged_seed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d)
   with self.assertRaises(ValueError):p.seed("left","COMMIT")
 def test_duplicate_apply(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.prepare();p.decide("COMMIT");p.seed("left","COMMIT")
   p.recover(retries=9);p.restart().recover(retries=9)
   self.assertEqual(sum(x["kind"]=="APPLIED" for x in p.left.log.rows()),1)
 def test_restart(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.prepare();p.decide("COMMIT");p.seed("left","COMMIT")
   self.assertEqual(p.restart().recover(),"CLOSED")
 def test_coordinator_disappears(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.prepare();p.decide("COMMIT");p.seed("left","COMMIT")
   p.coord.p.rename(p.coord.p.with_suffix(".missing"))
   self.assertEqual(p.recover(),"CLOSED")
 def test_original_memory(self):
  with tempfile.TemporaryDirectory() as d:self.assertEqual(Pair(d).left.register(),A)
 def test_energy_completed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Pair(d);p.prepare();p.decide("COMMIT");p.seed("left","COMMIT");p.recover()
   self.assertEqual(p.energy(),741.3125)
if __name__=="__main__":unittest.main()
