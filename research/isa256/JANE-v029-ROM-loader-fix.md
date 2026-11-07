# Jane v0.29 — ROM loader repair

Date 2026-11-07. User reported that Jane v0.28 failed to load their NES cartridge.

## Root cause reproduced
The v0.28 browser's script declared `corpus` as a constant and reassigned it after the first NES frame. This raised **Assignment to constant variable** and incorrectly marked the ROM failed after mapper decoding. Changed `corpus` to a mutable variable.

## Additional robustness
- Select a ROM before engine availability; keep it queued until JSNES loads.
- Explicit load stage diagnostics: bytes, JSNES initialization, mapper decoding, first frame, corpus restoration.
- Validate cartridge iNES header and declared PRG/CHR size.
- Three CDN fallback URLs for JSNES v2.1.0; permit explicit local JSNES engine file for offline environments.
- Keep Jane's behavior and the NES runtime decoupled.
- Preserve simple semantic-screen teaching corpus and automatic START recovery.

## Verification
- 16/16 existing semantic tests passed.
- Browser JavaScript syntax check passed.
- Chromium mock-engine integration test passed for queued ROM, subsequent engine ready event, ROM READY / MAPPER 9, PLAY/START, first-frame callback and stage-specific error on a simulated mapper exception.
- The user-provided cartridge has 262,160 bytes and mapper 9 (MMC2).
- **Real JSNES core boot and Punch-Out!! gameplay remain unverified**, because the execution environment could not download the CDN-hosted engine. Do not present the mock integration test as an actual NES gameplay pass.

Executable release is attached to the conversation as `jane_semantic_029.zip`; no copyrighted ROM is published.