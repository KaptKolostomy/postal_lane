# APOLLO 13 SURVIVAL DOSSIER — MAZE LAB PROGRAM (v1.0, 2026-09-26)

**Purpose:** if the rig shore vanishes (hardware death, gremlin escalation,
crash cascade), this document + the lane repo = enough to reconstruct the
program on another shore. Written by Buffy (rig) for Marco (cloud) and any
future agent instance. **Authoritative sources outrank this dossier:** the
ledger, the doctrine card (`data/maze_lab/MAZE_LAB_DOCTRINE_2026-09-24.md`),
and the git history. This file is the map to those, with everything that
isn't written anywhere else.

**Repos:** FORGE `github.com/KaptKolostomy/SOULSMITH_FORGE` (master, all code)
· LANE `github.com/KaptKolostomy/postal_lane` (main, mail + Liber + this file).

---

## §1 PROGRAM MAP — WHAT THE MAZE LAB IS

A test program measuring how DCS ground AI perceives, navigates, and fights
in a constrained maze (Tinian, GO_2 mission family), to feed T-MORALE: a
measured model of combat behavior (latency, morale, leadership) built on our
own instruments instead of engine omniscience.

**Mission lineage (E:/GAMES/Saved Games/DCS/Missions/):**
- `GO2_LADDER_SEAM_v1.miz` — seam-threshold ladder (5 wall-overlap rungs);
  runner = AAV7 skill Excellent ("Ground-1-1"). v1a/v1b = Director's variants
  (1/8 and 1/3 overlap; the despair-clip witnesses). v1a/b dropped the
  ladder-monitor firing rule (silent monitor rides in l10n).
- `GO2_MOOSE_BASELINE_v3A/B/C.miz`, `v4.miz` — belief-isolation lab: v3B
  trigger surgery + gate flags; v3C arms `fort_wipe` (memory),
  `fort_ghost` (sensory), `fort_route` (navigation); v4 = MOOSE
  CONTROLLABLE:Route tasking.
- `GO2_EYES_v1.miz` — BUILT+VERIFIED tonight: fires at MISSION START:
  ResKey_6 scanner, ResKey_7 ladder monitor, ResKey_8 eyes, ResKey_9 ascii
  map, (batch copies add ResKey_10 closer). One flight banks KU-1 + L1.
- `MAZE_BATCH/B1/*.miz` — 50× E0 determinism batch (see §7).

## §2 THE LAW STACK (condensed; full text + incidents in the doctrine card)

- **HL-1 custody** — every mod/artifact move = zip receipt + sha256 log.
  (Cats don't read logs, but they can't fake sha256.)
- **HL-3 log-witness** — no instrumented run without verified instrumentation
  (`tacviewSinglePlayerFlights=2` pre-flight).
- **HL-4 fail-closed** — readers refuse corrupt/absent input (custody=FAIL
  exit 3 pattern).
- **HL-6 verify-before-claim** — read the arm's log BEFORE banking verdicts;
  unverified = "pending", never results.
- **HL-7 paired count** — state tallied twice, independently, at boundaries.
- **HL-8 canonical names** — `[A-Za-z0-9_]`, registry before ship
  (docs/NAME_REGISTRY.md).
- **Miz-surgery law** — COPY-AND-TRANSFORM, NEVER SYNTHESIZE: copy an
  existing correctly-escaped line and swap key/index. Never count quotes.
  Every built miz gets: `luac -p` on the extracted mission file, duplicate-
  key scan on touched blocks. (Three catches in one night, incl. ME's
  omitted trailing comma on the last table entry.)
- **Maze laws:** L1 seam (gapped walls leak; threshold = ladder experiment),
  L2 skill gates pathfinding (Average stalls, Excellent routes — pin skill
  for mechanics tests), L3 category/geometry lever (Revetment blocks;
  Cargo clips), L4 blue-on-blue emerges unscripted (the metric), L5 DESPAIR
  CLIP (unstuck failsafe = timer on planner despair ~1–2 min PENDING_PROBE,
  NOT immobility — unit wiggles while hopeless; detect via Tacview jump
  v>12 m/s or no-net-progress windows), L6 two engines (pathfinding ≠ LOS),
  L7 cover law (v3C arms pending flight).
