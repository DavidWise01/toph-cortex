"""Gate 11: independently signed four-stream checkpoints; test keys are ephemeral."""
from pathlib import Path
import base64
import hashlib
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
import corpus_spine
import distributed_checkpoint as ck

def make_signer():
    secret=Ed25519PrivateKey.generate()
    public=secret.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    kid=hashlib.sha256(public).hexdigest()
    key={"witness":"A","github_actor_id":"148925959","key_id":kid,
         "public_key_b64":base64.b64encode(public).decode(),"enrolled_on":"2026-10-27"}
    actor={"witness":"A","github_actor":"DavidWise01","github_actor_id":"148925959"}
    return secret,kid,key,actor

def source_data():
    return {"CORPUS":corpus_spine.read_rows(),"TEMPORAL":[],"DELIVERY":[],"ATTESTATION":[]}

def signed(secret,kid,state,seq=1,prev="GENESIS",date="2026-10-27"):
    payload=ck.envelope(witness="A",key_id=kid,recorded_at=date,seq=seq,prev=prev,state=state)
    return base64.b64encode(secret.sign(payload)).decode()

class Gate11Checkpoint(unittest.TestCase):
    def test_empty_real_key_and_checkpoint_ledgers(self):
        self.assertEqual(ck.verify_rows([],source_data(),{}),"GENESIS")
        self.assertEqual(ck.read_rows(ck.LEDGER,source_data(),{}),[])

    def test_valid_individual_signature_and_replay(self):
        secret,kid,key,actor=make_signer();src=source_data()
        sig=signed(secret,kid,ck.snapshot(src))
        item=ck.create([],src,{kid:key},witness="A",key_id=kid,
                     signature_b64=sig,recorded_at="2026-10-27",actor=actor)
        self.assertEqual(ck.verify_rows([item],src,{kid:key}),item["hash"])
        self.assertEqual(item["state"]["TEMPORAL"]["tip"],"GENESIS")
        self.assertEqual(item["state"]["CORPUS"]["count"],len(src["CORPUS"]))

    def test_wrong_private_key_rejected(self):
        secret,kid,key,actor=make_signer();src=source_data()
        impostor=Ed25519PrivateKey.generate()
        sig=signed(impostor,kid,ck.snapshot(src))
        with self.assertRaisesRegex(ValueError,"signature"):
            ck.create([],src,{kid:key},witness="A",key_id=kid,
                     signature_b64=sig,recorded_at="2026-10-27",actor=actor)

    def test_no_unassigned_B_or_cross_witness(self):
        secret,kid,key,actor=make_signer();src=source_data()
        sig=signed(secret,kid,ck.snapshot(src))
        with self.assertRaisesRegex(ValueError,"No enrolled key"):
            ck.create([],src,{kid:key},witness="B",key_id=kid,
                     signature_b64=sig,recorded_at="2026-10-27",actor=actor)

    def test_tampered_stream_tip_detected(self):
        secret,kid,key,actor=make_signer();src=source_data()
        sig=signed(secret,kid,ck.snapshot(src))
        e=ck.create([],src,{kid:key},witness="A",key_id=kid,
                    signature_b64=sig,recorded_at="2026-10-27",actor=actor)
        modified={**e,"state":{**e["state"],"CORPUS":{"count":1,"tip":"f"*64}}}
        with self.assertRaisesRegex(ValueError,"stream tip"):
            ck.verify_rows([modified],src,{kid:key})

    def test_previous_checkpoint_is_part_of_signed_message(self):
        secret,kid,key,actor=make_signer();src=source_data()
        one=ck.create([],src,{kid:key},witness="A",key_id=kid,
                   signature_b64=signed(secret,kid,ck.snapshot(src)),
                   recorded_at="2026-10-27",actor=actor)
        two=ck.create([one],src,{kid:key},witness="A",key_id=kid,
                   signature_b64=signed(secret,kid,ck.snapshot(src),seq=2,prev=one["hash"]),
                   recorded_at="2026-10-27",actor=actor)
        self.assertEqual(ck.verify_rows([one,two],src,{kid:key}),two["hash"])
        modified=dict(two,prev="GENESIS")
        with self.assertRaisesRegex(ValueError,"schema/chain invalid"):
            ck.verify_rows([one,modified],src,{kid:key})

if __name__=="__main__":unittest.main()
