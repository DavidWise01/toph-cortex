"""Gate19 Sapphons inhabit cubit: exact containment, slot and source bounds."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import sapphon_registry as sapphon

PATH=Path(__file__).resolve().parents[1]/"memory/stochieon/cubit-sapphon-promotions-v1.json"

class SapphonInsideCubitTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_full_registry_and_cubit_parent(self):
        status=sapphon.verify(self.data)
        self.assertEqual(status["status"],"PASS")
        self.assertEqual(status["child_sapphons"],16)
        self.assertEqual(status["inside"],"cubit")
        self.assertEqual(status["spectral_positions"],18)
        self.assertEqual(status["new_agents_created"],0)

    def test_all_sapphons_are_nested_not_cortex_peers(self):
        self.assertTrue(all(n["parent"]=="cubit" and n["containment"]=="INSIDE_CUBIT"
                            for n in self.data["nodes"]))
        d=copy.deepcopy(self.data)
        d["nodes"][0]["parent"]="CORTEX"
        with self.assertRaisesRegex(ValueError,"escaped"):
            sapphon.verify(d)

    def test_parent_structure_is_exactly_eighteen_positions(self):
        d=copy.deepcopy(self.data)
        d["parent_cubit"]["slots"]=20
        with self.assertRaisesRegex(ValueError,"eighteen"):
            sapphon.verify(d)

    def test_no_synthetic_spectral_anchor_slots(self):
        for key in ("outer_anchors_consume_slots","broadband_white_consumes_slots"):
            d=copy.deepcopy(self.data)
            d["parent_cubit"][key]=True
            with self.assertRaisesRegex(ValueError,"cannot consume"):
                sapphon.verify(d)

    def test_only_spectrum_and_geometry_bind_numbered_positions(self):
        d=copy.deepcopy(self.data)
        d["nodes"][0]["spectral_slot_binding"]="EXACT_PARENT_18"
        with self.assertRaisesRegex(ValueError,"Only spectral"):
            sapphon.verify(d)

    def test_fourth_prime_is_not_fabricated(self):
        d=copy.deepcopy(self.data)
        d["prime_ordinal"]["found_canonical"].append(4)
        d["prime_ordinal"]["unassigned"]=[5]
        with self.assertRaisesRegex(ValueError,"Prime 04/05"):
            sapphon.verify(d)

    def test_historical_prime03_is_not_governance_quorum(self):
        d=copy.deepcopy(self.data)
        d["scope"]["independent_witness_quorum"]=2
        with self.assertRaisesRegex(ValueError,"votes or signatures"):
            sapphon.verify(d)

    def test_immutable_cubit_constant_cannot_be_qubit(self):
        d=copy.deepcopy(self.data)
        d["constant"]="qubit"
        with self.assertRaisesRegex(ValueError,"lowercase cubit"):
            sapphon.verify(d)

    def test_watermark_dlw_not_dropped(self):
        d=copy.deepcopy(self.data)
        d["mark"]="NO_MARK"
        with self.assertRaisesRegex(ValueError,"Immutable .dlw"):
            sapphon.verify(d)

    def test_source_pin_must_be_present(self):
        d=copy.deepcopy(self.data)
        d["nodes"][0]["source"]["blob_sha"]="unknown"
        with self.assertRaisesRegex(ValueError,"blob SHA"):
            sapphon.verify(d)

    def test_no_repo_traversal_or_invented_other_source(self):
        d=copy.deepcopy(self.data)
        d["nodes"][0]["source"]["path"]="../../other"
        with self.assertRaisesRegex(ValueError,"Unsafe"):
            sapphon.verify(d)

    def test_cannot_mark_a_symbolic_component_live(self):
        d=copy.deepcopy(self.data)
        d["nodes"][-1]["runtime_claim"]="LIVE_AUTONOMOUS"
        with self.assertRaisesRegex(ValueError,"Cannot promote"):
            sapphon.verify(d)

    def test_promoted_components_and_frozen_history_are_unmodified(self):
        self.assertFalse(self.data["scope"]["sources_moved"])
        self.assertFalse(self.data["scope"]["files_copied"])
        self.assertEqual(self.data["preservation"]["source_history"],"UNCHANGED")
        self.assertEqual(self.data["parent_cubit"]["canonical"],sapphon.CANON)
        self.assertFalse(self.data["reference_hierarchy"]["no_flattening_to_cortex_siblings"] is False)

if __name__=="__main__":unittest.main()
