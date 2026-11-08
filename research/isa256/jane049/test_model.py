import unittest
from dataclasses import replace
from model import *
class JANE049(unittest.TestCase):
 def test_geometry(self):self.assertEqual(POSITIONS,27)
 def test_ternary(self):self.assertEqual(TERNARY,(-1,0,1))
 def test_30_components(self):self.assertEqual(POSITIONS+len(TERNARY),30)
 def test_wave_length(self):self.assertEqual(len(WAVE),30)
 def test_wave_palindrome(self):self.assertEqual(WAVE,WAVE[::-1])
 def test_six_per_level(self):self.assertEqual([WAVE.count(str(i)) for i in range(1,6)],[6]*5)
 def test_seam(self):self.assertIn('27.5',SEAM)
 def test_signature(self):
  a=anchors()[0];rec=issue(a,1,'GENESIS','x');self.assertTrue(authentic(rec,a))
 def test_wrong_key(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x');self.assertFalse(authentic(r,Root(a.name,a.domain,'wrong')))
 def test_wrong_domain(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x');self.assertFalse(authentic(r,Root(a.name,'other',a.key)))
 def test_wrong_root_name(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x');self.assertFalse(authentic(r,Root('x',a.domain,a.key)))
 def test_record_identifier_stable(self):
  a=anchors()[0];self.assertEqual(issue(a,1,'GENESIS','x').id(),issue(a,1,'GENESIS','x').id())
 def test_signature_payload_tamper(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x');self.assertFalse(authentic(replace(r,claim='y'),a))
 def test_chain_clean(self):self.assertEqual(scenario('clean')['status'],'VERIFIED')
 def test_chain_tamper(self):self.assertEqual(scenario('tamper')['status'],'INVALID_AUTHORITY')
 def test_pinned_rollback(self):self.assertEqual(scenario('rollback_pinned')['status'],'ROLLBACK')
 def test_unpinned_rollback(self):self.assertEqual(scenario('rollback_unpinned')['status'],'VERIFIED')
 def test_stolen_key_pinned(self):self.assertEqual(scenario('key_compromise_pinned')['status'],'HISTORY_CONFLICT')
 def test_stolen_key_unpinned(self):self.assertEqual(scenario('key_compromise_unpinned')['status'],'VERIFIED')
 def test_shared_root_denied(self):self.assertEqual(scenario('shared_root')['status'],'INSUFFICIENT')
 def test_independent_sources(self):self.assertEqual(scenario('independent_roots')['status'],'wave=2')
 def test_colluding_roots_false_claim(self):self.assertEqual(scenario('colluding_roots')['status'],'wave=999')
 def test_compromised_pin_false_claim(self):self.assertEqual(scenario('pin_compromised')['status'],'VERIFIED')
 def test_absent_root(self):self.assertEqual(scenario('absent_root')['status'],'INSUFFICIENT')
 def test_broken_link(self):self.assertEqual(scenario('broken_link')['status'],'BROKEN_CHAIN')
 def test_missing(self):self.assertEqual(verify_chain(anchors()[0],[]),'MISSING_HISTORY')
 def test_wrong_pin_root(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x')
  self.assertEqual(verify_chain(a,[r],TrustPin('wrong',1,r.id())),'PIN_MISMATCH')
 def test_multiple_paths_shared(self):
  deps={'a':('shared','xa'),'b':('shared','xb'),'c':('shared','xc')}
  self.assertEqual(source_aware_quorum(deps,dict.fromkeys(deps,'yes')),'INSUFFICIENT')
 def test_two_disjoint(self):
  self.assertEqual(source_aware_quorum({'a':['ra'],'b':['rb']},{'a':'yes','b':'yes'}),'yes')
 def test_same_root_two_records(self):
  self.assertEqual(source_aware_quorum({'a':['ra'],'b':['ra']},{'a':'yes','b':'yes'}),'INSUFFICIENT')
 def test_disagree(self):
  self.assertEqual(source_aware_quorum({'a':['ra'],'b':['rb']},{'a':'yes','b':'no'}),'INSUFFICIENT')
 def test_conflicting_quorums(self):
  deps={str(i):[str(i)] for i in range(4)}
  self.assertEqual(source_aware_quorum(deps,{'0':'yes','1':'yes','2':'no','3':'no'}),'CONFLICT')
 def test_no_reports(self):self.assertEqual(source_aware_quorum({},{}),'INSUFFICIENT')
 def test_determinism(self):self.assertEqual(full_report(),full_report())
 def test_scenario_count(self):self.assertEqual(len(full_report()['scenarios']),12)
 def test_all_scenarios_have_note(self):self.assertTrue(all(scenario(x)['note'] for x in SCENARIOS))
 def test_unknown_case(self):
  with self.assertRaises(ValueError):scenario('unknown')
 def test_chain_epoch_skipping(self):
  a=anchors()[0];r=issue(a,3,'GENESIS','x')
  self.assertEqual(verify_chain(a,[r]),'BROKEN_CHAIN')
 def test_substituted_chain_pin(self):
  a=anchors()[0];r=issue(a,1,'GENESIS','x');s=issue(a,1,'GENESIS','y')
  self.assertEqual(verify_chain(a,[s],TrustPin(a.name,1,r.id())),'HISTORY_CONFLICT')
 def test_cannot_infer_truth_from_signature(self):
  self.assertEqual(scenario('pin_compromised')['status'],scenario('clean')['status'])
if __name__=='__main__':unittest.main()
