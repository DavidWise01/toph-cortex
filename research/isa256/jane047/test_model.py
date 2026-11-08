import unittest,random
from dataclasses import replace
from model import *

class TestJane047(unittest.TestCase):
    def test_registry(self):self.assertEqual(len(registry('independent')),3)
    def test_unknown_registry(self):
        with self.assertRaises(ValueError):registry('x')
    def test_authentication(self):self.assertTrue(authentic(sign('A',47,TRUE)))
    def test_tamper(self):self.assertFalse(authentic(replace(sign('A',47,TRUE),digest=FALSE)))
    def test_wrong_epoch(self):self.assertFalse(authentic(replace(sign('A',47,TRUE),epoch=46)))
    def test_distinct(self):self.assertEqual(verify([sign('A',47,TRUE),sign('B',47,TRUE)],registry('independent'),47)['digest'],TRUE)
    def test_one_not_quorum(self):self.assertEqual(verify([sign('A',47,TRUE)],registry('independent'),47)['status'],'INSUFFICIENT')
    def test_shared_reports_naive(self):self.assertEqual(verify([sign('A',47,FALSE),sign('B',47,FALSE)],registry('paired'),47,False)['digest'],FALSE)
    def test_shared_reports_aware(self):self.assertEqual(verify([sign('A',47,FALSE),sign('B',47,FALSE)],registry('paired'),47,True)['digest'],None)
    def test_three_clones(self):self.assertFalse(dependencies(registry('cloned')['A']).isdisjoint(dependencies(registry('cloned')['C'])))
    def test_shared_root(self):self.assertFalse(dependencies(registry('shared-key')['A']).isdisjoint(dependencies(registry('shared-key')['B'])))
    def test_overlap(self):self.assertFalse(dependencies(registry('overlap')['A']).isdisjoint(dependencies(registry('overlap')['B'])))
    def test_two_compromised(self):self.assertEqual(verify([sign('A',47,FALSE),sign('B',47,FALSE)],registry('independent'),47)['digest'],FALSE)
    def test_pinned(self):self.assertEqual(verify([sign('A',47,FALSE),sign('B',47,FALSE)],registry('independent'),47,pinned=TRUE)['status'],'ANCHOR_CONFLICT')
    def test_rollback(self):self.assertEqual(verify([],registry('independent'),46,min_epoch=47)['status'],'ROLLBACK')
    def test_duplicate_one(self):
        a=sign('A',47,TRUE)
        self.assertEqual(verify([a,a,a],registry('independent'),47)['digest'],None)
    def test_equivocation(self):
        a=sign('A',47,TRUE);b=sign('A',47,FALSE)
        self.assertEqual(verify([a,b,sign('B',47,TRUE)],registry('independent'),47)['digest'],None)
    def test_dissent(self):self.assertEqual(verify([sign('A',47,TRUE),sign('B',47,FALSE)],registry('independent'),47)['status'],'CONFLICT_NO_QUORUM')
    def test_cloned_abstains(self):
        for i in range(30):self.assertEqual(trial('cloned',random.Random(i),True),'ABSTAIN')
    def test_sharedkey_abstains(self):
        for i in range(30):self.assertEqual(trial('shared-key',random.Random(i),True),'ABSTAIN')
    def test_sweep_count(self):self.assertEqual(len(sweep(10)),10)
    def test_total(self):
        for row in sweep(40):self.assertEqual(row['TRUE_ACCEPT']+row['FALSE_ACCEPT']+row['ABSTAIN'],40)
    def test_repeat(self):self.assertEqual(sweep(50),sweep(50))
    def test_clones_naive_can_fail(self):
        row=next(x for x in sweep() if x['config']=='cloned' and x['verifier']=='naive')
        self.assertGreater(row['FALSE_ACCEPT'],0)
    def test_clones_aware_safely_abstains(self):
        row=next(x for x in sweep() if x['config']=='cloned' and x['verifier']=='source-aware')
        self.assertEqual(row['FALSE_ACCEPT'],0)
if __name__=="__main__":unittest.main()
