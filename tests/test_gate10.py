"""Gate 10: synthetic Ed25519 crypto tests. Never commit synthetic keys or attestations."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
import corpus_spine
import temporal_diode
import witness_attestation as attest

def fixture():
    sk=Ed25519PrivateKey.generate()
    pub=sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    kid=hashlib.sha256(pub).hexdigest()
    row={"witness":"A","github_actor_id":"148925959",
         "public_key_b64":base64.b64encode(pub).decode(),"key_id":kid,
         "enrolled_on":"2026-10-27"}
    return sk,kid,row

def temporal():
    c=corpus_spine.read_rows()
    s={"repo":"DavidWise01/oasis","path":"README.md","blob_sha":"a"*40,"visibility":"public"}
    e=temporal_diode.append([],c,thread="test-signer",witness="A",phase="PAST_OBSERVES",
      event_on="2026-10-26",source=s,what="Observation",how="Instrumented",
      why="Provenance",recorded_at="2026-10-27")
    return e

class CryptoWitnessAttestation(unittest.TestCase):
    def test_no_enrolled_real_keys_and_no_fabricated_proofs(self):
        self.assertEqual(attest.public_keys(),{})
        self.assertEqual(attest.read_rows(attest.LEDGER,{"TEMPORAL":[],"DELIVERY":[]},{}),[])

    def test_ed25519_valid_signature_survives_replay(self):
        sk,kid,key=fixture();e=temporal();sources={"TEMPORAL":[e],"DELIVERY":[]}
        signable=attest.message("A","TEMPORAL",1,e["hash"],kid)
        sig=base64.b64encode(sk.sign(signable)).decode()
        result=attest.append([],sources,{kid:key},witness="A",stream="TEMPORAL",seq=1,
                              key_id=kid,signature_b64=sig,recorded_at="2026-10-27")
        self.assertEqual(attest.verify_rows([result],sources,{kid:key}),result["hash"])
        self.assertEqual(result["signed_payload_sha256"],hashlib.sha256(signable).hexdigest())

    def test_wrong_signature_rejected(self):
        sk,kid,key=fixture();e=temporal()
        bad=base64.b64encode(Ed25519PrivateKey.generate().sign(attest.message("A","TEMPORAL",1,e["hash"],kid))).decode()
        with self.assertRaisesRegex(ValueError,"signature"):
            attest.append([],{"TEMPORAL":[e],"DELIVERY":[]},{kid:key},
                 witness="A",stream="TEMPORAL",seq=1,key_id=kid,signature_b64=bad)

    def test_cross_stream_replay_rejected(self):
        sk,kid,key=fixture();e=temporal()
        signature=base64.b64encode(sk.sign(attest.message("A","TEMPORAL",1,e["hash"],kid))).decode()
        with self.assertRaisesRegex(ValueError,"signature"):
            attest.append([],{"TEMPORAL":[e],"DELIVERY":[e]},{kid:key},
                 witness="A",stream="DELIVERY",seq=1,key_id=kid,signature_b64=signature)

    def test_witness_mismatch_rejected(self):
        sk,kid,key=fixture();e=temporal()
        sig=base64.b64encode(sk.sign(attest.message("A","TEMPORAL",1,e["hash"],kid))).decode()
        with self.assertRaisesRegex(ValueError,"different witness"):
            attest.append([],{"TEMPORAL":[e],"DELIVERY":[]},{kid:key},
                 witness="B",stream="TEMPORAL",seq=1,key_id=kid,signature_b64=sig)

    def test_changed_subject_invalidates_attestation(self):
        sk,kid,key=fixture();e=temporal();src={"TEMPORAL":[e],"DELIVERY":[]}
        sig=base64.b64encode(sk.sign(attest.message("A","TEMPORAL",1,e["hash"],kid))).decode()
        result=attest.append([],src,{kid:key},witness="A",stream="TEMPORAL",seq=1,
                       key_id=kid,signature_b64=sig,recorded_at="2026-10-27")
        modified=dict(e,hash="f"*64)
        with self.assertRaisesRegex(ValueError,"source hash"):
            attest.verify_rows([result],{"TEMPORAL":[modified],"DELIVERY":[]},{kid:key})

    def test_registry_rejects_duplicate_or_unbound_key(self):
        sk,kid,key=fixture()
        obj={"schema":"root0.witness-keys/1","revision":1,"keys":[key,key]}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"public.json"
            path.write_text(json.dumps(obj),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                attest.public_keys(path)
            obj["keys"]=[{**key,"witness":"B"}]
            path.write_text(json.dumps(obj),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"matching witness actor"):
                attest.public_keys(path)

if __name__=="__main__":
    unittest.main()
