"""Gate17 STOCHIEON full public kernel envelope; synthetic offline evidence only."""
import copy
import json
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import stochieon_kernel as k

CLOCK="2026-10-27T23:49:00.000Z"
LOOM="9368d3921ec95ad4c1ba02ce79f4bdde89516a1449d69a8f81dfbc1fa3e53780"
CORPUS="f3b41c27321a98f5059c1affc846fcb0ff9b7b4acc0c89c437252dacb29aab57"

def sample(node,result="MATCH"):
    return {"transport":"HTTP_RESPONSE","http_status":200,
        "sent_utc":"2026-10-27T23:48:58.000Z",
        "received_utc":"2026-10-27T23:48:58.143Z",
        "monotonic_rtt_ms":143.0,
        "date_header_utc":"2026-10-27T23:48:58.000Z",
        "content_sha256":"a"*64 if result=="MATCH" else None,
        "git_blob_sha":node["expected_git_blob"] if node["kind"]=="git_file" else None,
        "result":result,"time_quality":k.DATE_QUALITY}

def observe(rows,manifest,node,obs=None):
    return k.make(rows,manifest,kind="OBSERVE",witness="A",actor_id="148925959",
        loom_tip=LOOM,corpus_tip=CORPUS,node_id=node["id"],
        observation=obs or sample(node),recorded_at=CLOCK)

class Gate17Tests(unittest.TestCase):
    def setUp(self):
        self.m=k.read_manifest()
        self.nodes=k.manifest_check(self.m)

    def test_empty_events_do_not_imply_work_done(self):
        self.assertEqual(k.verify([],self.m),"GENESIS")
        self.assertEqual(k.read(m=self.m),[])
        status=k.overview([],self.m)
        self.assertEqual(status["seals"],0)
        self.assertFalse(status["required_coverage_complete"])
        self.assertEqual(status["independent_tsa_timestamp"],"NOT_ATTESTED")

    def test_architecture_encapsulates_named_systems_without_inventory_fantasy(self):
        self.assertEqual(self.m["name"],"stochieon")
        self.assertEqual(set(x["id"] for x in self.m["layers"]),{"K","E","T","X"})
        self.assertGreaterEqual(len(self.nodes),9)
        self.assertFalse(self.m["scope"]["inventory_exhaustive"])
        self.assertFalse(self.m["scope"]["all_public_repos_scanned"])
        self.assertEqual(self.m["contract"]["constant"],"cubit")
        self.assertEqual(self.m["contract"]["watermark"],".dlw")
        self.assertIsNone(self.m["contract"]["quorum"])

    def test_observation_is_dlw_bound_to_manifest_and_source_tips(self):
        node=self.nodes["toph-loom"]
        first=observe([],self.m,node)
        self.assertEqual(first["manifest_sha256"],k.sha(self.m))
        self.assertEqual(first["loom_tip"],LOOM)
        self.assertEqual(first["corpus_tip"],CORPUS)
        self.assertTrue(first["watermark"].startswith(".dlw:"))
        self.assertEqual(k.verify([first],self.m),first["hash"])

    def test_pinned_git_sha_cannot_fake_a_match(self):
        node=self.nodes["toph-loom"]
        o=sample(node)
        o["git_blob_sha"]="f"*40
        with self.assertRaisesRegex(ValueError,"pinned Git blob"):
            observe([],self.m,node,o)

    def test_network_error_cannot_be_approved(self):
        node=self.nodes["0root-ai"]
        o=sample(node)
        o["transport"]="NETWORK_ERROR"
        o["http_status"]=0
        with self.assertRaisesRegex(ValueError,"Network error"):
            observe([],self.m,node,o)

    def test_no_unsigned_http_date_masquerading_as_trusted_tsa(self):
        node=self.nodes["0root-ai"]
        o=sample(node)
        o["time_quality"]="INDEPENDENTLY_SIGNED_TIMESTAMP"
        with self.assertRaisesRegex(ValueError,"trusted timestamp"):
            observe([],self.m,node,o)

    def test_tampered_provenance_is_rejected(self):
        first=observe([],self.m,self.nodes["0root-ai"])
        changed={**first,"node_id":"pages-root"}
        with self.assertRaisesRegex(ValueError,"watermark changed"):
            k.verify([changed],self.m)

    def test_manifest_cannot_be_rewritten_under_existing_watermark(self):
        first=observe([],self.m,self.nodes["0root-ai"])
        modified=copy.deepcopy(self.m)
        modified["display_name"]="Rewritten and retitled"
        with self.assertRaisesRegex(ValueError,"unbound manifest"):
            k.verify([first],modified)

    def test_seal_refuses_a_partial_scope(self):
        first=observe([],self.m,self.nodes["0root-ai"])
        with self.assertRaisesRegex(ValueError,"required kernel node"):
            k.make([first],self.m,kind="SEAL",witness="A",actor_id="148925959",
                loom_tip=LOOM,corpus_tip=CORPUS,
                receipt={"receiver":"DavidWise01/0root","source_seq":1,
                         "source_hash":LOOM,"receipt_sha256":"a"*64},
                recorded_at=CLOCK)

    def test_complete_synthetic_scope_still_requires_receipt(self):
        rows=[]
        for node in self.nodes.values():
            rows.append(observe(rows,self.m,node))
        with self.assertRaisesRegex(ValueError,"requires a verified independent Hallway"):
            k.make(rows,self.m,kind="SEAL",witness="A",actor_id="148925959",
                   loom_tip=LOOM,corpus_tip=CORPUS,recorded_at=CLOCK)

    def test_synthetic_full_seal_is_deterministic_and_not_live_claim(self):
        rows=[]
        for node in self.nodes.values():
            rows.append(observe(rows,self.m,node))
        receipt={"receiver":"DavidWise01/0root","source_seq":1,
                 "source_hash":LOOM,"receipt_sha256":"f"*64}
        seal=k.make(rows,self.m,kind="SEAL",witness="A",actor_id="148925959",
            loom_tip=LOOM,corpus_tip=CORPUS,receipt=receipt,recorded_at=CLOCK)
        self.assertEqual(len(seal["coverage"]),sum(x["required"] for x in self.nodes.values()))
        self.assertEqual(k.verify([*rows,seal],self.m),seal["hash"])
        self.assertEqual(k.overview([*rows,seal],self.m)["seals"],1)
        self.assertFalse(k.overview([*rows,seal],self.m)["witness_votes"])

    def test_cannot_claim_complete_scope_after_one_node_failure(self):
        rows=[]
        for node in self.nodes.values():
            outcome="UNAVAILABLE" if node["id"]=="0root-ai" else "MATCH"
            rows.append(observe(rows,self.m,node,sample(node,outcome)))
        with self.assertRaisesRegex(ValueError,"0root-ai"):
            k.cover(rows,self.nodes)

    def test_actual_http_probe_is_not_called_by_offline_validator(self):
        self.assertEqual(k.verify([],self.m),"GENESIS")
        self.assertEqual(k.DATE_QUALITY,"UNSIGNED_HTTP_DATE_NOT_TRUSTED_TSA")

if __name__=="__main__":
    unittest.main()
