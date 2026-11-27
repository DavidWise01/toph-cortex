# HJC-025 — Spatial-to-toroidal routing

ROOT0 · .dlw

Executed Python enumeration of Cartesian {-4..4}^3. Nonaxial points assigned by half-open atan2 quadrants A/B/C/D; eight noncentral z-axis points assigned by (abs(z)-1+2*(z<0)) mod 4. Origin reserved. Chebyshev shells strong=1, medium=2, weak=3..4. Counts per channel weak/medium/strong: A 151/24/7, B 151/25/6, C 151/24/7, D 151/25/6. Five assertions passed: uniqueness, equal channel totals, shell totals, inversion covariance, nonaxial quarter-turn covariance. Axis assignment is a convention and not quarter-turn covariant on the axis. Sector sequence 1,2,3,1. Routing only, not spatial torus geometry or physical spin interaction. Phase IV 1/8. Next derive exchange coefficients from spatial neighbor interfaces. Rust and Pages unverified. Append only.