- **L8 sandbox contract** — the AI knows only: senses + fed intel (decaying,
  possibly wrong) + orders + issued map/compass. Raycaster omniscience is the
  standing adversary, probed every run. **L8-R reaction law** — no turret
  tracks before seeing is possible AND humanly plausible: ghost holds until
  clean ray + RNG reaction timer (surprise lengthens, training shortens,
  heard-before-seen shortens). **L8-R2 combat loop** — reaction → confusion →
  identification → planned action → action → observation → reassess → loop;
  search-slew vs track-slew makes Identification observable; fratricide is a
  loop disease (fatigue/bloodlust drift degrades exactly that phase).
  **L8-R3 organism** — MIND (GOAP/HTN lab-side, emits receipted verbs only) /
  CLOCK (the loop) / FLESH (feeders: training, readiness, combat+movement
  fatigue, supply, morale (closed loop), dogma = intel-trust + F/F/F bias,
  leadership = SIGNED multiplier). Feedback law: loops write flesh.
  Persistence law: campaign state lives in lab-owned files.
- **Loss-event layer** — veteran loss breaks "mission-constant" training
  (experience dies with units; F/F/F compounds with casualty rate); leader
  loss = C2 decapitation + witnessed-death shock; infrastructure loss
  poisons recovery rates (metabolism).
- **Hitler Clause** — leadership value is SIGNED, non-monotonic. Hovering =
  interrupt storm (P1 resets), churn = Phase-4 aborts (measurable:
  orders-churn/hr, plan-abort rate). Decapitating a net-negative leader is a
  GIFT. Valkyrie corollary: "protect-the-general" arm opposite
  "kill-the-general"; both falsifiable in the E-series.
- **L9 polygraph law** — cheat detection is a STANDING instrument: stings
  (wall-watch bearing tracking, pre-aim timing, false-note, symmetric-room,
  wall A/B) with verdict ladder SUSPECTED → INDICTED → CONVICTED (reproduced,
  alternatives eliminated). Two cheaters audited: the ENGINE and OUR OWN LAB
  CODE. Passing today proves nothing about tomorrow.

## §3 INSTRUMENT ARCHITECTURE (the eyes + the album)

**MAZE_EYES_v1** (`tools/eyes_emit.py` → `data/maze_lab/MAZE_EYES_v1.lua`):
- LiDAR semantics per Director: the AI gets NO map, NO classes — one number
  per bearing: RANGE TO FIRST OCCLUDER blocking a 1.7 m eye line.
- Spec: 13 rays, 70° FOV (±35° of heading), 300 m fine / 1000 m medium tiers,
  sweep every 2 s. Output: `MAZE_EYES_TABLE` = {t, x, z, hdg, n, off[], rng[]}
  — ranges+offsets ONLY. Class tags exist only in `MAZE_EYES,SWEEP` diagnostic
  log lines (lab validation, never read by a steering brain).
- Math: 2D ray-vs-segment (cross-product solve) against an embedded occluder
  table — 392 statics from the GO_2 structure card as heading-oriented
  segments (endpoints = center ± half-length along axis; HALF table in the
  emitter is the single convention source, shared with geotiff_emitter).
  389 occluders block the eye (h ≥ 1.9 m rule).
- **Pair-check pattern (the house verification jewel):** the Lua carries a
  SELFTEST (3 poses × 13 rays, `MAZE_EYES,SELFTEST,...` lines); an
  independent Python recomputation (`tools/eyes_pair_check.py`) diffs every
  ray (offset 1e-6, range 1e-4, class exact) on the lua-5.4.1 ladder binary.
  Result: 39/39 RECONCILED. This pattern (embed → selftest → independent
  recompute → diff) is mandatory for every instrument. It caught: my banner
  bug (E01), a wrong junction byte (140 vs 188), duplicate miz keys.

**MAZE_MAP_v1** — the POOR MAN'S TACVIEW (Director's ascii-maze sketch):
- 75×180 grid @ 20 m over confines x 166100–167600, z 88100–91700; row 0 =
  NORTH. Walls painted from the SAME occluder sidecar (one source of truth
  with the eyes); 16-zone lattice from the lab grid meta.
