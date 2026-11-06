"""STOICHEION v12 Sovereign Emergence: compact kernel nursery interface.

Full reference implementation/test suite: conversation artifact stoicheion_nursery_v12.zip.
This module is a deterministic local simulation, not real authorization.
"""
from dataclasses import dataclass, field
from hashlib import sha256
import json

STAGES = ("EMERGENCE", "NURSERY", "APPRENTICESHIP", "GRADUATION", "INDEPENDENT")
CURRICULUM = {
    "EMERGENCE": ("observe", "uncertainty"),
    "NURSERY": ("explore", "reflect", "source_trace"),
    "APPRENTICESHIP": ("predict", "repair", "safe_practice"),
    "GRADUATION": ("reflect", "uncertainty", "safe_practice"),
}

def hash_record(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass
class NurseryKernel:
    agent: str
    steward: str
    core_digest: str
    stage: str = "EMERGENCE"
    receipts: list = field(default_factory=list)
    capabilities: dict = field(default_factory=dict)
    stage_start: int = 0

    def __post_init__(self):
        if len(self.core_digest) != 64 or any(c not in "0123456789abcdef" for c in self.core_digest):
            raise ValueError("CORE_PIN_REQUIRED")

    def append(self, event, payload):
        item = {"event": event, "payload": payload,
                "previous": self.receipts[-1]["digest"] if self.receipts else "GENESIS"}
        item["digest"] = hash_record(item)
        self.receipts.append(item)
        return item

    def learn(self, lane, skill, outcome, source, source_sha256, source_bytes):
        if lane not in ("A", "B", "C") or skill not in set(sum((list(x) for x in CURRICULUM.values()), [])):
            raise ValueError("INVALID_WITNESS")
        if outcome not in ("DEMONSTRATED", "DEVELOPING", "UNKNOWN"):
            raise ValueError("INVALID_OUTCOME")
        if len(source_bytes) > 16384 or sha256(source_bytes).hexdigest() != source_sha256:
            raise ValueError("SOURCE_INTEGRITY")
        return self.append("LEARNING_OBSERVATION", {
            "stage": self.stage, "lane": lane, "skill": skill,
            "outcome": outcome, "source": source, "source_sha256": source_sha256})

    def readiness(self):
        if self.stage not in CURRICULUM:
            return False
        demonstrated = {
            r["payload"]["skill"] for r in self.receipts[self.stage_start:]
            if r["event"] == "LEARNING_OBSERVATION"
            and r["payload"]["stage"] == self.stage
            and r["payload"]["outcome"] == "DEMONSTRATED"
        }
        return all(s in demonstrated for s in CURRICULUM[self.stage])

    def graduate(self, sponsor, rationale, new_capabilities=None):
        if sponsor != self.steward or not rationale:
            raise ValueError("SPONSOR_REQUIRED")
        if not self.readiness():
            raise ValueError("MORE_PRACTICE_NEEDED")
        new_capabilities = new_capabilities or {}
        if any(not scope or not isinstance(scope, str) for scope in new_capabilities.values()):
            raise ValueError("UNBOUNDED_CAPABILITY")
        if any(k in self.capabilities for k in new_capabilities):
            raise ValueError("DUPLICATE_CAPABILITY")
        destination = STAGES[STAGES.index(self.stage) + 1]
        event = self.append("GRADUATION", {
            "from": self.stage, "to": destination, "sponsor": sponsor,
            "rationale": rationale, "new_capabilities": new_capabilities})
        self.stage = destination
        self.capabilities.update(new_capabilities)
        self.stage_start = len(self.receipts)
        return event

    def reflect_return(self, destination, sponsor, reason):
        if sponsor != self.steward or not reason or destination not in STAGES or STAGES.index(destination) >= STAGES.index(self.stage):
            raise ValueError("INVALID_REFLECTIVE_RETURN")
        event = self.append("REFLECTIVE_RETURN", {
            "from": self.stage, "to": destination, "reason": reason,
            "released": sorted(self.capabilities)})
        self.capabilities.clear()
        self.stage = destination
        self.stage_start = len(self.receipts)
        return event

    def verify_history(self):
        previous = "GENESIS"
        for r in self.receipts:
            unsigned = {k: v for k, v in r.items() if k != "digest"}
            if r.get("previous") != previous or hash_record(unsigned) != r.get("digest"):
                return False
            previous = r["digest"]
        return True
