"""Temporal diode: test three witnesses independently; never quorum or backward commits."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine
import temporal_diode as diode

SOURCE={"repo":"DavidWise01/oasis","path":"README.md","blob_sha":"a"*40,"visibility":"public"}
DAY="2026-10-27"
CORPUS=corpus_spine.read_rows()

def record(rows=None,*,thread="experiment-1",witness="A",phase="PAST_OBSERVES",
           event_on="2026-10-26",corpus=CORPUS):
    return diode.append(rows or [],corpus,thread=thread,witness=witness,
        phase=phase,event_on=event_on,source=dict(SOURCE),
        what="Observed a change",how="Independent sensor trace",
        why="Record without consensus",recorded_at=DAY)

class TemporalDiode(unittest.TestCase):
    def test_verified_genesis_and_empty_no_fabricated_witnesses(self):
        self.assertEqual(diode.verify_rows([],CORPUS),"GENESIS")
        self.assertEqual(diode.summary([])["witness_lanes"],{})
        self.assertEqual(diode.read_rows(diode.LEDGER,CORPUS),[])

    def test_one_lane_can_reach_future_without_others(self):
        a=record()
        b=record([a],phase="PRESENT_DESERVES",event_on=DAY)
        c=record([a,b],phase="FUTURE_RESERVES",event_on="2026-11-10")
        self.assertEqual(diode.verify_rows([a,b,c],CORPUS),c["hash"])
        s=diode.summary([a,b,c])
        self.assertEqual(set(s["witness_lanes"]["experiment-1"]),{"A"})
        self.assertIsNone(s["quorum"])
        self.assertFalse(s["voting"])
        self.assertFalse(s["auto_execution"])

    def test_B_reports_independently_even_after_A_reserves(self):
        a=record()
        p=record([a],phase="PRESENT_DESERVES",event_on=DAY)
        f=record([a,p],phase="FUTURE_RESERVES",event_on="2026-11-10")
        b=record([a,p,f],witness="B",phase="PAST_OBSERVES",event_on="2026-10-01")
        self.assertEqual(diode.verify_rows([a,p,f,b],CORPUS),b["hash"])

    def test_must_not_skip_present_or_regress(self):
        a=record()
        with self.assertRaisesRegex(ValueError,"diode forbids"):
            record([a],phase="FUTURE_RESERVES",event_on="2026-11-01")
        p=record([a],phase="PRESENT_DESERVES",event_on=DAY)
        with self.assertRaisesRegex(ValueError,"diode forbids"):
            record([a,p],phase="PAST_OBSERVES",event_on="2026-10-26")

    def test_temporal_date_cannot_cause_future_execution(self):
        with self.assertRaisesRegex(ValueError,"past observation"):
            record(event_on="2026-10-28")
        a=record()
        with self.assertRaisesRegex(ValueError,"present deserves"):
            record([a],phase="PRESENT_DESERVES",event_on="2026-10-26")
        p=record([a],phase="PRESENT_DESERVES",event_on=DAY)
        with self.assertRaisesRegex(ValueError,"future reservation"):
            record([a,p],phase="FUTURE_RESERVES",event_on=DAY)

    def test_bad_hash_and_lane_reference_fail(self):
        a=record()
        b=record([a],phase="PRESENT_DESERVES",event_on=DAY)
        changed=[dict(a),dict(b)]
        changed[1]["why"]="changed"
        with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
            diode.verify_rows(changed,CORPUS)
        changed[1]["why"]=b["why"]
        changed[1]["anchor"]=99
        with self.assertRaisesRegex(ValueError,"wrong predecessor"):
            diode.verify_rows(changed,CORPUS)

    def test_corrupt_corpus_anchor_rejected(self):
        a=record()
        changed=dict(a,corpus_tip="f"*64)
        with self.assertRaisesRegex(ValueError,"unknown verified corpus anchor"):
            diode.verify_rows([changed],CORPUS)

    def test_independent_witness_C_can_begin_late(self):
        a=record()
        c=record([a],witness="C",event_on="2026-10-25")
        self.assertEqual(diode.verify_rows([a,c],CORPUS),c["hash"])

if __name__=="__main__":
    unittest.main()
