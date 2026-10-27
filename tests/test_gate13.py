"""ROOT0 Gate 13 referent watermark and network-time evidence (no real probes)."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import referent_watermark as r

URL="https://www.scientificamerican.com/article/openai-just-scooped-human-researchers-on-a-million-dollar-quantum-math-problem/"
WHEN="2026-10-27T18:49:00.000Z"
def event(rows=None,kind="REGISTER",sample=None,source_seq=None,uri=URL,basis="REPORTED"):
    return r.write(rows or [],kind=kind,witness="A",actor_id="148925959",uri=uri,basis=basis,
            what="Public article reference",how="Source link supplied and recorded",
            why="Preserve disputed priority with provenance",author="Scientific American",
            content_sha=None,source_seq=source_seq,sample=sample,observed_at=WHEN)

def network_sample():
    return {"sent_utc":"2026-10-27T18:49:00.000Z","received_utc":"2026-10-27T18:49:00.300Z",
        "rtt_ms":298.5,"http_status":403,"server_date_utc":None,"transport_result":"HTTP_RESPONSE"}

class ReferentDiodeTests(unittest.TestCase):
    def test_empty_genesis_without_fake_network_events(self):
        self.assertEqual(r.verify([]),"GENESIS")
        self.assertEqual(r.read(),[])

    def test_public_register_watermark_replays(self):
        reg=event()
        self.assertEqual(r.verify([reg]),reg["hash"])
        self.assertEqual(reg["referent_id"],r.rid(URL))
        self.assertEqual(len(reg["watermark"]),64)
        self.assertIsNone(reg["content_sha256"])

    def test_actual_http_failure_is_observed_not_success(self):
        first=event()
        measured=event([first],kind="SAMPLE",sample=network_sample(),source_seq=1,basis="OBSERVED")
        self.assertEqual(r.verify([first,measured]),measured["hash"])
        self.assertEqual(measured["sample"]["http_status"],403)
        self.assertIsNone(measured["sample"]["server_date_utc"])

    def test_correcting_source_preserves_history(self):
        first=event()
        correction=event([first],kind="CORRECT",source_seq=1,basis="DISPUTED")
        self.assertEqual(r.verify([first,correction]),correction["hash"])
        self.assertEqual(first["kind"],"REGISTER")

    def test_tamper_and_fake_delay_rejected(self):
        first=event()
        with self.assertRaisesRegex(ValueError,"watermark mismatch"):
            r.verify([{**first,"what":"rewritten"}])
        bad={**network_sample(),"received_utc":"2026-10-27T18:48:00.000Z"}
        with self.assertRaisesRegex(ValueError,"before send"):
            event([first],kind="SAMPLE",sample=bad,source_seq=1)
        fake={**network_sample(),"transport_result":"NETWORK_ERROR","http_status":200}
        with self.assertRaisesRegex(ValueError,"cannot carry"):
            event([first],kind="SAMPLE",sample=fake,source_seq=1)

    def test_refuses_private_and_insecure_probes(self):
        for uri in ("http://www.scientificamerican.com/a","https://127.0.0.1/a",
                    "https://github.com@localhost/a","https://user:password@github.com/a",
                    "https://github.com/a#section"):
            with self.subTest(uri=uri),self.assertRaises(ValueError):
                r.uri_ok(uri)

    def test_hash_not_authorship_or_time_dilation(self):
        one=event()
        self.assertEqual(one["claimed_author"],"Scientific American")
        self.assertEqual(one["basis"],"REPORTED")
        self.assertIsNone(one["sample"])
        self.assertEqual(r.DOMAIN,"ROOT0-WATERMARK-v1")

if __name__=="__main__":
    unittest.main()
