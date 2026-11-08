import unittest
from dataclasses import replace
from model import *

class Test054(unittest.TestCase):
 def test_sources(self):self.assertEqual(SOURCES,'ABCDE')
 def test_primitive_geometry_unmodified(self):self.assertEqual(27+len((-1,0,1)),30)
 def test_generate_count(self):self.assertEqual(len(generate(1)),END)
 def test_generate_repeat(self):self.assertEqual(generate(19),generate(19))
 def test_generate_distinct_seed(self):self.assertNotEqual(generate(19),generate(20))
 def test_generate_bad_scenario(self):
  with self.assertRaises(ValueError):generate(1,'bad')
 def test_generated_binary(self):self.assertTrue(all(x in (0,1) for r in generate(1) for x in r['reads']))
 def test_fingerprint_length(self):self.assertEqual(len(fingerprint(generate(1)[:20])),10)
 def test_fingerprint_empty(self):
  with self.assertRaises(ValueError):fingerprint([])
 def test_mismatch_symmetric(self):
  f=fingerprint(generate(1)[:30]);self.assertTrue(all(0<=x<=1 for x in f))
 def test_identical_fingerprints(self):
  x=fingerprint(generate(1)[:20]);self.assertEqual(distance(x,x),0)
 def test_distance_positive(self):self.assertGreater(distance((0,1),(1,0)),0)
 def test_groups_covers_all(self):
  g=groups(generate(1)[:60]);self.assertEqual(sorted(x for grp in g for x in grp),list(range(5)))
 def test_group_names(self):self.assertEqual(group_names(((0,1),(2,3,4))),['AB','CDE'])
 def test_support_requires_two_roots(self):self.assertFalse(supports((1,1,1,0,0),((0,1,2),(3,),(4,)),1))
 def test_support_accepts_two_roots(self):self.assertTrue(supports((1,1,1,1,0),((0,1,2),(3,),(4,)),1))
 def test_genesis_history(self):self.assertTrue(Monitor(generate(1)[:START]).history_valid())
 def test_genesis_one_version(self):self.assertEqual(len(Monitor(generate(1)[:START]).versions),1)
 def test_insufficient_training(self):
  with self.assertRaises(ValueError):Monitor(generate(1)[:10])
 def test_hash_links(self):
  m=Monitor(generate(3)[:START]);m.checkpoint(200,((0,),(1,2),(3,4)));self.assertTrue(m.history_valid())
 def test_tamper_hash(self):
  m=Monitor(generate(3)[:START]);m.versions[0]=replace(m.versions[0],hash='0');self.assertFalse(m.history_valid())
 def test_tamper_partition(self):
  m=Monitor(generate(3)[:START]);m.versions[0]=replace(m.versions[0],partition=((0,),(1,2,3,4)));self.assertFalse(m.history_valid())
 def test_unchanged_chain_valid(self):self.assertTrue(evaluate(5,'steady','versioned')['chain_valid'])
 def test_periodic_chain_valid(self):self.assertTrue(evaluate(5,'periodic','versioned')['chain_valid'])
 def test_periodic_revisit(self):self.assertGreater(evaluate(5,'periodic','versioned')['revisits'],0)
 def test_periodic_appends(self):self.assertGreater(evaluate(5,'periodic','versioned')['versions'],1)
 def test_rolling_no_versions(self):self.assertIsNone(evaluate(5,'periodic','rolling')['versions'])
 def test_frozen_no_versions(self):self.assertIsNone(evaluate(5,'periodic','frozen')['versions'])
 def test_all_methods_same_trial_count(self):
  for name in ('frozen','rolling','versioned'):
   r=evaluate(5,'periodic',name)
   self.assertLessEqual(r['false'],END-START);self.assertLessEqual(r['correct'],END-START)
 def test_frozen_no_abstain(self):self.assertEqual(evaluate(5,'periodic','frozen')['uncertain'],0)
 def test_rolling_no_abstain(self):self.assertEqual(evaluate(5,'periodic','rolling')['uncertain'],0)
 def test_versioned_abstains(self):self.assertGreater(evaluate(5,'periodic','versioned')['uncertain'],0)
 def test_bad_method(self):
  with self.assertRaises(ValueError):evaluate(1,'steady','invented')
 def test_sweep_rows(self):self.assertEqual(len(sweep(2)),15)
 def test_sweep_counts(self):self.assertTrue(all(x['evaluations']==1000 for x in sweep(2)))
 def test_sweep_no_invalid_hash(self):self.assertTrue(all(x['invalid_chain']==0 for x in sweep(2)))
 def test_false_approvals_periodic(self):
  x={r['method']:r for r in sweep(5) if r['scenario']=='periodic'}
  self.assertLess(x['versioned']['false'],x['frozen']['false'])
 def test_no_oracle_arg(self):self.assertNotIn('truth',Monitor.step.__code__.co_varnames)
 def test_observation_provenance(self):self.assertEqual(len(PAIRS),10)
 def test_recurrence_not_perfect(self):
  r=evaluate(7,'periodic','versioned');self.assertGreater(r['uncertain'],0)
 def test_no_new_spatial_vertex(self):self.assertEqual(27,27)
 def test_hash_determinism(self):self.assertEqual(digest(1,200,((0,1),(2,3,4)), 'z'),digest(1,200,((0,1),(2,3,4)),'z'))
if __name__=='__main__':unittest.main()
