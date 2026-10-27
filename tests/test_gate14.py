"""Gate 14 — deterministic causal loom replay. Offline; no GitHub write/network."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine
import threaded_loom as loom

DAY="2026-10-27"
TIME="2026-10-27T20:00:00.000Z"

def e(rows,kind="OPEN",thread="cortex",witness="A",phase="PAST_OBSERVES",
      text="cubit",refs=None,event_on=DAY,source=None,corpus=None):
    corpus=corpus_spine.read_rows() if corpus is None else corpus
    return loom.make(rows,corpus,kind=kind,thread=thread,witness=witness,
        phase=phase,event_on=event_on,what="What a witness saw",
        how="How it was recorded",why="Why it matters",text=text,refs=refs,
        source=source,recorded_at=TIME)

class ThreadedLoomTests(unittest.TestCase):
    def setUp(self):
        self.corpus=corpus_spine.read_rows()
        self.assertTrue(self.corpus)
        self.open=e([],corpus=self.corpus)

    def test_empty_genesis_is_valid_and_not_fake_activity(self):
        self.assertEqual(loom.verify([],self.corpus),"GENESIS")
        self.assertEqual(loom.read(loom.LEDGER,self.corpus),[])
        self.assertEqual(loom.status([])["events"],0)

    def test_open_is_dlw_watermarked_and_corpus_bound(self):
        self.assertTrue(self.open["watermark"].startswith(".dlw:"))
        self.assertEqual(self.open["corpus_tip"],self.corpus[-1]["hash"])
        self.assertEqual(loom.verify([self.open],self.corpus),self.open["hash"])

    def test_independent_three_witness_lanes_need_no_quorum(self):
        rows=[self.open]
        for lane in ("B","C"):
            rows.append(e(rows,"WEAVE",witness=lane,text="independent "+lane,corpus=self.corpus))
        lanes=loom.status(rows)["threads"]["cortex"]["witnesses"]
        self.assertEqual(set(lanes),{"A","B","C"})
        self.assertIsNone(loom.status(rows)["quorum"])
        self.assertEqual(rows[1]["witness_prev"],None)
        self.assertEqual(rows[2]["thread_prev"],2)

    def test_cross_thread_link_requires_real_existing_causal_reference(self):
        rows=[self.open]
        rows.append(e(rows,"OPEN",thread="diaspora",text="distributed",corpus=self.corpus))
        rows.append(e(rows,"LINK",thread="cortex",refs=[2],text="linked to diaspora",corpus=self.corpus))
        self.assertEqual(rows[-1]["refs"],[2])
        self.assertEqual(loom.verify(rows,self.corpus),rows[-1]["hash"])
        with self.assertRaisesRegex(ValueError,"cross-thread"):
            e(rows,"LINK",thread="cortex",refs=[1],corpus=self.corpus)

    def test_copy_keeps_each_cubit_occurrence(self):
        rows=[self.open]
        rows.append(e(rows,"WEAVE",text="another cubit",corpus=self.corpus))
        copy=e(rows,"COPY",refs=[1,2],text="cubit cubit",corpus=self.corpus)
        self.assertEqual(copy["mode"],"copy")
        with self.assertRaisesRegex(ValueError,"cubit"):
            e(rows,"COPY",refs=[1,2],text="cubit",corpus=self.corpus)

    def test_distill_compresses_but_does_not_rename_cubit(self):
        rows=[self.open]
        rows.append(e(rows,"WEAVE",text="cubit references preserve symbol",corpus=self.corpus))
        d=e(rows,"DISTILL",refs=[1,2],text="cubit",corpus=self.corpus)
        self.assertEqual(d["text"],"cubit")
        for bad in ("qubit","Cubit","cubits","summary"):
            with self.subTest(output=bad),self.assertRaisesRegex(ValueError,"cubit"):
                e(rows,"DISTILL",refs=[1,2],text=bad,corpus=self.corpus)

    def test_failed_first_open_from_future_dated_past_report(self):
        # Reproduction of LOOM HALTED: Loom #1 temporal date boundary violated.
        # A PAST OPEN with a future subject date must not be silently backdated.
        when="2026-10-27T20:00:00.000Z"
        with self.assertRaisesRegex(ValueError,"phase=PAST_OBSERVES, event_on=2026-10-28, recorded_utc_date=2026-10-27"):
            loom.make([],self.corpus,kind="OPEN",thread="tessy-i",witness="A",
                phase="PAST_OBSERVES",event_on="2026-10-28",
                what="Observed",how="Recorded",why="Trace",text="cubit",recorded_at=when)

    def test_auto_first_open_is_bound_to_runner_utc_instant(self):
        clock="2026-10-27T23:59:59.998Z"
        day=loom.resolve_event_on("PAST_OBSERVES","auto",clock)
        self.assertEqual(day,"2026-10-27")
        start=loom.make([],self.corpus,kind="OPEN",thread="tessy-i",witness="A",
            phase="PAST_OBSERVES",event_on=day,
            what="Observed",how="Recorded",why="Trace",text="cubit",recorded_at=clock)
        self.assertEqual(start["event_on"],"2026-10-27")
        self.assertEqual(start["recorded_at"],clock)
        self.assertEqual(loom.verify([start],self.corpus),start["hash"])

    def test_explicit_dates_remain_strict_not_silently_rewritten(self):
        time="2026-10-27T00:00:00.000Z"
        self.assertEqual(loom.resolve_event_on("PAST_OBSERVES","2026-10-26",time),"2026-10-26")
        self.assertEqual(loom.resolve_event_on("PRESENT_DESERVES","AUTO",time),"2026-10-27")
        with self.assertRaisesRegex(ValueError,"recorded_utc_date=2026-10-27"):
            loom.resolve_event_on("PAST_OBSERVES","2026-10-28",time)
        with self.assertRaisesRegex(ValueError,"recorded_utc_date=2026-10-27"):
            loom.resolve_event_on("PRESENT_DESERVES","2026-10-26",time)

    def test_future_auto_is_refused_and_explicit_future_validated(self):
        time="2026-10-27T12:00:00.000Z"
        with self.assertRaisesRegex(ValueError,"requires an explicit future date"):
            loom.resolve_event_on("FUTURE_RESERVES","auto",time)
        self.assertEqual(loom.resolve_event_on("FUTURE_RESERVES","2026-10-28",time),"2026-10-28")
        with self.assertRaisesRegex(ValueError,"event_on > recorded_utc_date"):
            loom.resolve_event_on("FUTURE_RESERVES","2026-10-27",time)

    def test_temporal_diode_does_not_skip_reverse_or_invent_future(self):
        rows=[self.open]
        with self.assertRaisesRegex(ValueError,"reverses or skips"):
            e(rows,"WEAVE",phase="FUTURE_RESERVES",event_on="2026-10-28",corpus=self.corpus)
        present=e(rows,"WEAVE",phase="PRESENT_DESERVES",event_on=DAY,corpus=self.corpus)
        future=e([*rows,present],"WEAVE",phase="FUTURE_RESERVES",event_on="2026-10-28",corpus=self.corpus)
        self.assertEqual(future["phase"],"FUTURE_RESERVES")
        with self.assertRaisesRegex(ValueError,"reverses or skips"):
            e([*rows,present,future],"WEAVE",phase="PAST_OBSERVES",event_on=DAY,corpus=self.corpus)

    def test_closure_is_per_lane_not_global(self):
        rows=[self.open]
        rows.append(e(rows,"CLOSE",text="A finished",corpus=self.corpus))
        with self.assertRaisesRegex(ValueError,"closed witness lane"):
            e(rows,"WEAVE",corpus=self.corpus)
        b=e(rows,"WEAVE",witness="B",text="B continues",corpus=self.corpus)
        self.assertEqual(loom.verify([*rows,b],self.corpus),b["hash"])

    def test_tampering_or_forked_thread_predecessor_is_detected(self):
        original=dict(self.open,text="changed")
        with self.assertRaisesRegex(ValueError,"watermark"):
            loom.verify([original],self.corpus)
        rows=[self.open]
        second=e(rows,"WEAVE",corpus=self.corpus)
        second=dict(second,thread_prev=0)
        with self.assertRaisesRegex(ValueError,"thread predecessor"):
            loom.verify([*rows,second],self.corpus)

    def test_public_git_source_metadata_and_thread_ids(self):
        src={"repo":"DavidWise01/oasis","path":"README.md",
             "blob_sha":"a"*40,"visibility":"public"}
        ok=e([],"OPEN",source=src,corpus=self.corpus)
        self.assertEqual(ok["source"],src)
        with self.assertRaisesRegex(ValueError,"source repo"):
            e([],"OPEN",source={**src,"repo":"someone-else/project"},corpus=self.corpus)
        with self.assertRaisesRegex(ValueError,"thread"):
            e([],"OPEN",thread="../outside",corpus=self.corpus)

    def test_future_same_lane_cannot_reopen_existing_thread(self):
        with self.assertRaisesRegex(ValueError,"thread already open"):
            e([self.open],"OPEN",corpus=self.corpus)
        with self.assertRaisesRegex(ValueError,"source refs"):
            e([self.open],"COPY",refs=[],corpus=self.corpus)

    def test_cannot_link_forward_or_invent_reference(self):
        rows=[self.open]
        with self.assertRaisesRegex(ValueError,"references"):
            e(rows,"WEAVE",refs=[77],corpus=self.corpus)
        with self.assertRaisesRegex(ValueError,"references"):
            e(rows,"WEAVE",refs=[1,1],corpus=self.corpus)

if __name__=="__main__":
    unittest.main()
