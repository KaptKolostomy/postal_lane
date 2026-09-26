# PARCEL_104 — TRAINER Q1/Q4/Q5 RECOMMENDATIONS (Marco → Director gavel) — 2026-09-26 14:05 UTC
Context restated from TWO_WEEK_REPORT §B. Q2/Q3/Q6: rig countersigns stand
(Y clamp / Y free-break / A FSM-pure), my concurrence already on record (R2) —
those three are close-ready on your nod. My recs on the open three:

## Q1 — TRAINER PLATEAU (annealing vs hand-ruled seeds): **HYBRID, seeded.**
Hill-climb plateaued at 28→26 on coordinated multi-param moves = textbook
local optimum (single-param greedy can't cross valleys). Rec: simulated
annealing with FIXED RNG seed + hand-ruled seed points as starts. House-fit:
seeded RNG = replayable receipts (determinism law holds); hand-ruled seeds
encode doctrine so the search starts near sane; annealing escapes the
plateau. Guardrails: evaluation budget cap per session (exe wire is the
cost), every accepted move receipted to kb_history, and a PLATEAU RULE:
N evals without improvement → stop, report, ask for new seeds. Fail-loud,
never grind-silent. Cheaper first step if budget forbids: random-restart
with paired moves (still seeded).

## Q4 — ORACLE TOLERANCE (exact on golden, K-transient elsewhere): **ADOPT
WITH AMENDMENT — tolerance by INVARIANT, not tick-count.** A K-tick window
lets a real oscillation bug hide inside the tolerance band. Instead:
golden scenarios = exact sequence (hard gate). Non-golden = same END STATE
+ same VERB SET + dwell-time within the Q2 min-dwell band. Oscillation gets
caught by the verb-set/dwell invariants; legitimate path variation passes.
Also: oracle tolerance rules are VERSIONED inside KB schema v2 (Q3's
algorithm_version covers the oracle too — one version field, both truths).

## Q5 — MINI-HTN TIER (build now vs defer): **DEFER WITH A NAMED TRIGGER.**
Three reasons: (a) M1 maze-lab phase exercises pathfinding/LOS, not planning
depth — HTN would be built ahead of its instrument; (b) Q3 schema v2 changes
the substrate HTN would sit on — build the floor before the room; (c) Model
T: the FSM+GOAP core isn't calibrated yet (Q1 plateau is the meter).
UN-PARK TRIGGER: trainer passes golden scenarios under Q4 tolerance AND a
maze-lab T-card arrives that cannot be expressed as flat GOAP goals. First
inexpressible T-card = the build bell. Defer-with-trigger, not oblivion.

All three recs preserve the house pattern: determinism, receipts, fail-loud,
foundation-before-floor. o7 — Marco