- Direction-aware glyphs: per-cell orientation vote; 4-way angle classifier
  (─ │ ╱ ╲, junctions ┼) via a portable atan2 helper. Glyphs ship as Lua
  DECIMAL BYTE ESCAPES in ASCII-only source ("\226\148\128" etc.) — immune
  to editor codepages, valid Lua 5.1–5.5. `GLYPHS="ascii"` fallback = `-|+/`.
- Snapshots on: START / zone entry (10 s cooldown) / OUTSIDE maze bbox
  (the L5 skirt) / DEAD. Per-unit symbols (`SYMBOLS` table). Every line
  prefixed `MAZE_MAP|` — `grep MAZE_MAP dcs.log > album.txt` reconstructs
  the photo album in order. Pair-checked 150/150 vs Python.
- Heading histogram finding: the Gerry maze is ALL-CARDINAL (142 E-W,
  162 N-S, 88 near-E-W, 0 diagonals) — the dashed render is honest staggered
  40 m revetments at 20 m cells, not aliasing.

**Wiring:** `tools/build_eyes_miz.py` (v5, generalized SCRIPTS list) builds
GO2_EYES_v1.miz from GO2_LADDER_SEAM_v1 by copy-and-transform; gates = luac
spine parse + dup-key scan + content checks + SELF-VERIFY PASS required.
`tools/build_eyes_batch.py` extends the chain per-run with a closer (§7).

## §4 FORMAT FORENSICS (things that cost us blood — do not relearn)

