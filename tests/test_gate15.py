"""Gate 15: exact causal-head locks for an authenticated loom continuation."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine
import threaded_loom as loom
import loom_next

NOW="2026-10-27T21:39:51.830Z"

class CausalHandoffTests(unittest.TestCase):
    def setUp(self):
        self.corpus=corpus_spine.read_rows()
        self.one=loom.make([],self.corpus,kind="OPEN",thread="tessy-1",witness="A",
            phase="PAST_OBSERVES",event_on="2026-10-27",what="what",how="how",
            why="why",text="",recorded_at=NOW)

    def test_head_sha_pair_matches_actual_first_event(self):
        o=loom.require_heads([self.one],"tessy-1","A",
            expect_thread_head=self.one["hash"],expect_witness_head=self.one["hash"])
        self.assertEqual(o["thread_seq"],1)
        self.assertEqual(o["witness_seq"],1)

    def test_stale_thread_hash_halts_before_append(self):
        with self.assertRaisesRegex(ValueError,"STALE THREAD HEAD"):
            loom.require_heads([self.one],"tessy-1","A",
                expect_thread_head="0"*64,expect_witness_head=self.one["hash"])

    def test_stale_witness_hash_halts_before_append(self):
        with self.assertRaisesRegex(ValueError,"STALE WITNESS HEAD"):
            loom.require_heads([self.one],"tessy-1","A",
                expect_thread_head=self.one["hash"],expect_witness_head="0"*64)

    def test_new_thread_requires_genesis_pair(self):
        o=loom.require_heads([self.one],"another-thread","A",
            expect_thread_head="GENESIS",expect_witness_head="GENESIS")
        self.assertIsNone(o["thread_seq"])

    def test_unassigned_lane_is_not_an_approved_witness(self):
        with self.assertRaisesRegex(ValueError,"unassigned"):
            loom_next.prepare([self.one],self.corpus,"tessy-1","B",NOW)

    def test_new_lane_head_can_be_genesis_even_if_thread_open(self):
        o=loom.require_heads([self.one],"tessy-1","B",
            expect_thread_head=self.one["hash"],expect_witness_head="GENESIS")
        self.assertIsNone(o["witness_seq"])

    def test_invalid_sha_format_rejected(self):
        with self.assertRaisesRegex(ValueError,"64-character SHA"):
            loom.require_heads([self.one],"tessy-1","A",
                expect_thread_head="bad",expect_witness_head=self.one["hash"])

    def test_next_plan_contains_ref_and_exact_sha_head(self):
        plan=loom_next.prepare([self.one],self.corpus,"tessy-1","A",NOW)
        self.assertEqual(plan["refs"],"1")
        self.assertEqual(plan["expected_thread_head_sha"],self.one["hash"])
        self.assertEqual(plan["expected_witness_head_sha"],self.one["hash"])
        self.assertFalse(plan["may_commit_without_authentication"])

if __name__=="__main__":unittest.main()
