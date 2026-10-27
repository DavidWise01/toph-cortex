#!/usr/bin/env python3
"""OFFLINE witness key helper; never run key generation in a public GitHub Action.
The private PEM stays on the local machine. Only public_key_b64 + key_id go to Git.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PrivateFormat,PublicFormat,NoEncryption

def generate(witness:str,actor_id:str,dest:Path):
    if witness not in ("A","B","C") or not actor_id.isdigit():raise ValueError("Witness and GitHub actor ID required")
    dest=dest.expanduser()
    if not dest.parent.is_dir():raise ValueError("Create local private directory before generating key")
    key=Ed25519PrivateKey.generate()
    secret=key.private_bytes(Encoding.PEM,PrivateFormat.PKCS8,NoEncryption())
    fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    try:
        with os.fdopen(fd,"wb") as out:out.write(secret)
        if os.name=="posix":os.chmod(dest,stat.S_IRUSR|stat.S_IWUSR)
    except BaseException:
        try:dest.unlink()
        except OSError:pass
        raise
    public=key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    result={"witness":witness,"github_actor_id":actor_id,
            "public_key_b64":base64.b64encode(public).decode(),
            "key_id":hashlib.sha256(public).hexdigest(),
            "enrolled_on":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).date().isoformat()}
    print("PRIVATE PEM written locally:",dest)
    print("Do NOT commit, paste, upload or distribute the private PEM.")
    print("Submit ONLY the following public JSON entry in a reviewed key-registry commit:")
    print(json.dumps(result,indent=2))

def sign(path:Path,payload_b64:str):
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    pem=path.expanduser().read_bytes()
    key=load_pem_private_key(pem,password=None)
    if not isinstance(key,Ed25519PrivateKey):raise ValueError("Expected Ed25519 private key")
    payload=base64.b64decode(payload_b64,validate=True)
    if not (payload.startswith(b'{"domain":"ROOT0-ATTESTATION-v1",') or payload.startswith(b'{"domain":"ROOT0-CHECKPOINT-v1",')):
        raise ValueError("Unexpected signing domain; refuse")
    print(base64.b64encode(key.sign(payload)).decode())

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    gen=sub.add_parser("generate")
    gen.add_argument("--witness",choices=("A","B","C"),required=True)
    gen.add_argument("--github-actor-id",required=True)
    gen.add_argument("--private-out",type=Path,required=True)
    sig=sub.add_parser("sign")
    sig.add_argument("--private-file",type=Path,required=True)
    sig.add_argument("--payload-b64",required=True)
    a=p.parse_args()
    if a.cmd=="generate":generate(a.witness,a.github_actor_id,a.private_out)
    else:sign(a.private_file,a.payload_b64)

if __name__=="__main__":main()
