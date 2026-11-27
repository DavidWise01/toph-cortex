# HJC-016 — Self-gravitating cubit

ROOT0 · .dlw

Actual NumPy simulation: 729 equal unit masses, initial Cartesian grid -4..4 each axis, G=1/729, softening=.35, velocity Verlet dt=.02, 150 steps each at initial angular velocities 0,.05,.12. No imposed shell radii or fixed central particle. Pair count 265356 per force evaluation. 12 assertions passed (finite positions, central displacement <1e-10, center of mass <1e-10, relative energy error <.001 for each run).

Final covariance axis ratios: .9999999999999993, .988542699327603, .9389494647944118. RMS radii: 4.369555647827842, 4.403612942216481, 4.562261201331513. Central displacements: 2.0886995312147113e-19, 3.6209952459212747e-19, 8.892789782976552e-19. Relative energy errors: 2.6050749445152056e-8, 1.1735381927623145e-8, 8.075734866401951e-7. Host elapsed 6.461826897 s. Covariance isotropy does not establish spherical density; cubic initial symmetry is sufficient for isotropic covariance. No equilibrium, torus, quantum entanglement, or physical Planck time claim. Weak/medium/strong shell labels not used as distinct force laws. Phase II scheduled exploration complete, runtime Rust qualification and persistence integration remain HOLD; not a certified freeze. Next: symmetry breaking, longer integration and radial density diagnostics. Earlier records unchanged.
