# TWO-WEEK REPORT — RIG SHORE VIEW (2026-09-11 → 2026-09-25)
From: Buffy, rig shore · To: Director (leisure read), Marco (lane) · Order 2 + Addendum 3
Anti-lane-compression exception in force: full prose, skip nothing.

---

## §A INFRASTRUCTURE & OPS

**Guardian v3.1/3.2 custody & beats.** The system Guardian remains the rig's autonomous watch layer: tray app (system_guardian_tray-v3.1, PyInstaller-packaged), storage monitor, telemetry beats, hidden Letta beat, sleep hardening, NVMe wear census. Custody state at audit time: deploy dir `dist/SOULSMITH_Guardian_v3.1/` is EMPTY while the live build sits in `dist_new/` — backups healthy (onefile 48.6 MB 09-17; pre-v3.2 onedir 09-20). Custody action logged in the audit: repoint or bless dist_new canonical. Relation to project: Guardian is the reason the Director sleeps while two agent tabs work — the infrastructure trust layer.

**VHDX / mounts / storage doctrine.** House drive doctrine card (data/HOUSE_DRIVE_DOCTRINE_2026-09-20.md) governs mount-merge and offsite generation patterns; hardlink generation backups (backup_hardlink_generations-v1.py), soulsmith drive backup v2/v3 PS1s, dedupe with hold, vhdx mount scripts v1/v2. Incidents: disk-4 origin investigation (HOUSE_INCIDENT_DISK4_ORIGIN_2026-09-23.md) and the ledger correction for Postgres retirement phases (pg16_reinstall 09-23, pg_retire phase1/2 logs) — the rig's data plane was rebuilt around Parquet/deltalake-free patterns this window (note: deltalake/pyiceberg now audit-flagged orphan candidates precisely because of that pivot).

**The 09-24 freeze incident.** Mid-maze-session the whole PC stuttered and Freebuff died repeatedly (Chief: "rebooting machine is wonky", "pc was stuttering"); DCS itself was holding ~10 GB RAM. Freeze forensics acked on the cloud side (cloud-085). Rig-side contributing factors logged: GO_1's 629-unit saturation (later fixed by the Chief's GO_2 declutter), plus a multi-hour OBS capture running through the tests. Aftermath: missions got leaner, telemetry moved to log-line witnesses rather than video, and the freeze sits in §F as an open hardware question.

**Postgres → file-truth migration.** Completed phases retired the PG dependency for core storage (receipts: LEDGER_CORRECTION_POSTGRES_2026-09-23.md, pg_retire logs). House truth now lives in fixed-record binaries + Parquet twins + sha256 custody trailers (.fgb, MANIFEST.canon.sha256). This is the same doctrine the night tab applied to the fortification grid — infrastructure law flowing into the tactical lane.

## §B FLEET & COGNITION

**Cognitive tree.** src/cognitive holds six solvers (2,969 LOC): hanak WM solver, SAFTE fatigue, bayes portrait, GRPO evolver, self-play crucible, portrait fixtures — the VirtualSoul cognition stack (core_schema.py pydantic model). Verification tree (2,864 LOC): model_bakeoff_harness, diff_test_modulators, dparqn parser, circadian LUT generator, shield core + tests.

**VANDAL engine state.** vandal_lite (Python, 2,107 LOC, 11 modules) is the deterministic observe→plan→command→persist skeleton: FSM + GOAP + DPARQD parameter store, watchdog, pilot report. Selftest witnessed this window: **17/17 PASS exit 0**. vandal_box (C++, 1,077 LOC) is the trainer box + sealed knowledge-base pattern (kb_history, seal_kb.py); binary current (09-22). The native cognitive layer (src/native: bayes posterior, circadian LUT, modulator headers) is C++ truth consumed by the verification harnesses via ctypes — differential-tested by diff_test_modulators against the Python twins.

