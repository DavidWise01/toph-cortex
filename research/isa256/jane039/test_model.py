"""Regression checks for the GitHub edition of JANE039. Run: python -m unittest -q"""
import tempfile,unittest
from model import *
class TestJANE039(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.p=Pair(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def test_geometry(self):self.assertEqual(N,27)
 def test_wave_length(self):self.assertEqual(len(WAVE),30)
 def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_initial_energy(self):self.assertEqual(norm(A,B),741.3125)
 def test_initial(self):self.assertEqual(self.p.status(),"UNDECIDED")
 def test_prepare(self):self.assertEqual(self.p.prepare(),("READY","READY"))
 def test_restart_prepared(self):
  self.p.prepare();self.assertEqual(self.p.restart().left.phase(),"PREPARED")
 def test_undecided_commit(self):self.assertEqual(self.p.left.commit(),"NACK")
 def test_commit(self):
  self.p.prepare();self.assertEqual(self.p.decide(),"COMMIT")
 def test_restart_decision(self):
  self.p.prepare();self.p.decide();self.assertEqual(self.p.restart().coord.decision(),"COMMIT")
 def test_conflicting_decision(self):
  self.p.prepare();self.p.decide()
  with self.assertRaises(ValueError):self.p.coord.decide("ABORT")
 def test_partial(self):
  self.p.prepare();self.p.decide();self.assertEqual(self.p.deliver((True,False)),"IN_DOUBT")
 def test_partial_energy(self):
  self.p.prepare();self.p.decide();self.p.deliver((True,False));self.assertEqual(self.p.energy(),802.3125)
 def test_reconnect(self):
  self.p.prepare();self.p.decide();self.p.deliver((True,False));self.assertEqual(self.p.restart().deliver(),"CLOSED")
 def test_closed_energy(self):
  self.p.prepare();self.p.decide();self.p.deliver();self.assertEqual(self.p.energy(),741.3125)
 def test_idempotent(self):
  self.p.prepare();self.p.decide();self.p.deliver(duplicates=10)
  self.p.restart().deliver(duplicates=10)
  self.assertEqual(len(self.p.left.j.entries()),2)
 def test_abort_if_not_ready(self):self.assertEqual(self.p.decide(),"ABORT")
 def test_abort_eventually(self):
  self.p.decide();self.assertEqual(self.p.deliver(),"ABORTED")
 def test_full_loss(self):self.assertEqual(simulate(loss=1)["status"],"IN_DOUBT")
 def test_recovery(self):self.assertEqual(simulate(loss=0)["status"],"CLOSED")
 def test_partition_blocks(self):
  self.assertEqual(simulate(loss=0,connected=False)["status"],"IN_DOUBT")
 def test_repeat(self):self.assertEqual(simulate(100,.2),simulate(100,.2))
 def test_all_counted(self):
  for row in trials(3):self.assertEqual(row["closed"]+row["aborted"]+row["in_doubt"],3)
 def test_original_fields(self):self.assertEqual((len(F1),len(F2)),(27,27))
if __name__=="__main__":unittest.main()
