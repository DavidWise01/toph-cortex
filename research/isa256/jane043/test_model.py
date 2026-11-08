import unittest,tempfile
from model import *
class Tests(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.p=Pair(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def test_positions(self):self.assertEqual(N,27)
 def test_wave_length(self):self.assertEqual(len(WAVE),30)
 def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_six_each(self):self.assertTrue(all(WAVE.count(str(i))==6 for i in range(1,6)))
 def test_three_labels(self):self.assertEqual(27+3,30)
 def test_payloads(self):self.assertEqual(len(PAYLOADS),4)
 def test_initial_energy(self):self.assertAlmostEqual(TOTAL,741.3125)
 def test_initial_conserved(self):self.assertEqual(self.p.energy_parts()['total'],TOTAL)
 def test_staging(self):self.p.stage_all();self.assertEqual(self.p.report()['staged'],4)
 def test_no_early_accept(self):self.assertFalse(self.p.accept('Aminus'))
 def test_accept(self):self.p.stage('Aminus');self.assertTrue(self.p.accept('Aminus'))
 def test_no_early_release(self):self.assertFalse(self.p.release('Aminus'))
 def test_release(self):self.p.stage('Aminus');self.p.accept('Aminus');self.assertTrue(self.p.release('Aminus'))
 def test_no_early_confirm(self):self.assertFalse(self.p.confirm('Aminus'))
 def test_confirm(self):self.p.stage('Aminus');self.p.accept('Aminus');self.p.release('Aminus');self.assertTrue(self.p.confirm('Aminus'))
 def test_idempotent_stage(self):self.p.stage('Aminus');self.p.stage('Aminus');self.assertEqual(len(self.p.records('A','Aminus')),1)
 def test_idempotent_accept(self):self.p.stage('Aminus');self.p.accept('Aminus');self.p.accept('Aminus');self.assertEqual(len(self.p.records('B','Aminus')),1)
 def test_idempotent_release(self):self.p.stage('Aminus');self.p.accept('Aminus');self.p.release('Aminus');self.p.release('Aminus');self.assertEqual(len(self.p.records('A','Aminus')),2)
 def test_idempotent_confirm(self):
  for op in ('stage','accept','release','confirm','confirm'):getattr(self.p,op)('Aminus')
  self.assertEqual(len(self.p.records('B','Aminus')),2)
 def test_staging_conserved(self):self.p.stage_all();self.assertEqual(self.p.energy_parts()['total'],TOTAL)
 def test_accept_conserved(self):self.p.stage_all();self.p.step_all('accept');self.assertEqual(self.p.energy_parts()['total'],TOTAL)
 def test_release_conserved(self):self.p.stage_all();self.p.step_all('accept');self.p.step_all('release');self.assertEqual(self.p.energy_parts()['total'],TOTAL)
 def test_confirm_conserved(self):
  self.p.stage_all();self.p.step_all('accept');self.p.step_all('release');self.p.step_all('confirm');self.assertEqual(self.p.energy_parts()['total'],TOTAL)
 def test_all_delivered(self):
  for op in ('stage','accept','release','confirm'):self.p.step_all(op)
  self.assertEqual(self.p.report()['completed'],4)
 def test_final_escrow_zero(self):
  for op in ('stage','accept','release','confirm'):self.p.step_all(op)
  self.assertEqual(self.p.energy_parts()['sender_escrow']+self.p.energy_parts()['receiver_escrow'],0)
 def test_restart(self):self.p.stage('Aminus');self.assertTrue(self.p.restart().has('A','Aminus','STAGED'))
 def test_restart_finish(self):
  self.p.stage_all();p=self.p.restart()
  for op in ('accept','release','confirm'):p.step_all(op)
  self.assertEqual(p.report()['completed'],4)
 def test_incomplete_partition(self):self.assertEqual(run(partition=True)['completed'],0)
 def test_partition_conserved(self):self.assertTrue(run(partition=True)['conserved'])
 def test_clean_complete(self):self.assertEqual(run(drop=0)['completed'],4)
 def test_clean_conserved(self):self.assertTrue(run(drop=0)['conserved'])
 def test_full_loss(self):self.assertEqual(run(drop=1)['completed'],0)
 def test_loss_conserved(self):self.assertTrue(run(drop=1)['conserved'])
 def test_reproducible(self):self.assertEqual(run(seed=15,drop=.4)['completed'],run(seed=15,drop=.4)['completed'])
 def test_local_uncertainty(self):
  self.p.stage('Aminus');self.p.accept('Aminus');self.assertIn('Aminus',self.p.local_view('B')['unconfirmed_accepts'])
 def test_owner_before_release(self):
  self.p.stage('Aminus');self.p.accept('Aminus');self.assertEqual(self.p.ownership('Aminus'),'A')
 def test_owner_after_release(self):
  self.p.stage('Aminus');self.p.accept('Aminus');self.p.release('Aminus');self.assertEqual(self.p.ownership('Aminus'),'B')
 def test_lost_journal(self):self.assertFalse(run(drop=0,missing_log=True)['lost_log_audit']['valid'])
 def test_invalid_loss(self):
  with self.assertRaises(ValueError):run(drop=2)
 def test_sweep_shape(self):self.assertEqual(len(sweep(2)),5)
 def test_all_lanes(self):self.assertEqual({x[-1] for x in PAYLOADS},{'minus','plus'})
if __name__=='__main__':unittest.main()
