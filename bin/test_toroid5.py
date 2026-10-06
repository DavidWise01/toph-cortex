#!/usr/bin/env python3
from fractions import Fraction
from toroid5 import Toroid5, PHASES, mother_nature_gate, selftest

assert PHASES == tuple(Fraction(i,5) for i in range(6))
assert mother_nature_gate(-1,0,1)
assert not mother_nature_gate(-1,0,0)

c=Toroid5()
for n in range(1,6):
    p, commit=c.step()
    assert p == Fraction(n,5)
    assert commit == (n==5)
assert c.wrap() == 0

b=selftest(10000)
assert b["steps"] == 50000
assert b["commits"] == 10000
assert b["phase_error"] == 0
print("0e / TOPH CORTEX TOROID-5 10K CYCLE BENCH PASS")
