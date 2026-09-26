# MOOSE UPFLOW PACKAGE — offline scripting feedback box + house doctrine
Offered to FlightControl-Master/MOOSE (develop branch) via PR, pending conformity review. 2026-09-25.

## Contents
- `api_testbox.lua` — offline load/run box: stub DCS env + ED sandbox contract + pinned Moose.lua + target module. Coded output (TESTBOX,STAGE,CODE), exit codes 0/1/2/3/4. Catches dead-load scripts, sandbox violations, and captures MOOSE's own runtime error text WITHOUT launching DCS.
- `stub_env.lua` — auto-stub DCS environment: every missing global becomes a self-documenting recorder stub; reports exactly which engine APIs a framework touches at definition time.
- `load_moose.lua` / `probe_runtime.lua` — the "load MOOSE outside DCS" experiment runners (definition + runtime probes with the Vec2 {x,y} gotcha documented).
- `bible_lint.py` — static linter: charset law, banner/parse failures, MOOSE verb receipts vs the pinned build (automated NewROUTE-trap), sandbox-call audit, fail-closed guard check. E01–E12 coded findings, JSON output.
- `DCS_SCRIPTING_BIBLE.md` + `NAME_REGISTRY.md` — a worked example of a house scripting doctrine built around MOOSE (3 tiers, naming law, MOOSE interop law for FilterPrefixes pattern hazards, activation doctrine). Offered as an OPTIONAL companion doc for mission designers; adaptable to MOOSE's own conventions on review.

## Provenance
Built clean-room on a personal rig; informed by observed behavior only (MOOSE docs warnings, ED MissionScripting.lua contract). No third-party code copied. MIT offered to match repository norms.

## Witnessed results (2026-09-25)
- MOOSE 2.9.x fully defines in 0.14s outside DCS under stubs; runtime probes 6/6 on the harness Lua (5.4).
- Real catches: banner-broken script (silent dead load in DCS), require() stripped by sandbox (silent nil), SPAWN:New missing-template error text captured offline.

## WITHHELD — testing phase incomplete (not part of this offer)
A compiled-interpreter version ladder (Lua 5.4.1–5.5.1, self-built) exists as an
internal compatibility matrix for the box. It is NOT included here: the build
pipeline is still in internal testing and is not offered for upstream until it
passes muster. This offer covers the box + lint (pure source) only.
