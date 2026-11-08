import unittest
from dataclasses import replace
from model import *
class TestWitnessDivergence(unittest.TestCase):
 def test_geometry(self):self.assertEqual(N,27)
 def test_ternary(self):self.assertEqual(STATES,(-1,0,1))
 def test_accounting(self):self.assertEqual(N+len(STATES),30)
 def test_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_wave_counts(self):self.assertEqual([WAVE.count(str(x)) for x in range(1,6)],[6]*5)
 def test_three_keys(self):self.assertEqual(len(KEYS),3)
 def test_unique_keys(self):self.assertEqual(len(set(KEYS.values())),3)
 def test_authentic(self):self.assertTrue(authenticated(attest("A",1,ROOT0,ROOT1)))
 def test_forgery(self):self.assertFalse(authenticated(replace(attest("A",1,ROOT0,ROOT1),root=FORK1)))
 def test_unanimous(self):self.assertEqual(case("unanimous")["status"],"VERIFIED")
 def test_two(self):self.assertEqual(case("two_agree")["status"],"VERIFIED")
 def test_split(self):self.assertEqual(case("split")["status"],"CONFLICT")
 def test_fork(self):self.assertEqual(case("majority_with_fork")["status"],"VERIFIED_WITH_DIVERGENCE")
 def test_rejected_tamper(self):self.assertEqual(case("tampered_mac")["status"],"INSUFFICIENT")
 def test_stale(self):self.assertEqual(case("replayed_old")["status"],"INSUFFICIENT")
 def test_missing_chain(self):self.assertEqual(case("missing_chain")["status"],"INSUFFICIENT")
 def test_known_chain(self):self.assertEqual(case("known_chain")["status"],"VERIFIED")
 def test_equivocation(self):self.assertEqual(case("equivocation")["status"],"INSUFFICIENT")
 def test_equivocation_flagged(self):self.assertEqual(case("equivocation")["equivocation"],["A"])
 def test_two_corrupt_undetected(self):self.assertEqual(case("two_corrupt")["status"],"VERIFIED_WITH_DIVERGENCE")
 def test_no_evidence(self):self.assertEqual(case("missing_all")["status"],"INSUFFICIENT")
 def test_duplicate_not_quorum(self):
  p=attest("A",1,ROOT0,ROOT1)
  self.assertNotEqual(Verifier().evaluate([p,p])["status"],"VERIFIED")
 def test_wrong_prev(self):
  records=[attest("A",1,"bogus",ROOT1),attest("B",1,"bogus",ROOT1)]
  self.assertEqual(Verifier().evaluate(records)["status"],"INSUFFICIENT")
 def test_wrong_epoch(self):self.assertEqual(Verifier().evaluate([attest("A",5,ROOT0,ROOT1)])["status"],"INSUFFICIENT")
 def test_threshold3(self):
  a=attest("A",1,ROOT0,ROOT1);b=attest("B",1,ROOT0,ROOT1)
  self.assertEqual(Verifier(threshold=3).evaluate([a,b])["status"],"INSUFFICIENT")
 def test_threshold3_all(self):
  x=[attest(w,1,ROOT0,ROOT1) for w in KEYS]
  self.assertEqual(Verifier(threshold=3).evaluate(x)["status"],"VERIFIED")
 def test_known_chain_cannot_skip(self):
  x=[attest("A",3,ROOT2,"later"),attest("B",3,ROOT2,"later")]
  self.assertEqual(Verifier().evaluate(x,{(1,ROOT1):ROOT0})["status"],"INSUFFICIENT")
 def test_signature_unique_to_witness(self):
  x=attest("A",1,ROOT0,ROOT1)
  self.assertFalse(authenticated(replace(x,witness="B")))
 def test_anchor_pinning(self):
  x=[attest("A",1,ROOT0,ROOT1),attest("B",1,ROOT0,ROOT1)]
  self.assertEqual(Verifier(anchor_root="different").evaluate(x)["status"],"INSUFFICIENT")
 def test_determinism(self):self.assertEqual(case("majority_with_fork"),case("majority_with_fork"))
if __name__=="__main__":unittest.main()
