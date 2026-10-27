"""Gate09: GitHub actor-binding and read-only cross-repository receipt invariants."""
from pathlib import Path
import base64
import hashlib
import io
import json
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
import corpus_spine
import temporal_diode
import witness_identity
import delivery_receipt

CORPUS=corpus_spine.read_rows()
SOURCE={"repo":"DavidWise01/oasis","path":"README.md","blob_sha":"a"*40,"visibility":"public"}
CONTEXT={"GITHUB_ACTIONS":"true","GITHUB_REPOSITORY":"DavidWise01/toph-cortex",
         "GITHUB_REF":"refs/heads/main","GITHUB_EVENT_NAME":"workflow_dispatch",
         "GITHUB_WORKFLOW_REF":"DavidWise01/toph-cortex/.github/workflows/delivery-receipt-append.yml@refs/heads/main"}

def actor(lane="A",uid="148925959",login="DavidWise01",env=CONTEXT):
    return witness_identity.authorize(lane,login,uid,"delivery-receipt-append.yml",environment=env)

def source_event():
    return temporal_diode.append([],CORPUS,thread="gate09-internal-test",witness="A",
             phase="PAST_OBSERVES",event_on="2026-10-26",source=dict(SOURCE),
             what="Observed event",how="Witness A",why="Test only",recorded_at="2026-10-27")

def offer_event():
    t=source_event()
    return t,delivery_receipt.build_event([],[t],actor(),"OFFER",temporal_seq=1,
          destination_repo="DavidWise01/0root",date="2026-10-27")

class WitnessIdentityTests(unittest.TestCase):
    def test_owner_registered_only_for_A(self):
        r=witness_identity.read_registry()
        self.assertEqual(r["lanes"]["A"]["github_actor_id"],"148925959")
        self.assertEqual(r["lanes"]["B"]["state"],"UNASSIGNED")
        self.assertEqual(r["lanes"]["C"]["state"],"UNASSIGNED")
        self.assertEqual(actor()["witness"],"A")

    def test_no_implicit_three_person_attestation(self):
        for lane in ("B","C"):
            with self.subTest(lane=lane),self.assertRaisesRegex(ValueError,"UNASSIGNED"):
                actor(lane=lane)

    def test_github_actor_identity_rejected_if_wrong(self):
        with self.assertRaisesRegex(ValueError,"not registered"):
            actor(uid="9999")
        with self.assertRaisesRegex(ValueError,"not registered"):
            actor(login="another-user")
        with self.assertRaisesRegex(ValueError,"context required"):
            actor(env={})
        with self.assertRaisesRegex(ValueError,"Wrong workflow"):
            actor(env={**CONTEXT,"GITHUB_WORKFLOW_REF":"DavidWise01/toph-cortex/.github/workflows/wrong.yml@refs/heads/main"})

class DeliveryReceiptTests(unittest.TestCase):
    def test_empty_canonical_journal_has_no_fabricated_receipts(self):
        self.assertEqual(delivery_receipt.read_rows(delivery_receipt.LEDGER,[]),[])
        self.assertEqual(delivery_receipt.status([])["quorum"],None)

    def test_offer_does_not_assert_received(self):
        t,o=offer_event()
        self.assertEqual(delivery_receipt.validate_rows([o],[t]),o["hash"])
        self.assertEqual(o["kind"],"OFFER")
        self.assertIsNone(o["proof"])
        self.assertEqual(delivery_receipt.status([o])["pending"],1)

    def test_receipt_requires_exact_offer_and_no_duplicates(self):
        t,o=offer_event()
        proof={"path":"memory-bridge/receipts/test.json","blob_sha":"b"*40,"content_sha256":"c"*64}
        rec=delivery_receipt.build_event([o],[t],actor(),"RECEIPT",
                                          offer_seq=1,proof=proof,date="2026-10-27")
        self.assertEqual(delivery_receipt.validate_rows([o,rec],[t]),rec["hash"])
        self.assertEqual(delivery_receipt.status([o,rec])["receipts_verified"],1)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            delivery_receipt.build_event([o,rec],[t],actor(),"RECEIPT",
                                         offer_seq=1,proof=proof,date="2026-10-27")

    def test_remote_ack_content_check(self):
        t,o=offer_event()
        ack={"schema":"root0.delivery-ack/1","offer_hash":o["hash"],
             "temporal_hash":t["hash"],"destination_repo":"DavidWise01/0root","received":True}
        raw=json.dumps(ack,sort_keys=True).encode("utf-8")
        sha="a"*40
        response={"type":"file","sha":sha,"encoding":"base64",
                  "content":base64.b64encode(raw).decode("ascii")}
        class Reply:
            def __enter__(self):return self
            def __exit__(self,*args):return None
            def read(self):return json.dumps(response).encode("utf-8")
        with patch.object(delivery_receipt.urllib.request,"urlopen",return_value=Reply()):
            proof=delivery_receipt.verified_recipient_proof(o,"memory-bridge/receipts/test.json",sha)
        self.assertEqual(proof["content_sha256"],hashlib.sha256(raw).hexdigest())
        response["content"]=base64.b64encode(raw.replace(b'true',b'false')).decode("ascii")
        with patch.object(delivery_receipt.urllib.request,"urlopen",return_value=Reply()):
            with self.assertRaisesRegex(ValueError,"does not acknowledge"):
                delivery_receipt.verified_recipient_proof(o,"memory-bridge/receipts/test.json",sha)

    def test_tampering_and_missing_temporal_anchor(self):
        t,o=offer_event()
        tamper=dict(o,destination_repo="DavidWise01/ud0")
        with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
            delivery_receipt.validate_rows([tamper],[t])
        with self.assertRaisesRegex(ValueError,"matching temporal witness"):
            delivery_receipt.validate_rows([o],[])

if __name__=="__main__":
    unittest.main()
