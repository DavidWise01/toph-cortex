"""Read-only next-turn planner for a real, append-only witness thread."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine
import threaded_loom as loom
import loom_next

UTC="2026-10-27T21:39:51.830Z"
DAY="2026-10-27"
LATER="2026-10-28"

def make(rows, corpus, *, kind="OPEN", witness="A", phase="PAST_OBSERVES",
         thread="tessy-1", date=DAY, message="cubit"):
    return loom.make(rows,corpus,kind=kind,thread=thread,witness=witness,
        phase=phase,event_on=date,what="Witness statement",how="Observed",
        why="Provenance",text=message,recorded_at=UTC)

class NextLoomTests(unittest.TestCase):
    def setUp(self):
        self.corpus=corpus_spine.read_rows()
        self.genesis=make([],self.corpus)

    def test_real_open_next_is_weave_present(self):
        p=loom_next.prepare([self.genesis],self.corpus,"tessy-1","A",UTC)
        self.assertEqual(p["operation"],"WEAVE")
        self.assertEqual(p["phase"],"PRESENT_DESERVES")
        self.assertEqual(p["event_on"],DAY)
        self.assertEqual(p["source_thread_head_hash"],self.genesis["hash"])
        self.assertEqual(p["source_lane_head_seq"],1)
        self.assertEqual(p["content_constant"],"cubit")
        self.assertFalse(p["witness_statement_provided"])

    def test_other_witness_requires_actual_assignment(self):
        with self.assertRaisesRegex(ValueError,"unassigned"):
            loom_next.prepare([self.genesis],self.corpus,"tessy-1","B",UTC)
        with self.assertRaisesRegex(ValueError,"unassigned"):
            loom_next.prepare([self.genesis],self.corpus,"tessy-1","C",UTC)

    def test_exact_name_never_silently_renamed(self):
        with self.assertRaisesRegex(ValueError,"no authenticated OPEN"):
            loom_next.prepare([self.genesis],self.corpus,"tessy-i","A",UTC)

    def test_closed_lane_denied(self):
        rows=[self.genesis]
        rows.append(make(rows,self.corpus,kind="CLOSE",message="Closing A only"))
        with self.assertRaisesRegex(ValueError,"CLOSED"):
            loom_next.prepare(rows,self.corpus,"tessy-1","A",UTC)

    def test_future_lane_never_auto_reserved(self):
        rows=[self.genesis]
        rows.append(make(rows,self.corpus,kind="WEAVE",phase="PRESENT_DESERVES"))
        rows.append(make(rows,self.corpus,kind="WEAVE",phase="FUTURE_RESERVES",date=LATER))
        with self.assertRaisesRegex(ValueError,"explicit future date"):
            loom_next.prepare(rows,self.corpus,"tessy-1","A",UTC)

    def test_new_weave_preserves_source_head_and_no_vote(self):
        rows=[self.genesis]
        rows.append(make(rows,self.corpus,kind="WEAVE",phase="PRESENT_DESERVES"))
        p=loom_next.prepare(rows,self.corpus,"tessy-1","A",UTC)
        self.assertEqual(p["source_global_tip"],rows[-1]["hash"])
        self.assertEqual(p["source_lane_head_seq"],2)
        self.assertTrue(p["no_quorum"])
        self.assertFalse(p["votes"])
        self.assertFalse(p["may_commit_without_authentication"])

    def test_nonexistent_threads_are_not_materialized(self):
        with self.assertRaisesRegex(ValueError,"no authenticated OPEN"):
            loom_next.prepare([],self.corpus,"planned-only","A",UTC)
        s=loom_next.summarize([],self.corpus,UTC)
        self.assertEqual(s["threads"],{})

    def test_snapshot_is_projection_not_a_new_event(self):
        rows=[self.genesis]
        snap=loom_next.summarize(rows,self.corpus,UTC)
        self.assertEqual(snap["threads"]["tessy-1"]["head_seq"],1)
        self.assertEqual(snap["threads"]["tessy-1"]["events"],1)
        self.assertEqual(snap["global_tip"],self.genesis["hash"])
        self.assertFalse(snap["has_synthetic_witness_events"])
        self.assertEqual(len(rows),1)

    def test_corrupted_head_is_not_trusted(self):
        changed={**self.genesis,"text":"Forged"}
        with self.assertRaisesRegex(ValueError,"watermark"):
            loom_next.prepare([changed],self.corpus,"tessy-1","A",UTC)

if __name__=="__main__":
    unittest.main()
