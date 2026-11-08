import unittest
from model import *
class TestJane052(unittest.TestCase):
    def setUp(self):
        self.train,self.test=generate(seed=7,train=200,test=100)
        self.learner=Learner().fit(self.train)
    def test_geometry(self):self.assertEqual(N_PATH,27)
    def test_ternary(self):self.assertEqual(TERNARY,(-1,0,1))
    def test_30_count(self):self.assertEqual(N_PATH+len(TERNARY),30)
    def test_wave(self):self.assertEqual(len(WAVE),30)
    def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
    def test_sixfold(self):self.assertTrue(all(WAVE.count(str(k))==6 for k in range(1,6)))
    def test_waldo(self):self.assertEqual(WALDOS,'{-()+}')
    def test_sources(self):self.assertEqual(len(SOURCES),5)
    def test_train_length(self):self.assertEqual(len(self.train),200)
    def test_holdout_length(self):self.assertEqual(len(self.test),100)
    def test_sample_shape(self):self.assertEqual(len(self.train[0][0].readings),5)
    def test_training_truth_not_used(self):
        rewritten=[(s,1-truth) for s,truth in self.train]
        a=Learner().fit(rewritten)
        self.assertEqual(a.groups,self.learner.groups)
        self.assertEqual(a.similarities,self.learner.similarities)
    def test_clone_group(self):self.assertIn(('A','B','C'),self.learner.groups)
    def test_other_sources_separate(self):self.assertIn(('D',),self.learner.groups)
    def test_other_source_e(self):self.assertIn(('E',),self.learner.groups)
    def test_pair_identical(self):self.assertEqual(self.learner.similarities[('A','B')],1)
    def test_pair_unrelated(self):self.assertLess(self.learner.similarities[('A','D')],.97)
    def test_no_training_data(self):
        with self.assertRaises(ValueError):Learner().fit([])
    def test_short_training(self):
        with self.assertRaises(ValueError):Learner().fit(self.train[:10])
    def test_invalid_probability(self):
        with self.assertRaises(ValueError):generate(clone_error=-.1)
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):Learner(threshold=.1)
    def test_fit_required(self):
        with self.assertRaises(ValueError):Learner().vote(self.test[0][0],1)
    def test_missing_sources(self):
        bad=[Sample(i,(('A',1),)) for i in range(50)]
        with self.assertRaises(ValueError):Learner().fit(bad)
    def test_ordinary_vote(self):
        s=Sample(0,tuple(zip(SOURCES,(0,0,0,1,1))))
        self.assertEqual(naive_vote(s,0),'ACCEPT')
    def test_dependency_vote_refuses_clone_majority(self):
        s=Sample(0,tuple(zip(SOURCES,(0,0,0,1,1))))
        self.assertEqual(self.learner.vote(s,0),'REJECT')
    def test_dependency_vote_truth(self):
        s=Sample(0,tuple(zip(SOURCES,(0,0,0,1,1))))
        self.assertEqual(self.learner.vote(s,1),'ACCEPT')
    def test_holdout_disjoint(self):self.assertTrue(max(s.event for s,_ in self.train)<min(s.event for s,_ in self.test))
    def test_repeatable(self):self.assertEqual(generate(seed=1),generate(seed=1))
    def test_different_seeds(self):self.assertNotEqual(generate(seed=1)[0],generate(seed=2)[0])
    def test_evaluation(self):
        r=evaluate(self.train,self.test)
        self.assertEqual(r['trials'],100)
        self.assertLess(r['learned_false'],r['naive_false'])
    def test_metrics_bounds(self):
        r=evaluate(self.train,self.test)
        self.assertTrue(all(0<=r[k]<=100 for k in ('naive_false','learned_false','naive_true','learned_true')))
    def test_perfect_sources_ambiguity(self):
        a,b=generate(seed=39,independent_error=0,clone_error=0,train=200,test=100)
        learner=Learner().fit(a)
        self.assertEqual(len(learner.groups),1)
        self.assertEqual(evaluate(a,b)['learned_true'],0)
    def test_drift_baseline(self):
        r=replicate(5,100,100,drift=True)
        self.assertEqual(r['samples'],500)
    def test_no_claim_of_causality(self):self.assertIn('does not establish',self.learner.warning)
    def test_2pct_diff(self):
        r=replicate(3,150,100,clone_jitter=.02)
        self.assertEqual(r['samples'],300)
    def test_scenario_keys(self):
        r=scenarios()
        self.assertEqual(set(r),{'shared_training_and_test','near_clones_2pct_flip','dependency_drift','all_perfect_sensors'})
    def test_mirror_half_step(self):self.assertEqual((27,27.5,1)[1],27.5)
if __name__=='__main__':unittest.main()
