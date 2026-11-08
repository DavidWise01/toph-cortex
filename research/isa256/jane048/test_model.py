import unittest
from model import *
class ProvenanceTests(unittest.TestCase):
 def setUp(self):self.r=registry();self.a=[anchor(k,self.r) for k in KEYS]
 def test_size(self):self.assertEqual(len(KEYS),3)
 def test_signature(self):self.assertTrue(verify_registry_signature(self.r))
 def test_signature_modified(self):
  r=dict(self.r);r["seq"]=12;self.assertFalse(verify_registry_signature(r))
 def test_anchor_signature(self):self.assertTrue(verify_anchor(self.a[0]))
 def test_anchor_forged(self):self.assertFalse(verify_anchor(anchor("alpha",self.r,forged=True)))
 def test_wrong_domain(self):self.assertFalse(verify_anchor(anchor("alpha",self.r,domain="root-b")))
 def test_unknown_anchor(self):
  with self.assertRaises(ValueError):anchor("unknown",self.r)
 def test_distinct_domains(self):self.assertEqual(len(set(TRUSTED_DOMAINS.values())),3)
 def test_stable_digest(self):self.assertEqual(digest(self.r),digest(dict(reversed(list(self.r.items())))))
 def test_valid(self):self.assertEqual(verify(self.r,self.a,8)["status"],"ANCHORED")
 def test_missing_one(self):self.assertEqual(verify(self.r,self.a[:2],8)["status"],"ANCHORED")
 def test_missing_two(self):self.assertEqual(verify(self.r,self.a[:1],8)["status"],"INSUFFICIENT")
 def test_none(self):self.assertEqual(verify(self.r,[],8)["quorum"],0)
 def test_repeated_anchor(self):self.assertEqual(verify(self.r,[self.a[0]]*3,8)["quorum"],1)
 def test_one_corrupt(self):
  a=self.a[0].copy();a["signature"]="f"*64
  self.assertEqual(verify(self.r,[a,self.a[1],self.a[2]],8)["status"],"ANCHORED")
 def test_two_corrupt(self):
  a=self.a[0].copy();a["signature"]="f"*64
  b=self.a[1].copy();b["signature"]="f"*64
  self.assertEqual(verify(self.r,[a,b,self.a[2]],8)["status"],"INSUFFICIENT")
 def test_stale(self):self.assertEqual(scenarios()["rollback_pinned"]["status"],"ROLLBACK")
 def test_unpinned(self):self.assertEqual(scenarios()["rollback_unpinned"]["status"],"ANCHORED")
 def test_changed_root(self):self.assertEqual(scenarios()["rewritten_old_anchors"]["quorum"],0)
 def test_independent_signature_no_truth(self):self.assertEqual(scenarios()["two_keys_lying"]["status"],"ANCHORED")
 def test_independent_fact(self):self.assertEqual(scenarios()["two_keys_contradicted"]["status"],"CONTRADICTED")
 def test_invalid_graph_signed_fresh(self):
  r=registry(deps={"w1":["x"],"w2":["x"],"w3":["x"]})
  a=[anchor("alpha",r),anchor("beta",r)]
  self.assertEqual(verify(r,a,8)["status"],"ANCHORED")
 def test_no_vote_without_anchors(self):
  v=approval(self.r,[],{"w1":"GOOD","w2":"GOOD"},8)
  self.assertFalse(v["approval"])
 def test_vote_with_independence(self):
  v=approval(self.r,self.a,{"w1":"GOOD","w2":"GOOD"},8)
  self.assertTrue(v["approval"])
 def test_vote_conflicting(self):
  v=approval(self.r,self.a,{"w1":"GOOD","w2":"BAD"},8)
  self.assertFalse(v["approval"])
 def test_cloned_source(self):
  r=registry(deps={"w1":["x"],"w2":["x"],"w3":["x"]})
  a=[anchor("alpha",r),anchor("beta",r)]
  self.assertFalse(approval(r,a,{"w1":"GOOD","w2":"GOOD"},8)["approval"])
 def test_claim_without_witness(self):
  v=approval(self.r,self.a,{"w9":"GOOD","w1":"GOOD"},8)
  self.assertFalse(v["approval"])
 def test_invalid_registry(self):
  r=self.r.copy();r["signature"]="0"*64
  self.assertEqual(verify(r,self.a,8)["status"],"TAMPERED")
 def test_anchor_seq(self):
  a=self.a[0].copy();a["seq"]=7
  self.assertFalse(verify_anchor(a))
 def test_anchor_root(self):
  a=self.a[0].copy();a["root"]="0"*64
  self.assertFalse(verify_anchor(a))
 def test_seed_repro(self):self.assertEqual(monte_carlo(25,41),monte_carlo(25,41))
 def test_monte_counts(self):
  for row in monte_carlo(15):self.assertEqual(sum(v for k,v in row.items() if k!="case"),15)
 def test_clean_sim(self):self.assertEqual(monte_carlo(5)[0]["ANCHORED"],5)
 def test_collusion_sim(self):self.assertEqual(monte_carlo(5)[4]["ANCHORED"],5)
 def test_r_zero_is_valid_without_pin(self):
  r=registry(seq=0);a=[anchor("alpha",r),anchor("gamma",r)]
  self.assertEqual(verify(r,a)["status"],"ANCHORED")
 def test_r_zero_stale_with_pin(self):
  r=registry(seq=0);a=[anchor("alpha",r),anchor("gamma",r)]
  self.assertEqual(verify(r,a,1)["status"],"ROLLBACK")
 def test_different_true_root(self):
  r=registry(seq=9);self.assertNotEqual(self.a[0]["root"],anchor("alpha",r)["root"])
if __name__=="__main__":unittest.main()
