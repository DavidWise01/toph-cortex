# JANE 042 / Gap Escrow

Canonical structure: 1 tensor, 1 Jane, 1 brace, 2 waldos `{-()+}`, 1 box, 1 toroid, 27 occupied positions, and three ternary mode labels `−1,0,+1`. Preserve the `27 → 27.5 → 1` symbolic seam and wave `{([111222333444555555444333222111])}`.

This directory contains an executable **compact GitHub edition** of the JANE042 experiment, 30 separate regression checks, and interactive HTML. The originating conversation also provides a complete ZIP with the **original 46-test implementation**; CI execution of the GitHub version has not been verified.

Run locally:
```sh
python -m unittest -q
python model.py
```

Open `index.html` in a browser to step through the same four-payload escrow concept.

## Checked invariant

`A[-] → B[+]`, `A[+] → B[-]`, `B[-] → A[+]`, and `B[+] → A[-]` move one signed payload at a time. First move it from its origin to the symbolic `[0]` escrow, setting its occupied source slot to zero; then move it from escrow to its destination. Every state update is appended to one fsynced JSONL journal. Every subsequent stage can be reconstructed by reopening that journal. Repeated requests have no additional effect.

The combined squared-amplitude proxy is `registers + fixed spatial fields + escrow`, always **741.3125** under the staged model. During a stage, the occupied registers alone need not conserve this value. Immediately after all four payloads are staged, the occupied registers + fields have **654.3125** and the escrow has **87.0**. At completion the escrow is empty and the registers + fields return to **741.3125**.

This is **logical accounting conservation**, not physical proof of energy storage in the zero gap or actual quantum tunnelling. A single shared journal and complete untorn writes are assumptions. Lost escrow data, concurrent uncoordinated writers and independent two-peer storage are outside this experiment.

**Next bound: JANE043 split escrow without a central durable record.**
