# Sapphon — Orbital As-Above / So-Below Extension v1

**Status:** APPEND-ONLY SHARED EXTENSION  
**Parent timing layer:** Sapphon TOROID-5 commit clock  
**Orbital source:** `DavidWise01/oasis/kernel/generative/orbital-tether-v186/`

This extension adds the user's ternary orbital/stoich semantic layer without
mutating Sapphon Prime 01-03 or their frozen descendants.

## Canonical ternary

```text
+1 = AS ABOVE = ORBITAL

 0 = {{ .0l - .9l , or abandon hope ye all who enter here :: dantes :: stoch :: }}

-1 = SO BELOW
```

Canonical ordered form:

```text
{{ -1 :: 0 :: +1 }}

-1 :: so below
 0 :: {{ .0l - .9l , or abandon hope ye all who enter here :: dantes :: stoch :: }}
+1 :: orbital :: as above
```

## Five-phase orbital carry

The `+1` branch inherits the proven five-phase orbital clock from
`OaSIs_Orbital_Tether_v186`:

```text
. | | | | .

0 -> 1/5 -> 2/5 -> 3/5 -> 4/5 -> 1
                              |
                              +-> wrap -> 0
                                  revolution + 1
```

Within Sapphon, this means:

```text
candidate / referent
        |
        v
{{ -1 :: 0 :: +1 }}
        |
        +-- +1 --> orbital / as-above tether
        |
        +--  0 --> .0l-.9l Dante/STOCH liminal register
        |
        +-- -1 --> so-below branch
```

## Zero / STOCH register

The `0` branch is preserved literally as:

```text
{{ .0l - .9l , or abandon hope ye all who enter here :: dantes :: stoch :: }}
```

Interpretation inside this architecture:

- `.0l-.9l` is a bounded local register/address span;
- `dantes` is the named mnemonic/literary overlay supplied by the user;
- `stoch` marks the stochastic/stoichiometric semantic lane name as supplied;
- `0` remains a held/liminal branch until another rule resolves it.

No claim is made here that Dante's literary cosmology is physical orbital
mechanics. The literary label is mnemonic metadata layered over the formal
ternary address.

## Boundary with the orbital proof

The upstream v186 Lean proof establishes:

- five exact discrete observation phases;
- phase closure after five steps;
- revolution carry on wrap;
- symbolic bound/parabolic/unbound energy classification.

This Sapphon extension assigns the **semantic meaning** `+1 = orbital/as above`
to that already-proven timing layer. It does not alter the physical equations
or claim that real orbits move in five jumps.

## Append-only rule

```text
existing Sapphon validity/provenance rule
        |
        v
ternary semantic address
        |
        v
TOROID-5 / orbital phase timing
        |
        v
closure witness
        |
        v
append
```

The clock still controls **WHEN**. Existing Prime/provenance logic still
controls **WHETHER**.
