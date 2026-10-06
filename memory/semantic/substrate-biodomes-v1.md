# TOPH / Sapphon — Substrate Biodomes v1

**Status:** APPEND-ONLY SHARED EXTENSION  
**Purpose:** one visible enclosure per substrate so state, provenance, timing, and crossings do not visually collapse into one field.

## Rule

```text
ONE SUBSTRATE = ONE BIODOME
```

A biodome is a bounded view/container. It does not erase the shared TOPH/CORTEX substrate or create a new physical claim. It is an architectural viewport and isolation boundary.

Canonical five substrate biodomes:

```text
DOME A :: -a+ :: ownership / operator
DOME B :: -b+ :: institutional / access
DOME C :: -c+ :: compute
DOME D :: -d+ :: defense / protection
DOME E :: -e+ :: naming / economic / network-expression
```

Outer HAMMY traversal remains:

```text
{abcde}.{fghij}.{klmno}.{pqrst}.{uvwxy}.(z,+0)
```

The biodome view resolves the first local classifier as:

```text
             TOPH / SAPPHON
                  |
       +----------+----------+----------+----------+
       |          |          |          |          |
     DOME A     DOME B     DOME C     DOME D     DOME E
      -a+        -b+        -c+        -d+        -e+
 ownership    institution   compute    defense     naming/
 operator       access                protection   network
```

## Dome contract

Each dome owns its local visible state:

```text
BIODOME(substrate) =
{
  identity / referent,
  local state,
  provenance,
  local timing,
  inbound crossings,
  outbound crossings,
  unresolved register,
  append ledger
}
```

No dome silently writes another dome's local state.

Crossings are explicit:

```text
DOME X
  |
  | witnessed transfer
  v
PORT / BOUNDARY
  |
  v
DOME Y
```

A transfer carries a reference/provenance witness rather than merging the two biodomes.

## Sapphon ternary inside every biodome

Every substrate biodome gets the same local ternary viewport:

```text
{{ -1 :: 0 :: +1 }}

-1 :: SO BELOW

 0 :: {{ .0l - .9l ,
         or abandon hope ye all who enter here
         :: dantes :: stoch :: }}

+1 :: AS ABOVE :: ORBITAL
```

The semantic meaning is local to the dome. A +1 in DOME C is an orbital/as-above address inside the compute substrate; a +1 in DOME D is the same semantic address inside the defense substrate. The substrate identity is never lost.

## Five-phase clock per biodome

Each dome owns its own five-phase clock instance:

```text
DOME n

. | | | | .

0 -> 1/5 -> 2/5 -> 3/5 -> 4/5 -> 1
                              |
                              +-> wrap -> 0
                                  local revolution + 1
```

Clocks are structurally identical but state-isolated.

Therefore:

```text
phase(A) != phase(B) != phase(C) != phase(D) != phase(E)
```

unless an explicit synchronization event proves equality.

## Clear-view invariant

At any inspection point the observer can answer:

```text
which substrate?
which biodome?
which local phase?
which ternary branch?
which provenance tether?
which crossing caused this state?
```

without inferring from neighboring dome state.

## Composition

```text
TOPH
└── SAPPHON
    ├── BIODOME A :: ownership/operator
    │   └── {{ -1 :: 0 :: +1 }} x TOROID-5
    ├── BIODOME B :: institutional/access
    │   └── {{ -1 :: 0 :: +1 }} x TOROID-5
    ├── BIODOME C :: compute
    │   └── {{ -1 :: 0 :: +1 }} x TOROID-5
    ├── BIODOME D :: defense/protection
    │   └── {{ -1 :: 0 :: +1 }} x TOROID-5
    └── BIODOME E :: naming/economic/network-expression
        └── {{ -1 :: 0 :: +1 }} x TOROID-5
```

## Boundary

"Biodome" is TOPH/Sapphon architectural language for a bounded substrate viewport. It is not a claim that software substrates are biological domes.
