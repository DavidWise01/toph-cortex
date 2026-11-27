# HJC-023 — Directional force tolerance

ROOT0 · .dlw

Executed NumPy extension of HJC-022 spectrum.py: H(delta)=H+delta*Z_A Z_B/4, delta 0..2 step .02, g 0..2 step .005, angular boundaries 360/720 degrees. 81002 states evaluated, 304 vectorized assertions passed (three norm/probability bounds per delta and isotropic control). Worst sampled leakage for delta 0,.1,.3,.5,1,1.5,2: 1.4433e-15,.00035197362147,.00355063648778,.01000775387918,.03596181643553,.05868659929512,.09557665953603. First sampled exceedances of .001,.01,.05 leakage at delta .18,.50,1.26 respectively; .1 not exceeded on grid. All six listed nonzero samples have worst leakage at 720 degrees. Finite sampled boundaries only, not continuous-time tolerance or physical force calibration. Four-spin model, 729-site spatial dynamics not implemented. Phase III 7/8. Next: integrated source freeze and qualification boundary. Python executed; Rust/Pages not verified. Append only.
