#!/usr/bin/env python3
"""Exact TOROID-5 deterministic commit clock for TOPH CORTEX.

Literal cell: {{ . | | | | . }}
Five exact transfer intervals; commit only at 5/5; then wrap to next-cycle 0.
This schedules WHEN a candidate may commit. Existing Sapphon/referee rules decide WHETHER.
"""
from fractions import Fraction

TRANSFER = Fraction(1, 5)
PHASES = tuple(Fraction(i, 5) for i in range(6))

class Toroid5:
    def __init__(self):
        self.index = 0
        self.commits = 0

    @property
    def phase(self):
        return Fraction(self.index, 5)

    def step(self):
        if self.index >= 5:
            raise RuntimeError("cycle closed; wrap before stepping again")
        self.index += 1
        committed = self.index == 5
        if committed:
            self.commits += 1
        return self.phase, committed

    def wrap(self):
        if self.index != 5:
            raise RuntimeError("wrap requires 5/5 closure")
        self.index = 0
        return self.phase

def mother_nature_gate(neg=-1, zero=0, pos=1):
    return neg + zero + pos == 0

def selftest(cycles=10000):
    c=Toroid5()
    for _ in range(cycles):
        for n in range(1,6):
            phase, committed=c.step()
            assert phase == Fraction(n,5)
            assert committed == (n==5)
        assert c.wrap() == 0
    assert c.commits == cycles
    assert mother_nature_gate()
    return {"cycles":cycles,"steps":cycles*5,"commits":c.commits,"phase_error":Fraction(0,1)}

if __name__ == "__main__":
    print(selftest())
    print("0e / TOPH CORTEX TOROID-5 PASS")
