# T1-V6 — Effect-B go/no-go gate (cheap nonlinear probe): **NO-GO**

Result: `T1_v6_reservoir_probe.json`. Diagnostic: `scripts/diagnose_reservoir.py`.
Purpose: decide — with ~half a day, not multi-day — whether to build a full nonlinear
connectome-constrained forecaster to resolve Effect B.

## The probe
A reservoir / echo-state network (nonlinear tanh recurrent dynamics, only a linear readout
trained) driven by real Kato-2015 activity, forecasting H=10 steps ahead. Pre-registered gate:
**GO** iff base forecast FPS > 0.15 AND high-sparsity engram margin > +0.05; else **NO-GO**.

## What happened (and the critical diagnostic)
- Free-run forecast FPS = 0.000 on all worms. That looked like a dead instrument, so — per the
  don't-trust-a-broken-instrument rule — we diagnosed before deciding.
- **Teacher-forced diagnostic (`diagnose_reservoir.py`): the reservoir readout DOES learn.**
  10-step-ahead R² vs the mean-null is **+0.52 (worm 0), +0.41 (worm 4)** — genuine nonlinear
  predictive signal. So the free-run 0.00 was compounding divergence (an instrument issue), NOT
  a weak reservoir.
- **The decisive fact:** R² vs the **persistence** null is strongly **negative** (−1.6, −0.07),
  and persistence beats the mean-null by +0.82 / +0.45. I.e. for this smooth, highly
  autocorrelated calcium data, "predict no change" is near-optimal and a learning nonlinear
  model does **not** beat it at these horizons.

## Why this makes NO-GO the correct, robust call
The reason Effect B cannot be established on real Kato activity is **not** a weak model (we
confirmed a nonlinear model that genuinely learns, +0.5 vs mean). It is that **forecasting this
data above the trivial persistence baseline is genuinely hard**, so there is no "function"
headroom in which structured-vs-uniform compression could differentiate. A multi-day forecaster
would hit the same persistence wall. Spending days here is not warranted.

## Decision (final)
- **NO-GO: do not build the multi-day forecaster. Effect B is dropped for good** on the
  evidence available (V4 model-flip + V5 no-headroom + V6 persistence-wall with a *confirmed-
  learning* nonlinear model). This is a well-evidenced negative, not an untested abandonment.
- Revisit ONLY if a future dataset provides activity with real forecast headroom over
  persistence (e.g. stimulus-evoked / behaviorally-rich recordings, finer temporal resolution),
  where a connectome model could plausibly beat the trivial baseline. Logged as conditional
  future work.

## Banked from this probe
- A working reservoir forecasting harness + the teacher-forced diagnostic.
- A clean methodological result: **on slow whole-brain calcium, persistence is a near-ceiling
  baseline for short-horizon forecasting** — important for anyone scoring connectome models on
  this data, and a caution the field's dynamics-prediction claims should address.
