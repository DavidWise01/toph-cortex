# Gate 18 — STOCHIEON Cortex Promotion Registry

Promotion is **non-destructive reference promotion** into the ROOT0/STOCHIEON kernel index. The original GitHub source, history, authorship markers, and per-repository runtime remain unchanged. A promotion here does not invoke `bin/promote.py` on a semantic fact, activate an agent, run any code, create a synthetic witness or assert agreement.

## Verified public Git discovery

| Family | Promoted entries | Source of truth | Evidence class |
| --- | ---: | --- | --- |
| TOPH CORTEX | 1 | `DavidWise01/toph-cortex/bin/cortex.py` | Executable Python overseer source |
| OaSIs Four-Cortex VM Ladder | 4 | `DavidWise01/oasis/kernel/canon/four-cortex-vm-ladder-v01/CANON.json` | Symbolic C1/C2/C3/C4 state-model roles; repository-reported 11/11 checks |
| ud0 i13 Cortex | 1 | `DavidWise01/ud0/world2/i13-v2/06-rust-source/src/cortex.rs` | Executable Rust source, no build attested here |
| Atlas Hyper-Cortex / related nodes | 8 | `DavidWise01/atlas/dlw/packages/*cortex*.dlw/manifest.dlw.json` | Eight canonical `.dlw` symbolic manifests, not running VMs |
| TOROID proof support (not promoted cortex instances) | 6 proof sources | `DavidWise01/toroid-kernel/proof/chonk_{17,18,29,30,31,39}_*.lean` | Formal source references; Lean compilation not verified in this run |

### OaSIs ladder

```text
C1  IPv4       classical bounded route state
 ↓  {{i}}     invariant carrier
C2  IPv6       expanded classical route state
 ↓  {{i}}
C3  quasi-q    candidate / permutation state
 ↓  {{i}}
C4  quantum    coherent relational state

I(T(x)) = I(x)
```

This is the symbolic VM ladder as described in the repository, *not* evidence that protocols or quantum hardware are physically interchangeable. The repository's own `TEST_RESULTS.json` reports 11/11 checks passed; it was not independently rerun during this promotion.

### Atlas

Five Hyper-Cortex levels declare **16, 64, 256, 1,024 and 4,096 symbolic 64-bit VMs** respectively. Three other indexed Atlas nodes are **THE CORTEX (S+14)**, **THE CORTEX CORE (NODE-15)** and **THE CORTEX CORE (65TH AXIOM)**. These are `.dlw`-documented named entities/axiom nodes; none are implicitly promoted to live running agents.

### Deduplication

The `ud0` Rust file and its copy in `agent-0root` have exactly the same Git blob SHA-1: `629282e84e579f54a1fce936243f57c778cf9feb`. They share one promoted source identity, with the second path recorded as a mirror. A matching Git blob is evidence of the same file bytes, **not** of an independent implementation.

## Kernel rule

- **`cubit`** remains the exact lowercase symbolic constant in copy/distill transitions. No replacement with `Cubit`, `cubits` or `qubit`.
- **`.dlw`** identifies provenance for references and their existing original package history. No ownership decision or wholesale reattribution is made here.
- **A/B/C** remain separate independent witness lanes, no votes or quorum. No witness testimony is fabricated by this registry.
- **STOCHIEON v1** remains immutable; this source-pinned extension is a new file, not an in-place edit to its existing signed/frozen manifest.
- **Git files and symbolic models are not running services**. Runtime activation, actual agent jobs, proof compilation and live site checks must be independently established.

## Canonical evidence and verification

The canonical registry is [`cortex-promotions-v1.json`](cortex-promotions-v1.json), containing all 14 entries and the six supporting Lean source pointers. The [validator](../../bin/cortex_registry.py) rejects renamed symbols, false liveness, duplicate IDs, modified source hashes in a purported mirror and invalid family counts.

```sh
python3 bin/cortex_registry.py
python3 -m unittest discover -s tests -p 'test_cortex_registry.py' -v
```

The same source registry is independently **pinned** from `DavidWise01/0root/memory-bridge/cortex-promotions-v1.json`, which identifies the registry's exact Git blob SHA. This is a reference trust boundary, not a receipt from a second human witness.

[GitHub Pages cortex dashboard](https://davidwise01.github.io/persist-cortex/cortices/) reads the public registry and compares its canonical Git blob SHA against the Hallway pin before displaying the entries. Missing or mismatching trust data fails closed.

## Scan limits

The discovery inspected default-branch trees of a selected group of central public repositories: TOPH, OaSIs, `ud0`, `agent-0root`, Atlas, `0root`, the source library, STOICHEION/stoicheion support, several agent/kernel repos and Pages. It is **not** a complete scan of all existing or private repositories. Repositories with cortex-related references only, such as the six TOROID proof files, are not counted as new operational cortex instances. New implementations require another explicitly pinned promotion event/registry successor rather than silently editing the existing promoted sources.
