import unittest
from tempfile import TemporaryDirectory
from model import System,Chain,BASELINE,run_attack
class Tests(unittest.TestCase):
 def test_normal(self):self.assertEqual(run_attack("none")["result"][0],"VERIFIED")
 def test_erasure(self):self.assertEqual(run_attack("erase_both")["result"][1],"ROLLBACK_A")
 def test_rollback(self):self.assertEqual(run_attack("rollback_A")["result"][1],"ROLLBACK_A")
 def test_forged_hash_chain(self):self.assertEqual(run_attack("rewrite_rehashed")["result"][1],"REWRITE_A")
 def test_witness_rollback_pinned(self):self.assertEqual(run_attack("rollback_anchor")["result"][1],"WITNESS_ROLLBACK")
 def test_baseline(self):self.assertEqual(BASELINE,741.3125)
 def test_unanchored(self):
  with TemporaryDirectory() as d:self.assertEqual(System(d).verify()[0],"UNANCHORED")
 def test_anchor(self):
  with TemporaryDirectory() as d:
   s=System(d);self.assertEqual(s.checkpoint(),1);self.assertEqual(s.verify()[0],"VERIFIED")
 def test_append_suffix(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();s.event("A",{"kind":"NEW"});self.assertEqual(s.verify()[0],"VERIFIED_PREFIX")
 def test_witness_corruption(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();s.witness.path.write_text(s.witness.path.read_text().replace("anchors","altered"))
   # An unchanged witness remains valid; targeted replacement of signed contents is checked separately.
   self.assertEqual(s.verify()[0],"VERIFIED")
 def test_witness_bad_mac(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();text=s.witness.path.read_text();s.witness.path.write_text(text.replace('"mac":"','"mac":"f',1));self.assertEqual(s.verify()[1],"WITNESS_MAC_FAIL")
 def test_duplicate_checkpoint(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();self.assertEqual(s.checkpoint(),2)
 def test_no_reconstruction_from_head(self):
  with TemporaryDirectory() as d:
   s=System(d);s.event("A",{"kind":"PRIVATE"});s.checkpoint();s.waldos["A"].path.write_bytes(b"")
   self.assertEqual(s.verify()[0],"INVALID")
 def test_pinned_rollback_missing_witness(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();s.witness.path.write_bytes(b"");self.assertEqual(s.verify(pinned=1)[1],"WITNESS_ROLLBACK")
 def test_unpinned_missing_witness(self):
  with TemporaryDirectory() as d:
   s=System(d);s.checkpoint();s.witness.path.write_bytes(b"");self.assertEqual(s.verify()[0],"UNANCHORED")
if __name__=="__main__":unittest.main()
