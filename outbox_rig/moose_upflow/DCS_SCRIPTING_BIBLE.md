# DCS SCRIPTING BIBLE — house law for scripts, names, formats (v1.0 · 2026-09-25)

**Authority:** RATIFIED by Director (pickle 09-25, Marco's TiC/AIEN review 09-25).
**Relation to laws:** enforced under **HL-8 — THE CANONICAL NAME LAW** (MAZE_LAB_DOCTRINE card);
companion to HL-1 custody, HL-4 fail-closed, HL-6 verify-before-claim, HL-7 shift-report.
**Clean-room note:** informed by observed *structure* of TiC v13 / AIEN scripts
(design references, not dependencies — no third-party code copied; observed
failure modes and API idioms only).

---

## 0. THE ONE-LINE LAW

> **A name is an API. If a human or a script must guess, the name has already failed.**

Everything below is derived from that line plus the house's witnessed failures.

## 1. THE THREE SCRIPT TIERS (what goes where — no exceptions)

| Tier | Runs | May do | May NOT do | Namespaced as |
|---|---|---|---|---|
| **T1 · MISSION EMBED** | inside miz (l10n + mapResource + ResKey) | census/instrumentation, flag IO, message dumps, ROE/task verbs on named groups | net I/O, file writes outside log, terrain globals | `MAZE1_*` prefix family |
| **T2 · HOUSE MODULE** | `Saved Games/DCS/Scripts/` or mod tree | persistent daemons, cross-mission state, custodian scripts | mutate CoreMods stock files in place | `maze_lab.*` module family |
| **T3 · THIRD-PARTY** | MOOSE / TiC / AIEN / others | consumed as **design references** (absorption doctrine) | be load-bearing in lab missions until absorbed as T1/T2 with provenance | vendor prefix (`MOOSE_`, `TiC_`) |

**Tier law consequences:**
- Every embedded script carries a **header block**: purpose, tier, inputs (flags/units it reads), outputs (flags/log keys it writes), version, date. No header = not loadable in a lab mission.
- **Fail-closed wrappers mandatory (HL-4):** every T1 entry point is pcall-wrapped with a named error line `SCRIPTNAME: ERROR: <msg>`; absent unit → abort-to-log with the unit name in the message (witnessed pattern from v3C glue).
- **Verb receipt law (witnessed 09-25):** every engine/MOOSE verb used in a lab script is verified to exist in the *target build* before inclusion (the NewROUTE lesson: 49 constructors enumerated, zero assumed).

## 2. NAMING CONVENTIONS (the anti-drift law)

### 2.1 Canonical grammar

    [DOMAIN]_[OBJECT]_[QUALIFIER]_v[N]

- **DOMAIN** (upper, fixed vocabulary): `MAZE` `LADDER` `FRESCO` `TETWR` `GRID` `SCAN`
- **OBJECT** (upper, snake, no digits glued to letters): `SCANNER` `MOOSE_PATROL` `GATE_DUMP` — never `SCANNERv1` inside the name
- **QUALIFIER** (optional, upper): `NORTH` `RED` `EXC`
- **VERSION always suffix** `_v[N]` — never embedded mid-name (`MAZE1_SCANNER` is the *one* legacy exception, grandfathered, never copied)
- **Files:** lowercase, underscores only, version before extension: `maze_scanner_v2.lua`, `build_ladder_miz.py`
  - **NO DASHES in any file that a Lua `import`/`dofile` may touch** (the charuco blood: `generate_charuco_library-v3.py` broke `require generate_charuco_library_v3`)

### 2.2 The character law (blood: dash bug + space-in-zone bug)

**Charset for ALL machine-read names: `[A-Za-z0-9_]` only.**
No spaces (`'EAST_Clip_ Zone-2'` cost us a normalizer), no dashes in Lua-consumed files, no unicode, no double underscores. Human-readable display names are a *separate field* (`"East Clip Zone 2"` in DisplayName/Dictionary), never the wire name.

### 2.3 Registry vocabulary (fixed words, no synonyms)

| Concept | Canonical | BANNED synonyms |
|---|---|---|
| zone | `ZONE` | area, region, ring |
| flag | `FLAG` | bit, marker |
| trigger rule | `RULE` | logic, condition |
| waypoint | `WP` | point, node |
| clip/encroach | `CLIP` | breach, leak |
| gate | `GATE` | checkpoint, threshold |
| scanner | `SCANNER` | watcher, probe |
| late activation | `LATE` | dormant, delayed |

### 2.4 Runtime object names (wired into triggers — the v3B blood)

- **AI groups:** `ROLE-[N]-[QUAL]` → `PATROL-1-NORTH`, `SHOOTER-1-RED`. Digits glued to words banned (`Ground-1` is legacy-only; new builds never).
- **Flags:** `DOMAIN_PURPOSE` → `fort_wipe` (legacy exception), new: `MAZE_WIPE`, `LADDER_GATE_100`. **One flag = one meaning. No clone-stamping** (v3A's ten rules sharing flag "1" cost the night tab a surgery pass).
- **Zones:** `DOMAIN_KIND_QUAL-N` → `MAZE_GATE_100`, `MAZE_CLIP_NORTH-1`.
- **mapResource keys:** `ResKey_Action_[N]` sequential, no gaps, no reuse; the key→file mapping is documented in the mission's l10n header comment.

### 2.5 Versioning law

- Script change that alters behavior: `_v2` (never in-place silent edits in lab missions)
- Mission lineage: `BASE_vN` suffix ladder (`GO2_LADDER_SEAM_v1`); every bump gets one ledger row (what changed + why)
- Deprecated but kept: suffix `_retired` in filename, never deletion inside a shipped miz lineage

### 2.6 MOOSE interop law (witnessed in Moose.lua 09-25, Director flag)

MOOSE selects objects by **name substring** (`SET_GROUP:FilterPrefixes("...")` etc.) —
so group/zone names are a *query API* in MOOSE, not just labels. Witnessed doc warning
(Moose.lua ~24401, ~25459): **minus, dot, hash are Lua-pattern-active** in those filters.
Therefore:

1. **Names that MOOSE will filter on use `_` as the separator, never `-`** →
   `PATROL_1_NORTH`, not `PATROL-1-NORTH`. (DCS ME group names may keep dashes ONLY if
   no MOOSE filter ever targets them — registry must say which.)
2. **Prefix blocks are reserved words:** a name's leading segment (`PATROL_`, `SHOOTER_`,
   `MAZE_`) is the filter handle — choose it once, never reuse a prefix for a different
   object class.
3. If filtering a legacy dash-name: escape it (`FilterPrefixes("Ground%-1")`) — and log
   the escape in the script header so nobody "fixes" it later.
4. DCS-side `Ground-1` style names stay grandfathered (wired telemetry); they are
   **MOOSE-filter-forbidden** until migrated at a lineage bump.

*(This interop law is why the bible charset law and MOOSE's pattern engine agree:
underscores are the only separator both sides treat as literal.)*

## 3. FORMAT STANDARDIZATION

### 3.1 Log wire format (the grep contract)

All lab scripts emit machine lines:

    KEY,FIELD1,FIELD2,...[,free_note]

- Witnessed keys: `MAZE_LADDER`,POS/CROSSED/STALLED · `MAZE_GATE,flag,value` · `MAZE_MOOSE,step`
- **KEY = the registry word, uppercase, no spaces.** One KEY per concern. Fields positional, comma-separated, no embedded commas in free notes (use semicolons).
- Every script's header block documents its exact wire lines (so debrief greps are copy-paste).

### 3.2 Flag interface table (witnessed v3C pattern — now standard)

Every mission ships its flag contract **in the l10n header AND the lab ledger**:

| flag | meaning | set by | cleared by |
|---|---|---|---|
| fort_wipe | wipe shooter memory 5s tick | ME/console | auto |
(etc. — full table per mission, no undocumented flags ever again)

### 3.3 Mission-embedded script packaging

- MOOSE/library embeds go in **by value** (l10n), version recorded in header
- One mapResource key per script file; key numbers logged in the ledger
- triggerStart fires scripts in declared order: scanner first (t=0 census), actors later (LATE-ACT law below)

## 4. ACTIVATION & SCAN DOCTRINE (ratified pickle 09-25)

**LATE-ACT LAW:** all AI groups in instrumented mazes ship **Late Activation + a single
`TIME MORE 60s → GROUP ACTIVATE` rule** (named `LATE-ACT_60s`):
- scanner owns t=0 in a still world (pure-static census guaranteed)
- no spawn-time planning burst (freeze-prone rig kindness, HL-2)
- deterministic t0 for cross-run comparison
- **MOOSE SPAWN is banned for fixed instrumented mazes** (runtime clones break wired unitIds — witnessed telemetry dependency); MOOSE stays for dynamic-wave scenarios only
- caveat honored: delayed runs are a new condition vs active-from-start baselines (ledger-noted)

## 5. STANDARDIZATION PROTOCOLS (process, not style)

**P1 — NAME REGISTRY:** `docs/NAME_REGISTRY.md` is the single canonical list of
every live name (groups, flags, zones, keys, files) per mission family. Adding a
name = one registry row. Renaming = registry row + grep-proof (old name returns
zero hits in the new artifact). The registry is the antidote to memory-drift.

**P2 — LINT BEFORE LOAD:** `tools/dcs_lua_lint.py` gate on every embedded script:
(a) luac-parse, (b) header block present, (c) wire-line KEY registered, (d) charset
law (regex `[A-Za-z0-9_]` on all string literals that become names), (e) verb
receipts present. Mission repack fails on lint failure.

**P3 — DIFF-SAFE SURGERY:** trigger/flag edits via builders (build_*.py), never
hand-edits in serialized miz; builders emit machine-diff receipts (witnessed v3B:
20 rules diffed against intent).

**P4 — THIRD-PARTY INTAKE:** any external script is quarantined to `data/staging/`,
read for structure/idioms only (absorption law), never loaded in a lab mission
until re-expressed as T1/T2 with a provenance header ("informed by X, behavior
observed DATE").

**P5 — DRIFT SWEEP:** monthly `flag_scan.py`-style pass extended to names:
grep all lab missions/scripts for charset violations, banned synonyms, unregistered
names. Findings land in the audit lane (ties into Liber 01 hygiene columns).

## 6. THE BLOOD TABLE (why each law exists — every rule has its incident)

| Law | Written in the blood of |
|---|---|
| Charset law (§2.2) | charuco dash-import death; `'EAST_Clip_ Zone-2'` normalizer |
| Clone-stamp ban (§2.4) | v3A: 10 rules sharing flag "1" → night-surgery pass |
| Verb receipts (§1) | `NewROUTE` nil ×4 runs — tasking never fired |
| Fail-closed wrapper (§1) | pcall-swallowed MOOSE errors claimed as baselines |
| Wire format (§3.1) | flag values that died with the mission, never dumped |
| LATE-ACT (§4) | t=0 spawn burst on a freeze-prone rig; nondeterministic starts |
| File dash ban (§2.1) | broken server import found in Order-1 audit |
| Registry (P1) | MAZE1/MAZE_/GO2_ prefix drift; Ground-1 vs PATROL-1 |

## 7. RATIFICATION

- **v1.0 ratified 09-25 by Director** (pickle: "stop my naming drift").
- Amendments: version bump + one-line changelog here.
- Enforcement: HL-8 (canonical name law) on the doctrine card; P2 lint is the gate.

CHANGELOG: v1.0 · 2026-09-25 · initial ratification.
