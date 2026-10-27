"""Gate 12 key lifecycle: synthetic offline Ed25519 keys, no live enrollment."""
import base64
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bin"))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
import key_lifecycle as lc

def key():
    sk=Ed25519PrivateKey.generate()
    p=sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    kid=hashlib.sha256(p).hexdigest()
    meta={"witness":"A","github_actor_id":"148925959","key_id":kid,"public_key_b64":base64.b64encode(p).decode(),"enrolled_on":"2026-10-27"}
    return sk,meta

def signed(sk,*,kind,kid,old=None,seq=1,prev="GENESIS",role="NEW",reason="rotation"):
    message=lc.payload(kind=kind,witness="A",key_id=kid,previous_key_id=old,
        actor_id="148925959",reason=reason,seq=seq,prev=prev,role=role)
    return base64.b64encode(sk.sign(message)).decode()

def add(rows,keys,kind,kid,old=None,new_sig=None,old_sig=None,reason="rotation"):
    return lc.make(rows,keys,kind=kind,witness="A",key_id=kid,previous_key_id=old,
          reason=reason,new_signature_b64=new_sig,old_signature_b64=old_sig,
          recorded_at="2026-10-27",actor_id="148925959")

class LifecycleTests(unittest.TestCase):
    def test_empty_genesis(self):
        self.assertEqual(lc.replay([],{}),{"tip":"GENESIS","active":{},"disabled":set(),"history":{}})
        self.assertEqual(lc.read_rows(lc.LEDGER,{}),[])

    def test_activate_requires_ownership(self):
        sk,k=key();keys={k["key_id"]:k}
        with self.assertRaisesRegex(ValueError,"signature"):
            add([],keys,"ACTIVATE",k["key_id"],new_sig="AA==")
        sig=signed(sk,kind="ACTIVATE",kid=k["key_id"],reason="rotation")
        e=add([],keys,"ACTIVATE",k["key_id"],new_sig=sig)
        self.assertEqual(lc.replay([e],keys)["active"]["A"],k["key_id"])

    def test_dual_signature_rotate(self):
        first,a=key();second,b=key();keys={a["key_id"]:a,b["key_id"]:b}
        act=add([],keys,"ACTIVATE",a["key_id"],new_sig=signed(first,kind="ACTIVATE",kid=a["key_id"]))
        old=signed(first,kind="ROTATE",kid=b["key_id"],old=a["key_id"],seq=2,prev=act["hash"],role="OLD")
        new=signed(second,kind="ROTATE",kid=b["key_id"],old=a["key_id"],seq=2,prev=act["hash"],role="NEW")
        rotate=add([act],keys,"ROTATE",b["key_id"],old=a["key_id"],new_sig=new,old_sig=old)
        final=lc.replay([act,rotate],keys)
        self.assertEqual(final["active"]["A"],b["key_id"])
        self.assertIn(a["key_id"],final["disabled"])
        self.assertEqual(final["history"][a["key_id"]],"ROTATED")

    def test_rotation_without_old_signature_is_denied(self):
        first,a=key();second,b=key();keys={a["key_id"]:a,b["key_id"]:b}
        act=add([],keys,"ACTIVATE",a["key_id"],new_sig=signed(first,kind="ACTIVATE",kid=a["key_id"]))
        new=signed(second,kind="ROTATE",kid=b["key_id"],old=a["key_id"],seq=2,prev=act["hash"])
        with self.assertRaisesRegex(ValueError,"base64"):
            add([act],keys,"ROTATE",b["key_id"],old=a["key_id"],new_sig=new)

    def test_emergency_revoke_is_account_only_and_permanent(self):
        sk,a=key();keys={a["key_id"]:a}
        one=add([],keys,"ACTIVATE",a["key_id"],new_sig=signed(sk,kind="ACTIVATE",kid=a["key_id"]))
        with self.assertRaisesRegex(ValueError,"account-only"):
            add([one],keys,"REVOKE",a["key_id"],reason="lost")
        last=add([one],keys,"REVOKE",a["key_id"],reason="ACCOUNT_RECOVERY_NOT_KEY_SIGNED: lost")
        state=lc.replay([one,last],keys)
        self.assertNotIn("A",state["active"])
        self.assertIn(a["key_id"],state["disabled"])
        with self.assertRaisesRegex(ValueError,"activation"):
            add([one,last],keys,"ACTIVATE",a["key_id"],new_sig="AA==")

    def test_no_backward_history_edit(self):
        sk,a=key();keys={a["key_id"]:a}
        one=add([],keys,"ACTIVATE",a["key_id"],new_sig=signed(sk,kind="ACTIVATE",kid=a["key_id"]))
        altered=dict(one,reason="changed")
        with self.assertRaisesRegex(ValueError,"SHA mismatch"):
            lc.replay([altered],keys)

if __name__=="__main__":unittest.main()
