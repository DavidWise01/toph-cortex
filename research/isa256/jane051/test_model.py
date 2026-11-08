import unittest
from dataclasses import replace
from model import *

class TestJANE051(unittest.TestCase):
    def test_positions(self):self.assertEqual(POS,27)
    def test_ternary(self):self.assertEqual(TERNARY,(-1,0,1))
    def test_30_counted(self):self.assertEqual(POS+len(TERNARY),30)
    def test_wave_len(self):self.assertEqual(len(WAVE),30)
    def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_wave_counts(self):self.assertEqual([WAVE.count(str(i)) for i in range(1,6)],[6]*5)
    def test_bad_value(self):
        with self.assertRaises(ValueError):Reading('a','r',0,2)
    def test_immutable(self):
        with self.assertRaises(Exception):replace(Reading('a','r',0,1),value=9)
    def test_no_readings(self):self.assertEqual(group_aware([])['status'],'INSUFFICIENT')
    def test_one_root(self):self.assertEqual(group_aware([Reading('a','r',0,1)])['status'],'INSUFFICIENT')
    def test_cloned_does_not_multiply(self):
        rs=[Reading('a','r',i,1) for i in range(50)]
        self.assertEqual(group_aware(rs)['roots'],1)
    def test_three_roots(self):
        rs=[Reading(str(i),str(i),0,1) for i in range(3)]
        self.assertEqual(group_aware(rs)['status'],'CORROBORATED')
    def test_two_roots(self):
        rs=[Reading(str(i),str(i),0,1) for i in range(2)]
        self.assertEqual(group_aware(rs)['status'],'INSUFFICIENT')
    def test_mixed_root(self):
        rs=[Reading('a','r',0,1),Reading('a','r',1,-1)]
        self.assertEqual(group_aware(rs)['status'],'CONFLICT')
    def test_conflicting_roots(self):
        rs=[Reading('a','a',0,1),Reading('b','b',0,-1),Reading('c','c',0,1)]
        self.assertEqual(group_aware(rs)['status'],'CONFLICT')
    def test_disagree_claim(self):
        rs=[Reading(str(i),str(i),0,-1) for i in range(3)]
        self.assertEqual(group_aware(rs)['status'],'CONFLICT')
    def test_conflict_preserved(self):
        rs=[Reading('a','a',0,1),Reading('b','b',0,-1)]
        self.assertEqual(len(rs),2)
        self.assertIsNone(group_aware(rs)['decision'])
    def test_naive_repeated_false(self):
        rs=[Reading('a','r',i,1) for i in range(9)]
        self.assertEqual(naive(rs),1)
    def test_group_aware_repeated_false(self):
        rs=[Reading('a','r',i,1) for i in range(9)]
        self.assertIsNone(group_aware(rs)['decision'])
    def test_three_colluding_roots_still_false(self):
        rs=[Reading(str(i),str(i),0,1) for i in range(3)]
        self.assertEqual(group_aware(rs)['decision'],1)
    def test_repeat_seed(self):self.assertEqual(trial(seed=42)['false_group'],trial(seed=42)['false_group'])
    def test_independent_count(self):self.assertEqual(len(trial(mode='independent')['readings']),27)
    def test_cloned_count(self):self.assertEqual(len(trial(mode='cloned')['readings']),9)
    def test_correlated_count(self):self.assertEqual(len(trial(mode='correlated')['readings']),27)
    def test_truth_hidden(self):
        rs=trial()['readings'];self.assertFalse(hasattr(rs[0],'truth'))
    def test_trial_binary(self):self.assertIn(trial()['false_group'],(0,1))
    def test_invalid_mode(self):
        with self.assertRaises(ValueError):trial(mode='nonsense')
    def test_invalid_repeat(self):
        with self.assertRaises(ValueError):trial(repeat=0)
    def test_invalid_error(self):
        with self.assertRaises(ValueError):trial(error=2)
    def test_batch_modes(self):self.assertEqual({r['mode'] for r in run_batch(5)},{'independent','cloned','correlated'})
    def test_trials(self):self.assertTrue(all(r['trials']==5 for r in run_batch(5)))
    def test_false_never_gt_trials(self):self.assertTrue(all(r['false_group']<=r['trials'] for r in run_batch(10)))
    def test_clone_always_abstain(self):self.assertEqual(run_batch(10)[1]['group_abstained'],10)
    def test_healthy_clone_always_abstain(self):self.assertEqual(healthy_batch(10)[1]['corroborated'],0)
    def test_independent_correct_can_pass(self):self.assertGreater(healthy_batch(100)[0]['corroborated'],0)
    def test_zero_error_independents(self):self.assertEqual(run_batch(10,error=0,shared_error=0)[0]['false_group'],0)
    def test_total_shared_failure(self):self.assertEqual(run_batch(10,error=0,shared_error=1)[2]['false_group'],10)
    def test_group_duplicate_reordering(self):
        rs=[Reading(str(i),str(i),0,1) for i in range(3)]
        self.assertEqual(group_aware(rs),group_aware(rs[::-1]))
    def test_group_no_mutation(self):
        rs=[Reading('a','r',0,1)];group_aware(rs);self.assertEqual(len(rs),1)
    def test_count_vs_source(self):
        rs=[Reading('a','r',i,1) for i in range(100)]
        self.assertEqual(group_aware(rs)['roots'],1)

if __name__=='__main__':unittest.main()
