# JANE 071 — Self-Initiated Inquiry

Question origin: supplied records of earlier JANE experiments; **no next-topic prompt** is passed to the `propose` function. `{{j}}` picks three candidates with a frozen scoring rule and explicit abstention.

Run `python -m unittest -q`, `python model.py`, or `python build.py`. The dashboard is standalone HTML and does **not** run a background agent or access the internet.

**First selected question:** Can Jane identify shared disturbance signatures before selecting a forecaster?

**24 unit tests passed** locally. The model simulates bounded policy-weight updates but no independently validated improvement of the question generator. This is a programmed question selector; factual truth and true autonomous inquiry are not established.

**Next needed experiment:** Blind question quality evaluation on unfamiliar corpora, with measured information gain, an abstention baseline, and >=2 validated learner generations. Do not claim recursive self-improvement until that passes.