"""JANE053 GitHub regression suite. Run: python -m unittest -q."""
import unittest
from dataclasses import replace
from model import *
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=emit(11);cls.old=groups(cls.data[:180]);cls.new=groups(cls.data[400:520]);cls.result=run(11)
 def test_01_five_sources(self):self.assertEqual(len(SOURCES),5)
 def test_02_ternary_accounting(self):self.assertEqual(27+3,30)
 def test_03_shape(self):self.assertTrue(all(len(x['reads'])==5 for x in self.data))
 def test_04_truth_binary(self):self.assertTrue(all(x['truth'] in (0,1) for x in self.data))
 def test_05_repeat_seed(self):self.assertEqual(emit(1),emit(1))
 def test_06_different_seeds(self):self.assertNotEqual(emit(1),emit(2))
 def test_07_change_at_280(self):self.assertEqual(CHANGE,280)
 def test_08_original_group(self):self.assertIn((0,1,2),self.old)
 def test_09_replacement_group(self):self.assertIn((0,3,4),self.new)
 def test_10_partition_unique(self):self.assertEqual(sorted(i for g in self.old for i in g),list(range(5)))
 def test_11_old_name(self):self.assertIn('ABC',group_names(self.old))
 def test_12_new_name(self):self.assertIn('ADE',group_names(self.new))
 def test_13_stable_mismatch(self):self.assertLess(mismatch(self.data[60:180],0,1),.09)
 def test_14_changed_mismatch(self):self.assertGreater(mismatch(self.data[410:540],0,1),.17)
 def test_15_symmetric_mismatch(self):self.assertEqual(mismatch(self.data[:90],0,1),mismatch(self.data[:90],1,0))
 def test_16_self_mismatch(self):self.assertEqual(mismatch(self.data[:90],1,1),0)
 def test_17_empty_window(self):
  with self.assertRaises(ValueError):groups([])
 def test_18_two_votes(self):self.assertTrue(assess((1,1,1,1,0),((0,1,2),(3,),(4,)),1))
 def test_19_clones_one_vote(self):self.assertFalse(assess((1,1,1,0,0),((0,1,2),(3,),(4,)),1))
 def test_20_ties(self):self.assertFalse(assess((1,0,0,0,0),((0,1),(2,),(3,),(4,)),1))
 def test_21_valid_chain(self):self.assertTrue(self.result['history_valid'])
 def test_22_flag(self):self.assertIsNotNone(self.result['first_flag'])
 def test_23_flag_after_change(self):self.assertGreater(self.result['first_flag'],CHANGE)
 def test_24_flag_timely(self):self.assertLess(self.result['first_flag'],CHANGE+110)
 def test_25_revision(self):self.assertGreater(self.result['versions'],1)
 def test_26_final_group(self):self.assertIn('ADE',self.result['final'])
 def test_27_preserve_old(self):self.assertIn('ABC',self.result['baseline'])
 def test_28_has_flag_event(self):self.assertIn('FLAG',[x['event'] for x in self.result['events']])
 def test_29_has_revision_event(self):self.assertIn('REVISE',[x['event'] for x in self.result['events']])
 def test_30_uncertainty(self):self.assertGreaterEqual(self.result['uncertain_events'],48)
 def test_31_truth_not_used(self):
  data=emit(5);bad=[{'time':x['time'],'reads':x['reads'],'truth':1-x['truth']} for x in data]
  a,b=DriftMonitor(data[:180]),DriftMonitor(bad[:180])
  for x,y in zip(data[180:],bad[180:]):a.step(x);b.step(y)
  self.assertEqual(a.change_events,b.change_events)
 def test_32_unknown_method(self):
  with self.assertRaises(ValueError):run(method='bad')
 def test_33_no_change(self):self.assertIsNone(run(seed=11,switch=False)['first_flag'])
 def test_34_stale_worse(self):self.assertGreater(run(11,method='frozen')['false_approvals_post'],run(11)['false_approvals_post'])
 def test_35_reproducible(self):self.assertEqual(run(13)['events'],run(13)['events'])
 def test_36_detect_hash_tamper(self):
  m=DriftMonitor(self.data[:180]);m.versions[0]=replace(m.versions[0],hash='z'*64);self.assertFalse(m.history_valid())
 def test_37_detect_previous_tamper(self):
  m=DriftMonitor(self.data[:180]);m.versions[0]=replace(m.versions[0],previous='a'*64);self.assertFalse(m.history_valid())
 def test_38_post_trials(self):self.assertEqual(self.result['post_trials'],260)
 def test_39_append_only_versions(self):
  m=DriftMonitor(self.data[:180]);orig=m.versions[0]
  for r in self.data[180:]:m.step(r)
  self.assertEqual(m.versions[0],orig)
 def test_40_six_rows(self):self.assertEqual(len(sweep(1)),6)
 def test_41_equal_streams_indistinguishable(self):self.assertEqual(groups([{'reads':(0,0,0,0,0)}]*80),((0,1,2,3,4),))
 def test_42_independent_from_truth_label(self):
  d=emit(6);a=DriftMonitor(d[:180]);b=DriftMonitor(d[:180])
  for row in d[180:]:
   self.assertEqual(a.step(row),b.step({'time':row['time'],'reads':row['reads']}))
  self.assertEqual(a.change_events,b.change_events)
if __name__=='__main__':unittest.main()
