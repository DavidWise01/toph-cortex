"""Offline tests: cubit must remain lowercase, atomic and never be normalized."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import cubit_constant as contract

class CubitConstantTests(unittest.TestCase):
    def test_exact_copy_preserves_all_occurrences(self):
        self.assertEqual(contract.verify("cubit / cubit", "cubit / cubit","copy")["output_cubit_count"],2)

    def test_copy_with_changed_surroundings_is_allowed(self):
        self.assertEqual(contract.verify("a cubit b", "new text [cubit]","copy")["result"],"PASS")

    def test_distill_may_compress_multiple_occurrences(self):
        self.assertEqual(contract.verify("cubit then cubit then cubit", "cubit","distill")["result"],"PASS")

    def test_distill_must_not_erase_constant(self):
        with self.assertRaisesRegex(contract.CubitContractError,"lost exact"):
            contract.verify("an analytical cubit here", "an analytical unit here","distill")

    def test_qubit_is_not_synonym(self):
        with self.assertRaisesRegex(contract.CubitContractError,"lost exact"):
            contract.verify("cubit", "qubit","distill")
        self.assertEqual(contract.verify("qubit hardware", "qubit hardware","copy")["source_cubit_count"],0)

    def test_case_and_plural_mutations_fail_closed(self):
        for spelling in ("Cubit","CUBIT","cUbIt","cubits","CUBITS"):
            with self.subTest(spelling=spelling),self.assertRaises(contract.CubitContractError):
                contract.verify("cubit", f"cubit and {spelling}","distill")

    def test_cubit_is_atomic_not_substring(self):
        p=contract.verify("cubit123 pre_cubit cubit-proof", "cubit-proof","distill")
        self.assertEqual(p["source_cubit_count"],1)
        self.assertEqual(p["output_cubit_count"],1)

    def test_copy_count_mismatch_fails(self):
        with self.assertRaisesRegex(contract.CubitContractError,"occurrence count"):
            contract.verify("cubit cubit", "cubit","copy")

    def test_proof_does_not_claim_semantic_equivalence(self):
        out=contract.verify("cubit", "cubit","copy")
        self.assertEqual(out["mark"],".dlw")
        self.assertFalse(out["semantic_equivalence_proven"])
        self.assertIsNone(out["quorum"])
        self.assertEqual(len(out["source_sha256"]),64)

    def test_empty_source_has_no_constant_obligation(self):
        self.assertEqual(contract.verify("no constant here","different summary","distill")["result"],"PASS")

if __name__=="__main__":
    unittest.main()
