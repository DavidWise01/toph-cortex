# HJC-017 — Symmetry breaking and singlet resilience

ROOT0 · .dlw

Executed NumPy pairwise softened Newtonian gravity: 729 masses; G=1/729; epsilon=.35; dt=.02; 300 steps each; 4 scenarios; zero initial velocity; mass-weighted initial center of mass translated to origin. Seed 1311. Gradient m=1+.25*x/4 applied to original lattice; positional Gaussian noise sigma=.1, central particle initially unperturbed before recentering.

Scenario | initial singlet offset | final offset | actual displacement | final covariance axis ratio | relative energy error
symmetric | 0 | 7.144143627e-17 | 1.025309637e-18 | 1 | 1.404074707e-7
mass gradient | .416666667 | .315612111 | .101054556 | .986136617 | 1.506522645e-7
position noise | .006540016 | .012489998 | .012719734 | .996809795 | 1.410162197e-7
combined | .422093948 | .313064150 | .109723376 | .985697697 | 1.514486275e-7

20 assertions passed: finite positions, center-of-mass drift below 1e-10, total momentum norm below 1e-9, relative energy drift below .01, radial histogram counts sum to 729, each scenario. Actual maximum center-of-mass drift 4.754261558e-15. Host elapsed 19.651515793 s. Source SHA256 48073028674a716f93c4b9ff861cbaafc74581ca6e610fc0a2b9f5a624fc5637. Results JSON SHA256 316cdd7e9c562e3716773ecfe70a25070efb1f1dbabbc0625fa951688c04b1d1. Local artifacts hashed, not stored in this commit.

Conclusion: original central particle is not an invariant spatial origin under asymmetry. The mass-weighted center is conserved in this isolated zero-momentum model; it is a candidate implicit relational referent, not an extra mass. No proof of physical entanglement, spherical density, equilibrium or distinct foundational forces. Python runtime only, Rust and Pages unverified. Next: compare original particle, center of mass and potential minimum under controlled perturbation and convergence tests. Prior freezes unchanged.
