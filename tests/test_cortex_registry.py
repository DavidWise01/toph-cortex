"""STOCHIEON Cortex promotions: strict, offline, non-destructive tests."""
from pathlib import Path
import copy
import json
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import cortex_registry as cortex

REG=Path(__file__).resolve().parents[1]/"memory/stochieon/cortex-promotions-v1.json"

class CortexRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry=json.loads(REG.read_text(encoding="utf-8"))

    def test_all_promoted_source_classes_and_counts(self):
        result=cortex.verify(self.registry)
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["promoted"],14)
        self.assertEqual(result["families"],sorted(cortex.EXPECTED_FAMILIES))
        self.assertEqual(result["formal_source_files"],6)

    def test_deduplicate_ud0_and_agent_0root(self):
        result=cortex.verify(self.registry)
        self.assertEqual(result["mirrors_deduplicated"],1)
        rust=next(x for x in self.registry["promoted"] if x["id"]=="ud0-i13-rust-cortex")
        self.assertEqual(rust["source"]["blob_sha"],rust["mirrors"][0]["blob_sha"])

    def test_different_rust_blob_cannot_claim_mirror(self):
        reg=copy.deepcopy(self.registry)
        rust=next(x for x in reg["promoted"] if x["id"]=="ud0-i13-rust-cortex")
        rust["mirrors"][0]["blob_sha"]="0"*40
        with self.assertRaisesRegex(ValueError,"different Git blob"):
            cortex.verify(reg)

    def test_never_promote_symbolic_manifest_as_live_agent(self):
        reg=copy.deepcopy(self.registry)
        reg["promoted"][-1]["operational_status"]="LIVE_AGENT"
        with self.assertRaisesRegex(ValueError,"live cortex"):
            cortex.verify(reg)

    def test_dlw_and_cubit_are_immutable(self):
        for key,val in (("mark","DLW"),("immutable_constant","Cubit")):
            reg=copy.deepcopy(self.registry);reg[key]=val
            with self.assertRaisesRegex(ValueError,"lowercase cubit"):
                cortex.verify(reg)

    def test_no_quorum_or_fake_witnesses(self):
        for name,val in (("no_quorum",False),("independent_witness_claims_created",3),
                         ("executable_redeployments",1)):
            reg=copy.deepcopy(self.registry);reg["promotion_policy"][name]=val
            with self.assertRaises(ValueError):cortex.verify(reg)

    def test_symbolic_identity_carrier_is_exact(self):
        reg=copy.deepcopy(self.registry)
        node=next(x for x in reg["promoted"] if x["family"]=="oasis-four-cortex")
        node["carrier"]="{{I}}"
        with self.assertRaisesRegex(ValueError,"carrier altered"):
            cortex.verify(reg)

    def test_source_paths_have_no_parent_traversal(self):
        reg=copy.deepcopy(self.registry)
        reg["promoted"][0]["source"]["path"]="../../private"
        with self.assertRaisesRegex(ValueError,"Unsafe source path"):
            cortex.verify(reg)

    def test_false_formal_compilation_claim_is_rejected(self):
        reg=copy.deepcopy(self.registry)
        reg["supporting_formal_sources"][0]["kind"]="proven"
        with self.assertRaisesRegex(ValueError,"compilation"):
            cortex.verify(reg)

    def test_no_source_files_were_moved(self):
        result=cortex.verify(self.registry)
        self.assertEqual(result["live_agents_created"],0)
        self.assertEqual(self.registry["promotion_policy"]["source_history"],"UNCHANGED")

if __name__=="__main__":unittest.main()
