import unittest
from model import *
class JANE050Tests(unittest.TestCase):
 def test_geometry(self):self.assertEqual(N,27)
 def test_states(self):self.assertEqual(TERNARY,(-1,0,1))
 def test_thirty(self):self.assertEqual(N+len(TERNARY),30)
 def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_len_wave(self):self.assertEqual(len(WAVE),30)
 def test_six_each(self):self.assertTrue(all(WAVE.count(str(i))==6 for i in range(1,6)))
 def test_seam(self):self.assertIn('27->27.5->1',GEOMETRY)
 def test_sign_positive(self):self.assertTrue(authentic(sign(1,10,b'key'),b'key'))
 def test_sign_wrong_key(self):self.assertFalse(authentic(sign(1,10,b'bad'),b'key'))
 def test_sign_wrong_epoch(self):self.assertNotEqual(sign(1,10,b'key').signature,sign(1,11,b'key').signature)
 def test_sign_wrong_value(self):self.assertNotEqual(sign(1,10,b'key').signature,sign(-1,10,b'key').signature)
 def test_clean(self):self.assertEqual(experiment()['status'],'CORROBORATED')
 def test_clean_correct(self):self.assertFalse(experiment()['false_corroboration'])
 def test_bad_claim_key(self):self.assertEqual(experiment(forge=True)['status'],'INVALID_SIGNATURE')
 def test_stolen_key_wrong_claim(self):self.assertEqual(experiment(forge=True,stolen_key=True)['status'],'CONFLICT')
 def test_wrong_sensor(self):self.assertEqual(experiment(sensor_flip=True)['status'],'CONFLICT')
 def test_joint_false(self):self.assertTrue(experiment(joint=True,stolen_key=True)['false_corroboration'])
 def test_joint_status(self):self.assertEqual(experiment(joint=True,stolen_key=True)['status'],'CORROBORATED')
 def test_missing_sensor(self):self.assertEqual(experiment(missing_sensor=True)['status'],'INSUFFICIENT')
 def test_rollback(self):self.assertEqual(experiment(epoch=9)['status'],'ROLLBACK')
 def test_invalid_sensor(self):self.assertEqual(classify(sign(1,10,b'k'),4,b'k'),'INVALID_SENSOR')
 def test_explicit_zero(self):self.assertEqual(classify(sign(0,10,b'k'),0,b'k'),'CORROBORATED')
 def test_signed_zero_disagree(self):self.assertEqual(classify(sign(0,10,b'k'),-1,b'k'),'CONFLICT')
 def test_stale_and_missing(self):self.assertEqual(classify(sign(1,8,b'k'),None,b'k'),'ROLLBACK')
 def test_invalid_precedes_sensor(self):self.assertEqual(classify(sign(1,10,b'wrong'),1,b'right'),'INVALID_SIGNATURE')
 def test_bad_pin(self):self.assertEqual(classify(sign(1,10,b'k'),1,b'k',11),'ROLLBACK')
 def test_no_pin_effect(self):self.assertEqual(classify(sign(1,10,b'k'),1,b'k',0),'CORROBORATED')
 def test_trials_accounting(self):
  c=trial_batch(50)['counts'];self.assertEqual(c['CORROBORATED']+c['CONFLICT'],50)
 def test_repeat(self):self.assertEqual(trial_batch(seed=9),trial_batch(seed=9))
 def test_no_errors(self):
  r=trial_batch(50,claim_error=0,sensor_error=0)
  self.assertEqual(r['counts']['true_corroboration'],50)
 def test_always_joint_failure(self):
  r=trial_batch(50,claim_error=0,sensor_error=0,common_error=1)
  self.assertEqual(r['counts']['false_corroboration'],50)
 def test_independent_error_has_conflicts(self):
  r=trial_batch(1000,claim_error=.2,sensor_error=.2,common_error=0)
  self.assertGreater(r['counts']['CONFLICT'],0)
 def test_joint_increases_false(self):
  r0=trial_batch(1000,common_error=0)['counts']['false_corroboration']
  r1=trial_batch(1000,common_error=.2)['counts']['false_corroboration']
  self.assertGreater(r1,r0)
 def test_key_is_not_truth(self):
  self.assertNotEqual(experiment(forge=True,stolen_key=True)['status'],'INVALID_SIGNATURE')
 def test_conflict_not_ascribed(self):
  self.assertEqual(experiment(sensor_flip=True)['status'],experiment(forge=True,stolen_key=True)['status'])
 def test_truth_not_input(self):
  import inspect
  self.assertNotIn('truth',inspect.signature(classify).parameters)
 def test_scenarios(self):self.assertEqual(len(scenarios()),7)
 def test_observation_absent(self):self.assertIsNone(experiment(missing_sensor=True)['observed'])
 def test_other_truth(self):self.assertEqual(experiment(truth=-1)['status'],'CORROBORATED')
 def test_no_overclaim(self):self.assertNotIn('VERIFIED_TRUE',{experiment()['status']})
if __name__=='__main__':unittest.main()
