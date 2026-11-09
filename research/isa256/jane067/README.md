# JANE 067 — Verified 600-Address Primitive + Two-Second Forecast

**Verified:** 30/30 Python regression checks passed. Exhaustively tested all 600 nested tuple addresses. Connected 45 legacy forecast leaves injectively into the 600-address prim without modifying JANE 065 predictions.

```text
JANE {{j}} > PRIM 10×5×4×3×1 = 600 addresses
                       45 routed forecast leaves  +  555 available addresses
                      > {{-+-+-+}} ternary-symbol carrier
                      > emit forecast at time t for t+2 s
                      > wait for actual observation at t+2 s
                      > compare absolute error > threshold? -1 freeze : continue
```

Prim coordinates `(a,b,c,d,e)` satisfy `(0≤a<10, 0≤b<5, 0≤c<4, 0≤d<3, e=0)`. Mixed-radix encoding is `((((a*5+b)*4+c)*3+d)*1+e)`. The 45 historical `(x,y,z)` branches map to `(x,y,z,0,0)` for `x<5, y<3, z<3`; the injective mapping is **a design choice**, not derived necessity. Thus the remainder of the prim is unallocated, not 555 extra agents. `10^5^3^1` is preserved as the user’s symbolic notation; arithmetic uses the explicit 600-product.

Python: `python -m unittest -q` then `python model.py`. `legacy065.py` is a frozen copy of the previous executed JANE 065 forecaster. Comparison runs use same observations, horizon, and stopping threshold. Default no-halt run: 112 settled, 8 pending, matching MAE 0.868448; strict threshold 0.75: same -1 failure at 2250 simulated ms, error 0.772025. Never reinterpret simulated-time execution as future messages or hard real-time; the browser is a visual approximation.

Canonical 27-position root geometry and the `27 → 27.5 → 1` seam remain unchanged. Forecast addresses are separate from root geometry. The user’s 6×6×6 hive and helix are also separate layers; no untested bijection is asserted.

**Next real experiment:** evaluate whether allocating some of the 555 available addresses to *genuinely different* forecasters improves holdout accuracy under fixed compute/time budget; if not, keep the frozen 45-leaf model.