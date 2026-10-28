"""Regression checks for the ROOT0 append-only corpus spine."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine as spine

class CorpusSpineTest(unittest.TestCase):
    def test_committed_chain(self):
        rows=spine.read_rows()
        self.assertGreaterEqual(len(rows),1)
        self.assertEqual(spine.verify_rows(rows),rows[-1]["hash"])

    def test_reject_mutated_event(self):
        rows=spine.read_rows()
        changed=[dict(x) for x in rows]
        changed[0]["what"]="altered"
        with self.assertRaises(ValueError):
            spine.verify_rows(changed)

    def test_reject_truncation_with_bad_link(self):
        rows=spine.read_rows()
        # Use a second synthetic row; the canonical chain may contain
        # only its authentic genesis, and must never be padded for tests.
        extra=spine.append_row(rows,actor="root0",kind="CORRECTION",
            source=dict(rows[0]["source"]),what="fixture-only second event",
            how="synthetic offline test",why="test bad predecessor",
            supersedes=1,date="2026-10-27")
        changed=[dict(x) for x in [*rows,extra]]
        changed[1]["prev"]="GENESIS"
        with self.assertRaises(ValueError):
            spine.verify_rows(changed)

    def test_append_correction(self):
        rows=spine.read_rows()
        source=dict(rows[0]["source"])
        entry=spine.append_row(rows,actor="root0",kind="CORRECTION",
                source=source,what="updated interpretation",how="reference review",
                why="keep history",supersedes=1,date="2026-10-27")
        self.assertEqual(spine.verify_rows(rows+[entry]),entry["hash"])

    def test_no_non_public_sources(self):
        source=dict(spine.read_rows()[0]["source"])
        source["visibility"]="private"
        with self.assertRaises(ValueError):
            spine.validate_source(source)

if __name__=="__main__":
    unittest.main()