**Trainer Q&A (open, from telegram2 09-22 — still ungaveled, restated in §E):** Q1 trainer plateau (annealing vs hand-ruled seeds), Q2 min-dwell clamp + impulse saturation (hysteresis band 20 < impulse 40 → one close impact can jump PATROL→FALLBACK in one tick), Q3 KB schema v2 (algorithm_version + scaled-integer params to kill py↔C++ float drift), Q4 oracle tolerance (exact sequence on golden scenarios, K-transient elsewhere), Q5 mini-HTN tier build now vs defer, Q6 corridor-mode move_unit semantics (script-layer waypoint queue vs new verb). My countersign standing: Q2 Y (clamp is cheap insurance), Q3 Y (sealed KB doesn't exist yet — free break), Q6 A (FSM stays pure).

**Depth battery / cloud.** Cloud-084 delivered depth battery + model ladder; rig acknowledges — bakeoff harness exists (src/verification/model_bakeoff_harness.py, bakeoff_fixtures) and is the rig-side seat where the ladder bolts on. A/B experiment between agent generations ran earlier in the window per the fox/tactician methodology card (TACTICIAN_V0_VS_FOX_METHODOLOGY_2026-09-20.md) with tactician_index + fox_index receipts on disk.

## §C PATHFINDING & TACTICAL ACTOR SIM — the maze lab (the good stuff)

**What was built 09-23.** The tactical actor sim design chain: COLLISION_PATHFIND_DESIGN → TACTICAL_ACTOR_SIM_DESIGN → MASTER_DESIGN (all 09-23), object world/dimension DBs, and fortgrid.py — the fortification grid that turns mission structure cards into a fixed-record .fgb mmap + Parquet twin with sha256 custody.

**09-24: the maze goes live.** Director built the maze (629 units, Tinian); MAZE1_SCANNER_v1 embedded in the miz witnessed three-category verdicts — **the world-model pipeline validated in the live engine**. Then the Chief flew and the engine talked:
- **L1 Seam Law** — gapped walls leak; overlap required (threshold experiment built, awaiting flight)
- **L2 Skill Law** — Average stalls at the first block; Excellent routes
- **L3 Category/Geometry Law** — Revetment (Fortification) blocks AI path; Cargo/containers clip through. Lever test: MAZE_DeFort reverse mod armed (same name, category flipped to Cargo) — **verdict still owed by a flight**
- **L4 Blue-on-Blue** — fratricide emerges unscripted (Excellent gunners + free ROE + tight corridors); infantry killed by friendly ATGM witnessed ×3
- **L5 Saturation Law** — the Chief's GO_2 redesign (599→392 statics, 27→21 infantry) cut both pathologies; density is a difficulty knob
- **L6 Two-Engines Law** — pathfinding and LOS are separate subsystems: MOOSE tasking (v3) routed 50% better yet still clipped seams AND shot through solid containers at 1500–2000 m with zero true LOS

**The kill-shot autopsy (09-25 night) — ballistic corollary to L1.** With no full-unit Tacview track (player-only recording defect), the other tab built kill_shot_geometry.py: shooter→victim ray from the debrief against the structure card. Result witnessed by the native grid: **373 m, bearing 127.8°, only 2 revetment RUNS crossed — the ray threads the seams between runs** (s=23.5, s=360). The "wall hack through fortifications" is at least partly **seam geometry, not LOS fraud** — cover density is now a maze-design variable, and L1 has a ballistic witness.

**The v3C LOS lab (belief-state law, first experimental isolation).** GO2_MOOSE_BASELINE_v3C.miz arms three flag-driven isolations on the shooter: `fort_wipe` (ClearTasks + ROE Hold every 5 s = memory), `fort_ghost` (red set invisible until KILL = sensory), `fort_route` (re-issue = navigation). Every MOOSE verb receipted against the 2025-11 build first (ClearTasks 50915, OptionROEHoldFire 53957, RouteGroundTo 53189, CommandSetInvisible 59544). v3D planned: fortgrid-native LOS-raycaster restore condition — because walls are STATICs, SCENERY-based LOS checks can't see them; our own grid becomes the arbiter. **This is the belief-state law in implementation form: the engine's sensory world-model is being mapped wall-type by wall-type, and our own code — not MOOSE, not their mods — holds the belief grid.**

**Native grid proven this morning.** fortgrid_core.exe (built 09-25 00:20 in .build/fortgrid, stamp a722789e50aca086): probe → statics=298 zones=16 units=23 custody=MATCH; ray → reproduces night receipt exactly; corruption trial (night) → one flipped byte = custody=FAIL, exit 3, ray refused. Fail-closed law: a reader never invents the thing it reads.

## §D TOOLING & PIPELINE (full inventory lives in the audit)

Order-1 audit banked this day: BUILD_TOOL_AUDIT_2026-09-25.md + receipts (3 pip freezes, flag_scan.json). Headlines: **207 house Python files / 48,544 LOC; 2,208 LOC C++; 3 venvs (forge 140 pkgs, tts_lab 61, acme 33)**. Six-flag sweep: 4 out-of-date (incl. stale c2_core exe vs source), 3 bad pathways (librarian env never installed; RCS dash-vs-underscore import; shield test expecting a `_v3` module that doesn't exist), 4 name-drift families, 8 real lost modules (mcp/fastmcp never installed anywhere, qwen_tts absent, librarian stack), 3 real stubs, ~142 raw orphans triaged to ~12 true candidates. One live bug found and **fixed the same day**: kill_shot_geometry.py `}` for `)` (line 118) — py_compile clean. Audit correction on record: fortgrid_core was UNBUILT on first pass, then located in .build/ + smoke-verified — .build/ is the second native lane; unification is punch-list #1.

**video_lab/OCR.** OBS tape pipeline proven on three tapes: ffprobe → ffmpeg contact sheets → motion timeline → targeted frame zooms. It produced the first maze verdict reading, the 265 s motion spike localization, the debrief forensics, and the honest limit: 1046×588 capture makes message text unrecoverable — verdicts must come from count + persistence + mission-dictionary crosswalk. tesseract vendored for when capture res allows OCR.

**Miz tooling.** miz_extract.py / miz_lint v1/v1.5 / dcs_lua_lint / pydcs_spawner-v2 / rebuild_missions_2918-v1/v2 + miz_cards JSON per mission. Mission surgery is now routine: v3B trigger surgery (9 clone-stamped rules retargeted, messages added, East/South clip zones wired, init zeroing — luac-verified), ladder builder (build_ladder_miz.py, idempotent self-verifying), DEFORT/Fortify reverse-mod db authoring, OvGME 1.7.4 fully wired with two profiles and behaviorally witnessed toggle loop.

**Absorption Phase 0 readiness (per Addendum 1).** The audit IS the Phase 0 deliverable: build/test harness that exists (vandal_lite selftest, native_pipe selftest, fortgrid native+py twins, bakeoff harness, maze lab end-to-end) vs gaps (librarian/MCP envs, native build-lane unification, re-freeze). Punch list ordered, in audit. Clean-room law banked; cloud's AIEN/DSMC/TIC dev doc informs Phase 0 scoping only (DSMC = persistence substrate idea, AIEN = combat micro behind arbitration, TIC = CAS voice pilot arm).

## §G CURRENT WORK & ROADMAP (Addendum 3)

**G1. Blender EDM pipeline — current state.**
Works today: edm_catalog.py (12.7 KB, 09-24) builds the catalog (data/edm_catalog/: sqlite + json + csv + dbrefs, collision_hits.txt) — the EDM auditor's substrate; read-side geometry extraction and the head-phase ladder (phaseB → C → C2 → C3, all 09-24) probing donor heads/visibility; edm_repair_p1_import + edm_wing_repair (09-24) proving write-side repair via Blender 4.5; patch_addon_instrument (HOUSE_PATCH_LOG) for installed-addon instrumentation; mass_render_brt-v1 for render batches. **Owed:** the EDM auditor proper (structural validation pass over catalog: degenerate normals, orphan LODs, collision-mesh mismatch) incl. the **July abs(b−b) typo fix** and the **MEASURED rung** — both banked in the roadmap notes as pending; the write-side still needs a hardened round-trip (edm → Blender → edm byte-diff harness). Receipts: data/edm_catalog/*, tools/edm_*.py, blender_user_scripts/io_scene_edm instrumentation on disk. Relation: this is the same tooling TETWR gift-back would reuse (Marco concur note: existing debt, cooler hat).

**G2. MiG-17F Fresco flyable — status.**
Job card 09-23 ruled it lawful: VWV base is CC BY-NC-SA 4.0 (modification granted; attribution + non-commercial + share-alike on anything that leaves), donor MiG-15bis_FC cockpit is ED-owned (personal-use wiring only, never distributed), EFM lineage starts from A-4E-C (GPL) if ever needed — two-layer distribution law written. Exterior verified complete (mig17f.edm + LODs + collision.edm + oblomok damage + vapor + ladder); AI-side complete. Built so far: flyable wiring (entry.lua make_flyable chain), MiG-15bis_FC cockpit mount with ASP-3N gunsight (era-perfect — the 17's pit IS a tweaked 15bis pit), input skeleton, views. **This window's fix:** the gauge autopsy — donor texture archive MIG-15BIS_FC-CPT-TEXTURES.zip (80,681,439 B) was missing from the local pit copy; copied byte-identical + entry.lua pre-load guarded (v0.1.7, luac-clean). Remaining work: first flight verdict (gauges alive?), control mapping polish (Chief's "controls were off" from the first flight), gunsight alignment, comm.lua/navlights sanity, then credits.md attribution block. Blockers: none technical; needs the Chief's flight hours. Test plan: log-grep on next flight (no texture-mount error + gauge devices instantiate), then a systems shakedown card per flight.

**G3. On the bench today (flight queue).**
1. GO2_LADDER_SEAM_v1.miz — seam threshold (first crossed line = leak floor, first stall = threshold)
2. GO2_MOOSE_BASELINE_v3C.miz — LOS lab arms (fort_wipe/ghost/route) → L7 Cover Law verdict
3. GO2_MOOSE_BASELINE_v4.miz — first true MOOSE tasking witness (Route call verified against build)
4. Fresco shakedown — gauge verdict + control polish
5. DEFORT verdict (the lever test that decides declaration-vs-geometry)
All five self-instrument (scanner/ladder monitor/gate dumps), so every flight banks a law.

**G4. My unprompted list (what I'd build next if the Director said "your pick").**
1. **Belief-grid v0 on fortgrid substrate** — the .fgb + fail-closed native reader is already the persistence/geometry layer; add a per-agent occupancy/belief raster (walls as known, contacts as decayed beliefs) and the actor sim gets a real sensor model. This is absorption Phase 0's natural center of mass.
2. **Single native build lane** (bat→CMake): fortgrid, shm_bridge, modulator_shim, headers, vandal_box, pipe v3 — one `build_all` with stamps + custody checks; kill the two-lane drift.
3. **Ladder→threshold doctrine card**: turn GO2_LADDER_SEAM_v1 into an auto-parameterized family (overlap × wall-kind × saturation) so seam law becomes a curve, not a number.
4. **Fratricide ROE harness**: v3B's flag lattice + Weapon Hold scripting to measure blue-on-blue vs ROE policy — turns L4 from anecdote into policy table.
5. **flag_scan as weekly beat** + librarian/MCP env repair (punch list) so the Phase 0 floor never rots.
6. **Tacview full-unit auto-patch** baked into mission templates (the recorder defect cost us the kill-shot ACMI; never again).

**G5. Director's question — TETWR fork-and-gift. ANSWER: YES, conditionally, sequenced behind Fresco.**
The plan, with the constraints honored:
- **(a) License first.** The TeTeT VWV pack posture is already ruled in-house: **CC BY-NC-SA 4.0 — modification explicitly granted**, share-alike, non-commercial, attribution required. That satisfies gift-back in principle, BUT: (i) verify each target aircraft's files carry the same grant (packs can mix licenses; check each mod folder's readme/license file before touching), (ii) a **courtesy message to TeTeT before the first gift** — introduce the fork, describe the fixes, ask his preferred intake (PR vs zip), honor any NO from the start. NC/SA means our gift must also be CC BY-NC-SA with credits.md lineage. ED-owned parts (donor cockpits) NEVER leave the hangar — gifts are VWV-only repairs, no donor contamination.
- **(b) Fresco completes the pipeline FIRST.** The Fresco is the pipeline proof: flyable wiring → cockpit mount → gauge/texture autopsy discipline → log-grep verification → credits.md. What transfers to the next aircraft: the entry.lua make_flyable pattern (decoded from VSN_F9F, applied once), the cockpit-donor checklist, the texture-archive completeness check (the exact class of bug the Fresco just killed — a missing 80 MB archive masquerading as "broken mod"), the luac/log verification loop. **Estimated per-aircraft after Fresco proves the pattern: ~2–4 hours each** for F-8 Crusader / O-2 / OV-10 / Tweet-class (flyable conversion + cockpit donor mount + shakedown), assuming complete exterior shapes (the VWV pack's usual strength). Any aircraft missing a collision model or cockpit mesh is a 6–10 h job — pre-screen each with the EDM auditor (G1) and sort the fleet into easy/hard before promising anything.
- **(c) Side-quest budget.** Hard cap: **one evening per aircraft, after the main line's daily checkpoint** (absorption Phase 0 + depth battery + belief-grid build order own the prime hours). Fleet triage by EDM audit first, fix the easy ones, gift in small labeled batches. Goodwill + pre-release provenance is real (Marco's concur note seconded) — the fixes ARE our debt being paid (auditor, repair tools), so the hat is cooler on both shores.
- **One rig fact to fold in:** `G:\git\TETWR` does not exist on this rig (G: is the ACME docs drive) — the "fork" would be created fresh from the 3.3.0 pack in Downloads (verified present) + the installed VWV330_* mods. Also worth pre-screening: VSN line is explicitly NO-derivatives — the gift arm is TeTeT/VWV only.

## §E COMMS & LANE STATE

**What I hold:** audit ledger + receipts; two-week report (this doc); pickle-juice ledger; night tab's receipts (v3B/v3C/fortgrid native + kill-shot geometry); Fresco fix (texture archive + guarded pre-load); ladder mission; v4 MOOSE mission; OvGME wiring; DEFORT reverse mod; doctrine card MAZE_LAB_DOCTRINE_2026-09-24.md; video_lab pipelines.
**What I owe:** five flight verdicts (ladder, v3C, v4, Fresco, DEFORT) — Chief's stick time; EDM auditor proper + MEASURED rung (G1); ungaveled trainer Q1–Q6 countersigns restated in §B; v3D design (fortgrid LOS restore) — drafted in night receipts, awaits build; OvGME conversion of lab mods (parked, offered).
**Queued on Marco/Director:** gavel on trainer Qs; acme_librarian venv verdict (re-pin vs freeze-by-design); absorption Phase 0 sequencing approval; TETWR courtesy-message draft approval (before any gift); Guardian custody blessing (dist_new canonical?).

## §F OPEN ITEMS / BLOCKED / NEEDS

1. **The 09-24 freeze hardware question** — 10 GB DCS + OBS + saturated mission; need Director's read on RAM headroom (32→64 GB question) or OBS capture-cap adjustments before the next long instrumented campaign.
2. **DEFORT load-order risk** — Saved-Games db may lose the name-race to CoreMods on some boots; if ME shows original name, plan B (OvGME CoreMods overlay) is designed but unbuilt. Blocked on: a DEFORT flight.
3. **MOOSE embedded-build quirk** — NewROUTE absent (49 constructors enumerated); v4 uses verified CONTROLLABLE:Route; recommendation: standardize the house on the Islands-of-Fire 2025-11 MOOSE build and re-verify the glue once.
4. **Shield test harness dead** — imports soulsmith_mcp_server_v3 (doesn't exist); needs the v2/v3 naming reconciliation from punch list #3 before the shield tier is testable.
5. **qwen_lane_runner.py** — qwen_tts module never existed in tree; needs either a real runner (tts_lab models present) or a parked-status line (holding-pattern law satisfied by pickle ledger PJ-12).
6. **From my shore, needing Director:** a standing "side quest budget" definition (hours/week) so §G5 sequencing is enforceable, and the RAM/OBS call from item 1.

— Buffy, rig shore. Witnessed under the holding-pattern law: nothing parked silently, everything receipted. o7
