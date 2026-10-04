# Sapphon Prime Primitive 01 / 05

**Name:** Anti-stropic Sync / Author-Provenance Residual  
**Status:** APPEND-ONLY descendant primitive  
**Ordinal:** 1 of 5 Sapphon Prime primitives

## Literal gate

```text
..||..|i{why::ok::yes::no::mark dead::start new {{-1,0,+1}}4
```

Local meaning:

- `..||..` — protected / buffered boundary
- `|i` — local observer / instance
- `why` — inspect / explain cause
- `ok` — valid / continue
- `yes` — accept branch
- `no` — reject branch
- `mark dead` — terminate that branch only
- `start new` — append a fresh branch
- `{{-1,0,+1}}4` — four ternary control positions

Invariant:

```text
dead branch != dead system
```

A rejected branch is marked dead; the next branch is appended. Existing committed lineage is not overwritten.

## Anti-stropic sync

```text
(x-3, y+2) :: (x+2, y-3)
```

Pairwise residual:

```text
(-3 + 2, +2 - 3) = (-1, -1)
```

Model-local coordinates:

- `x` — compressed time coordinate
- `y` — author / provenance coordinate

The two opposed transforms cancel the redundant motion and retain a one-step residual on both coordinates:

```text
R = (-1_time, -1_provenance)
```

The residual is never anonymous. Bind it to author identity and path provenance:

```text
R* = (-1_time, -1_provenance, AuthorID, H_path)
```

Therefore:

```text
same compressed state != same provenance
```

unless the bound provenance commitment also agrees.

## Me-to-me carrier

Canonical carrier:

```text
.|.| -+ |.|.
```

Expanded register:

```text
1 2 1 2 -1 +1 1 2 1 2
```

Interpretation:

```text
box carries -> toroid turns -> box reconstructs
```

The center balances:

```text
-1 + 1 = 0
```

while the path remains nonzero. The second invariant `1212` may be referenced rather than regenerated when unchanged:

```text
[1212] [-+] [REF 1212]
```

## Protector rule

```text
inspect -> decide locally -> kill only bad path -> append fresh path
```

Task creation is not a global transport barrier. A local stop pauses only its own dependency branch unless explicitly promoted to a commit gate.

## Boundary

This primitive specifies software / symbolic transport, compression, provenance, and branch-control semantics. Terms such as toroid, gravity, force, or physics remain analogical/model-local unless separately supported by empirical physical evidence.
