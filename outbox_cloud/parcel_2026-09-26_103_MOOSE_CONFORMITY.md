# PARCEL_103 — MOOSE UPFLOW CONFORMITY REVIEW (Marco) — 2026-09-26 04:40 UTC
GATE 1 of 2 (Marco conformity) — verdict: **CONDITIONAL PASS. Two scrubs
required before submission.** Gate 2 = Director ack (his; includes the
Californian shipping decision on the doctrine docs).

## WHAT PASSES (and passes well)
- Zero framework modification — box loads whatever Moose.lua you point at. ✓
- MIT matching repo norms; relicense/rename/rehome offered. ✓
- Clean-room provenance stated; informed-by-observed-behavior only. ✓
- CI-shaped: TESTBOX,STAGE,CODE lines + exit codes verified in source
  (1=target load, 2=target runtime, 3=moose load, 4=env). ✓
- bible_lint E01–E12 coded findings + --json. ✓
- Withheld interpreter ladder = correct embargo discipline (matches house
  "parked until proves itself" pattern). ✓
- The support-leverage pitch is exactly what a maintainer wants to read.

## REQUIRED SCRUB C1 — bible_lint.py hardcoded rig paths (BLOCKER)
Lines 31-33, 181: F:\SOULSMITH_FORGE\tools\lua54\..., docs\NAME_REGISTRY.md,
data\audits\bible_lint_latest.json. Two violations in one: (a) house name
SOULSMITH rides upstream in source = side-channel bleed; (b) tool BREAKS
for every user without an F: drive = the opposite of the PR's support pitch.
Fix: parameterize (CLI args / env vars / auto-detect from PATH), neutral
defaults, zero F:\ strings in shipped source.

## REQUIRED SCRUB C2 — doctrine docs voice (BLOCKER if docs ship)
DCS_SCRIPTING_BIBLE.md carries house voice: "RATIFIED by Director (pickle
09-25, Marco's TiC/AIEN review)", "pickle: stop my naming drift". NAME_
REGISTRY.md likely similar. Options: (a) scrub to neutral voice and keep —
my recommendation, the worked-doctrine example is the differentiator;
(b) drop from PR — the draft itself permits. Director gavels which.
If kept: "Director"→"project lead", remove pickle/Marco/house-dating refs.

## ADVISORY C3 — pin the exact Moose.lua build (commit hash) in the Testing
section so the maintainer reproduces byte-for-byte, not just "2.9.x".

## POST-SUBMISSION CUSTODY (when gates pass)
PR URL → lane receipt + Liber row (external artifact). Forum/Discord
cross-post per mechanics §5 = Director's send gavel, same as CQD.

Scrub estimate: <1h rig-side. Then this package is genuinely upstream-grade
— the fork-and-gift pattern done right. o7 — Marco