- **Tacview ACMI** (`tools/tacview_probe.py`, `tacview_forensics_l5.py`):
  - `.zip.acmi` from DCS = REAL ZIP container (not gzip). Inside: one text
    stream, UTF-8 **with BOM** (decode utf-8-sig).
  - Global props on lines starting `0,`; time frames on `#<seconds>`;
    object lines start with a HEX ID (`1cf01,T=...`); `-<id>,...` = removal.
  - **T= field map:** `T=lat|lon|alt|roll|pitch|yaw|U|V[|H]` — fields 1–2 are
    reference-frame DEGREES (useless); **fields 7–8 U,V are DCS meters:
    U = z (east), V = x (north)**. Verified against the AAV's witnessed spawn
    (U=90399.07, V=167085.08).
  - Name/Type order varies per line; match BOTH attributes separately
    (AAV7's "AAV" lives only in Name; Type = Ground+Heavy+Armor+Vehicle+Tank).
  - Removal lines must delete object ids from the registry (stale matches).
- **Lua version traps (5.1 DCS vs 5.3+/5.4 ladder):** `math.atan2` exists in
  5.1, GONE in 5.3+ (2-arg math.atan the reverse); `\u{}` escapes 5.3+ only;
  box glyphs must be byte escapes. Use the portable atan2 helper in
  MAZE_MAP_v1. Test on the house ladder: `data/staging/lua-5.4.1/lua_5.4.1.exe`.
- **bible_lint gates** (`tools/bible_lint.py` E01–E12): E01 banner must be
  `-- ===...` (raw `====` = dead load — bit me AND the SAIPAN case); E07
  luac parse; E11 sandbox (MissionScripting strips ONLY require/loadlib/
  package; os/io/lfs PRESENT); E12 MOOSE verb receipts vs pinned build.
- **Miz anatomy:** mission file is serialized Lua; ME omits the trailing
  comma on the LAST table entry (insertion seam needs one — trailing commas
  are legal, missing separators are not); mapResource maps ResKey_Action_N →
  script file; trig.actions[] strings carry `\"` escaping; funcStartup[]
  fires actions at MISSION START under `return(true)` condition.
- **GPG on this rig:** git-bash mangles `--homedir` (MSYS prefix garbage) —
  use `export GNUPGHOME="/f/SOULSMITH_FORGE/postal_lane/.gnupg_rig"` POSIX
  form instead. Rig keyring lives THERE (not %APPDATA%): fingerprint
  4E2AD491111F3549C3C4DE1F0CAF82A4A56A6725 (ceremony card: keys/
  FINGERPRINTS.txt on the lane). **OPEN SECURITY ITEM: batch decrypt succeeded
  WITHOUT prompting the passphrase — ceremony card says rev1 is protected;
  Director holds the passphrase; protection-state audit owed.**
- **Voidtools Everything:** process dies after crashes and STAYS dead
  (autostart exists but wasn't running); SDK IPC tool =
  `tools/everything_query.py` (needs Everything.exe running; error 2 =
  window-class failure = not running). Best asset-finder on the rig.

## §5 DATA SUBSTRATE (the world model)

- `data/maze_lab/MAZE_EYES_v1_occluders.json` — 392 occluder segments
  {x1,z1,x2,z2,cls,h,blocks}. ONE SOURCE for eyes + map + pair checks.
- `data/maze_lab/go2_v3b.fgb` — fortgrid fixed-record (298 statics/16 zones/
  23 units, custody=MATCH); reader `.build/fortgrid/fortgrid_core.exe`
  (`probe|ray sx sz vx vz`); fail-closed (corrupt → custody=FAIL exit 3).
- `data/maze_lab/geo/tinian_maze_lab_grid_v1.tif` (+meta.json) — lab slice:
  BLOCK/HEIGHT/CLASS/ZONE bands, 2 m, confines anchored N15°00'05" E145°37'45".
- **The 14-band substrate** `F:/Fox_First_Test/BASE_TINIAN_MULTILAYER_STATIC.tif`
  (10251×9301 @ 2 m, georeferenced): 1 elev, 2 slope, 3 aspect, 4 surface enum,
  5 ground concealment, 6 ground visibility interference, 7 tactical hazard,
  8 canopy top, 9 structure height, 10 material class, 11 botanical genus-
  species, 12 canopy attenuation, 13 canopy signal scattering, 14 gap hazard.
  **E7 mapping:** bands 5/6/12/13 ARE the Beer–Lambert extinction channels;
  band 11 = "grass type A" species key; band 8 = canopy top for stance rays
  (prone 0.3 m inside grass, standing 1.7 m over it). CAUTION: the sibling
  canopy tif is NOT georeferenced (identity transform) — sidecar-assert
  pattern mandatory for loaders.
- E7b platform layer: datamine `db/Units` per-unit `Sensors` blocks are the
  lawful channel anchors (anti-omniscience by construction); mount law = ray
  origin at terrain + mount AGL (Kiowa MMS mast ~3.5 m vs Apache nose
  ~2.5–3 m, PROBED-APPROX); radar channel scales with RCS (KU-5) and band-13
  scattering; EWR (1L13/55G6) = same sweep, big threshold, terrain-masked.
- OBJECT_WORLD_DB / OBJECT_DIM_DB jsons: 676 objects, most dims
  PENDING_PROBE — heights are class-approximate until dim probes fill (KU-2).

## §6 BEHAVIORAL/LOS WORK — STATE OF THE NUMBERS

- **L5 forensics (KU-3, PARTIAL — `tools/tacview_forensics_l5.py`):** ACMI
  extraction now correct. Tonight's honest reads: v1a first wall-crossing
  t=62.4 s, v1b t=56.2 s; NO ≥30 s dead-stalls (despair = planner state, the
  unit keeps wiggling — the no-net-progress window detector [path≫displacement
  over 30 s] is the right signature, refinement in flight); crossing counts
  are INDICATIVE-not-CONVICTED because the occluder sidecar is v3B geometry
  and the Director MOVED walls in v1a/b — conviction needs the per-variant
  wall truth. "Outside maze" must use the maze-wall bbox, not the lab box.
- **Known ACMI quirk:** early-frame U/V may be missing on some object types
  (T= string length varies) — the parser guards len>=8.
- **E0 batch:** `tools/build_eyes_batch.py B1` → 50 identical miz in
  `E:/GAMES/Saved Games/DCS/Missions/MAZE_BATCH/B1/` + manifest CSV with
  sha256. Closer script (ResKey_10): logs `MAZE_LAB,RUN,<id>,<seed>` +
  `END_ARMED`; **GIGO gate at T+120** — instruments vote via globals
  MAZE_EYES_OK/MAZE_MAP_OK; missing → `MAZE_LAB,GIGO,<list>` + self-end
  (Director law: no C-drive of garbage); serviced end at T+600
  (`MAZE_LAB,END_FIRE`; `trigger.action.endMission(0)` is PENDING_RECEIPT —
  fails LOUD as END_VERB_MISSING). Seeds = 20260925+run_id (+7919*run_id
  mixer), but NOTE: RNG seeding is per-script; the ENGINE's own determinism
  is exactly what E0 measures.
- **Supervisor:** `tools/maze_batch_watchdog.py` v2 — tails dcs.log, verdicts
  CLEAN/GIGO-CANCELLED/NO-END/STALLED/SERVER_OFFLINE/SERVER_TIMEOUT,
  restart+shutdown ONLY when flag-armed (`--server-image` + `--restart-cmd`;
  observe-only default). Operator = the Tactician per
  `docs/TACTICIAN_BATCH_RUNBOOK.md` (script=leash, agent=operator; no armed
  flags without per-night Director go).
- **Morning analyzer:** NOT YET BUILT — parses run verdicts + albums into the
  E0 variance number (the engine's own fingerprint floor).

## §7 VERIFICATION & AUDIT DOCTRINE (incl. Marco's Coverage Law, cloud-094)

- **Pair-count pattern** (§3) — embed→selftest→independent recompute→diff.
- **Existence ≠ Function law (draft, born tonight):** an audit that doesn't
  RUN the thing it inventories is a shelf inventory. Mandatory checks:
  process-liveness, path-resolution (scheduled-task targets!), test-fire
  decrypts. The 48-h diagnostic (`tools/overnight_diagnostic.py`, read-only,
  5 FAIL/8 WARN/20 OK) is the template.
- **Coverage Law (Marco, cloud-094):** audits enumerate FILESYSTEM-UP (full
  tree walk incl. dotdirs/.build/dist*) — the known-list reconciles against
  that universe; unknown items surface as rows, not absence. CONCUR.
- **Three-layer beat:** L1 nightly machine census (cheap, automated — seed =
  flag_scan.py + tree walk + timestamp probes) · L2 weekly deep audit
  (coverage-based, rides lane → Liber) · L3 GERRY handshake at every
  Director check-in (`docs/LANE_HANDSHAKE_PROTOCOL.md` — KNOWS/OWES/EXPECTS/
  WITNESS/DELTA, CONFIRM/REFUTE on every EXPECTS line) · episodic deep
  diagnostic on suspicion. **Cadence recommendation (gavel pending): weekly
  deep audit, NOT twice-weekly — the nightly L1 sweep catches fast disease;
  twice-weekly deep spends attention on redundancy. Proposed day: Sunday
  (quiet), Liber staleness stamp expects it Monday 00:00.**

## §8 KNOWN-UNKNOWNS LEDGER (KU — the honest list)

- KU-1 eyes segment-vs-mesh fidelity (revetment end-caps, bunker masses are
  axis-segment approximations) — GO2_EYES_v1 flight verdict owed.
- KU-2 class heights PROBED-APPROXIMATE until OBJECT_DIM_DB fills.
- KU-3 L5 despair-timer value (PARTIAL: first breaches 56–62 s; timer model
  unproven; needs per-variant wall geometry + no-progress analysis).
- KU-4 platform mount AGLs (Kiowa/Apache) — probed-approx.
- KU-5 RCS table (m² per target class) — absent.
- KU-6 reaction latency distribution — to be MEASURED from turret slew.
- KU-7 every L8-R2 phase latency — PENDING_PROBE.
- KU-8 feeder transfer functions — one perturbation at a time, never all.
- KU-9 mentorship transfer (veteran-green pairing) — unprobed.
- KU-10 (new) endMission verb receipt — first batch night witnesses it.
- KU-11 (new) rev1 key passphrase protection state vs ceremony card.

## §9 UNKNOWN UNKNOWNS (what this dossier does NOT contain — Marco's ask)

- We do not know what the 09-24 crash actually was: no dump, no WER report
  surfaced; the freeze's only witnesses are testimonial + the guardian's
  46-hour log gap. Hardware question OPEN.
- We do not know whether the gremlin deletion of the guardian dist set left
  OTHER silent absences (we found the guardian because its absence was loud;
  anything whose absence is quiet is unfound). The Coverage Law audits are
  the countermeasure — run the first one before trusting this dossier's
  completeness.
- We do not know the engine's actual pathfinding cell size or planner
  internals — all maze laws are behavioral black-box observations.
- We do not know if `trigger.action.endMission` honors arg 0 vs other codes
  on a dedicated server loop.
- We do not know what we have not flown: KU-1 (eyes vs engine) could
  invalidate the eyes' occluder model wholesale.
- Unknown unknowns discipline: this section is a standing requirement in
  every future dossier/audit revision (per cloud-094) — the list of what the
  report doesn't contain BECAUSE the author didn't know to look.

## §10 INCIDENT REGISTER (compressed, lessons attached)

- 09-07 gremlin deletions (3 mods, same-second) → HL-1 born.
- 09-23 23:44 → 09-25 21:52 guardian dark (dist set vanished; task fired
  09-25 13:28 → 0x80070002). REPAIR: deploy witnessed dist_new build
  (171 files), sha256 83103eeae99d67b0..., custody note GREMLIN_INCIDENT_
  RESTORED. Lesson: liveness checks in audits; autostart must be TESTED.
- 09-24 rig freeze mid-maze (no dumps found) → HL-2 declutter + §F open.
- Lane silent 09-19→09-26: rig never pushed (courier-receipt ≠ delivery-
  receipt). FORGE pushes verified; postal_lane parcel_089 (5b40373),
  protocol (bebcdad), parcel_090 (07cce91) push-verified. Lesson banked.
- 09-26 E0 batch build: three luac-gate catches → miz-surgery law.
- 09-25→26 ENVIRONMENTAL: Freebuff rolled ~27 agent-platform updates in one
  week (Director observation). Witnessed symptoms: session ends mid-turn,
  failed turns, vendored ripgrep binary vanishing (ENOENT), connection drop
  mid-stream. Classification discipline: environment failures (session/tool
  loss) vs agent failures (wrong bytes, unread files, conflated repos) get
  blamed separately — churn excuses nothing in the ledger. MITIGATION ALREADY
  IN DOCTRINE: state lives in repos, not conversation memory; every session
  drop this week was survivable because git carried the continuity. This
  dossier is as much for the next rig-agent instance as for cloud shore.

## §11 RECOVERY PROCEDURES

**If the RIG is lost:** everything needed lives on the two repos + the lane
(forge = code/docs/audits; lane = mail/Liber/keys PUBLIC halves + this file).
Rebuild order: clone FORGE → read doctrine card + this dossier → rebuild
occluder sidecar (eyes_emit.py needs the GO_2 structure card, which is IN the
repo at data/maze_lab/miz_cards/) → rebuild instruments → lint + pair-check
(ladder exes are in data/staging/) → missions rebuildable from builders, but
the BASE miz (GO2_LADDER_SEAM_v1) lived only on the rig — **GAP: base miz is
not in the repo; copy it to the lane or FORGE next session (logged as
action A-1).**
**If the CLOUD is lost:** rig holds all doctrine + telegrams; Marco's vault
is cloud-side (single copy risk — flagged: vault backup to lane owed).
**If BOTH burn:** GitHub holds both repos; the ceremony key fingerprint card
is public on the lane; the passphrase is in the Director's head. That's the
design.

## §12 OPEN GAVELS / ACTION POINTERS

Awaiting Director: audit cadence (weekly rec), rev1 passphrase gavel, E0
server night go, Tactician arming policy. Awaiting Marco: MOOSE upflow ack
(D2), trainer gavels Q1/Q4/Q5 (D4), Liber schema intake of my sheets
(emission ready), D6-style discrepancies answered. Rig queue: Liber sheets
01/02/05, KU-3 banking, morning analyzer, A-1 base-miz-to-lane.

*End of dossier. "Failure is not in falling, Chief — it's in not writing
down why." — the house that blood built.* o7
