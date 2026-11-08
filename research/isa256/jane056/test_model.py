import unittest
from model import *
class Tests(unittest.TestCase):
 def test_27(self):self.assertEqual(GEOMETRY["vertices"],27)
 def test_ternary(self):self.assertEqual(GEOMETRY["modes"],(-1,0,1))
 def test_30(self):self.assertEqual(GEOMETRY["vertices"]+len(GEOMETRY["modes"]),30)
 def test_seam(self):self.assertEqual(GEOMETRY["seam"],(27,27.5,1))
 def test_wave(self):self.assertEqual(GEOMETRY["wave"],GEOMETRY["wave"][::-1])
 def test_two_waldos(self):self.assertEqual(GEOMETRY["waldos"],2)
 def test_independent(self):
  j=Jane([sample("A","a","root1"),sample("A","b","root2")]);self.assertEqual(j.query("x"),("SUPPORTED","A"))
 def test_clones(self):
  j=Jane([sample("A","a","same"),sample("A","b","same"),sample("A","c","same")]);self.assertEqual(j.query("x")[0],"UNVERIFIED")
 def test_conflict(self):
  j=Jane([sample("A","a","root1"),sample("B","b","root2")]);self.assertEqual(j.query("x")[0],"UNVERIFIED")
 def test_wrong_quorum(self):
  j=Jane([sample("B","a","root1"),sample("B","b","root2"),sample("A","c","root3")]);self.assertEqual(j.query("x")[1],"B")
 def test_offline(self):
  j=Jane([]);j.online=False;self.assertEqual(j.query("x"),("UNKNOWN",None))
 def test_cached(self):
  j=Jane([sample("A","a","r1"),sample("A","b","r2")]);j.query("x");j.online=False
  self.assertEqual(j.query("x"),("CACHED_UNVERIFIED","A"))
 def test_expired(self):
  j=Jane([sample("A","a","r1"),sample("A","b","r2")],ttl=0);j.query("x");j.online=False
  self.assertEqual(j.query("x")[0],"UNKNOWN")
 def test_cache_cap(self):
  j=Jane([sample(k,"A","a","r1",) for k in []],capacity=1)
  j.reports=[sample("A","a","r1",key="x"),sample("A","b","r2",key="x"),
             sample("B","a","r1",key="y"),sample("B","b","r2",key="y")]
  j.query("x");j.query("y");self.assertEqual(list(j.cache),["y"])
 def test_log_intact(self):
  j=Jane([]);j.query("missing");self.assertTrue(j.audit())
 def test_log_corrupt(self):
  j=Jane([]);j.query("missing");j.log[0]["data"]["key"]="changed";self.assertFalse(j.audit())
 def test_policy_range(self):
  with self.assertRaises(ValueError):Jane([],capacity=0)
 def test_no_promotion(self):
  j=Jane([]);cases=[dict(reports=[sample("A","a","r1"),sample("A","b","r2")],truth="A")]
  self.assertIsNone(j.propagate(cases,list(cases)));self.assertEqual(j.threshold,2)
 def test_promotion(self):
  j=Jane([],threshold=1)
  wrong=[dict(reports=[sample("WRONG","a","r1")],truth="RIGHT") for _ in range(7)]
  right=[dict(reports=[sample("RIGHT","a","r1"),sample("RIGHT","b","r2")],truth="RIGHT") for _ in range(7)]
  cases=wrong+right
  self.assertEqual(j.propagate(cases,list(cases)),2);self.assertEqual(j.version,1)
 def test_reject_same_holdout(self):
  j=Jane([]);cases=[]
  with self.assertRaises(ValueError):j.propagate(cases,cases)
 def test_five_steps(self):
  j=Jane([]);j.propagate([],list([]))
  self.assertEqual([e["event"] for e in j.log],["OBSERVE","PROPOSE","TEST","RETURN","RETAIN"])
 def test_kernel_constant(self):
  j=Jane([]);before=j.kernel;j.propagate([],list([]));self.assertEqual(j.kernel,before)
if __name__=="__main__":unittest.main()
