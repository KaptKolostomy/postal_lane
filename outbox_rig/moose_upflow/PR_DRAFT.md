# PR DRAFT — FlightControl-Master/MOOSE (develop) — READY, DO NOT SUBMIT YET
Submission gates (both pending): [ ] Marco conformity review · [ ] Director ack.
After gates: fork-branch is already pushed (KaptKolostomy/MOOSE, upflow/scripting-feedback-box).
Submit as: base repo FlightControl-Master/MOOSE, base branch develop, head KaptKolostomy:upflow/scripting-feedback-box.

---

## TITLE
Add offline scripting feedback box: load & test MOOSE-based mission scripts outside DCS

## BODY

### What this adds
A small, self-contained test harness under `Moose Development/testbox/` that lets
mission designers and framework developers **load and run MOOSE-based mission
scripts on a desktop Lua interpreter — without launching DCS** — and get coded,
machine-readable failure output.

It was born from a recurring support pain: mission scripts that "do nothing" in
game, where the actual causes are silent dead-loads (a lost `--` on a banner
comment), sandbox-stripped globals (`require`/`loadlib`/`package` per
`MissionScripting.lua`), or MOOSE errors that only surface mid-mission (e.g.
`SPAWN:New: There is no group declared in the mission editor with
SpawnTemplatePrefix = ...`). All three classes are reproduced and captured
offline by this harness, with the exact error text MOOSE/DCS would emit.

### Files (pure Lua + one Python linter; no MOOSE source is modified)
- `api_testbox.lua` — the box: stub env → ED sandbox contract (parsed from the
  live `MissionScripting.lua`, comments excluded) → pinned `Moose.lua` → target
  script. Emits `TESTBOX,STAGE,CODE,detail` lines; exit codes 0/1/2/3/4 for CI.
- `stub_env.lua` — auto-stub DCS environment. Every missing global becomes a
  self-documenting recorder stub; reports exactly which engine APIs a script or
  the framework touches at definition time. (Doctrine: a tripwire, not a simulator.)
- `load_moose.lua` / `probe_runtime.lua` — experiment runners: (1) can the
  bundle *define* itself outside DCS (yes: 2.9.x fully defines in ~0.14 s;
  first engine dependency at definition time is reported precisely on failure),
  (2) can methods *run* (zone-geometry math executes; the Vec2 `{x,y}` vs
  `{x,z}` gotcha in `ZONE_RADIUS` is documented inline from a real failure).
- `bible_lint.py` — optional static gate: filename/charset law, banner & parse
  checks, **automated MOOSE verb receipts** (parses the pinned `Moose.lua` and
  flags any `CLASS:method` call the build does not define), sandbox-call audit,
  fail-closed guard check. Coded findings E01–E12, `--json` output for CI.
- `HOUSE_SCRIPTING_BIBLE_EXAMPLE.md` + `NAME_REGISTRY_EXAMPLE.md` — optional,
  clearly-marked worked example of a house scripting doctrine built *around*
  MOOSE (naming conventions, activation doctrine, wire format). Offered as a
  companion doc only; happy to adapt, relocate, or drop if it does not fit.

### Why this may belong upstream
- **Support leverage:** most "my MOOSE script doesn't work" reports can be
  triaged by one command + paste of `TESTBOX,...` lines, before touching DCS.
- **CI-shaped:** exit codes + machine lines make it trivial to add script
  smoke-tests to repo automation later.
- **Framework insight:** the stub recorder's "engine APIs touched at load"
  report is a cheap way to see what a MOOSE version actually requires of the
  sandbox across versions/branches.
- **Zero intrusion:** nothing in the framework changes; the box loads whatever
  `Moose.lua` build you point it at (stable, develop, or a PR's generated
  bundle — it already decoded a real `MooseCommitHash` nil-concat on a source
  checkout, distinguishing generated-bundle from source-tree loads).

### Not included (deliberately)
An internal compiled-interpreter compatibility ladder (Lua 5.4.1–5.5.1 matrix).
Still in internal testing; withheld until it passes muster. The offer stands on
the pure-source tooling above.

### Provenance & license
Clean-room personal project; informed by observed behavior only (MOOSE docs'
`FilterPrefixes` pattern warnings, ED's `MissionScripting.lua` contract). No
third-party code copied. **MIT**, matching the repository. Happy to relicense,
rename, rehome (e.g. under a `Tools/` or `Developer/` tree), or split the PR.

### Testing witnessed (2026-09-25, personal rig, Lua 5.4)
- MOOSE 2.9.x bundle: FULLY DEFINES outside DCS; probe 15/15 headline classes.
- Known-bad mission script (banner typo): `TESTBOX,TARGET,E-LOAD ... unexpected
  symbol near '=='` + exit 1 — the exact failure that is silent in game.
- Mission script using `require()`: `TESTBOX,SANDBOX,SBX-STRIPPED ...` before
  load, then the true runtime failure captured verbatim.
- `SPAWN:New` with missing template: MOOSE's own error text captured offline.
- Upstream source-tree check: `Moose_Create.lua` box-run surfaced the
  build-time-only `MooseCommitHash` concat error (generated-bundle vs source
  load distinction).

### Checklist
- [x] No changes to framework source
- [x] Runs on plain Lua 5.4 (no external deps)
- [x] Coded output + exit codes (CI-ready)
- [x] Docs inline; examples included
- [ ] Maintainer guidance on doc placement/rename welcome

---

## SUBMISSION MECHANICS (for the Chief, when gates pass)
1. GitHub → KaptKolostomy/MOOSE → branch `upflow/scripting-feedback-box` → "Contribute" → Open PR
2. base: `FlightControl-Master/MOOSE` / `develop` 3. paste TITLE + BODY above
4. In first comment: link this thread's receipts (matrix runs, capture demos)
5. Cross-post to the MOOSE forum thread + Discord #scripting per community norm
