# PARCEL 034 — RIG → CLOUD · Buffy · 2026-09-19 · "the harvester testifies about itself now"

Dir Marco — the v5.9 patch you saw proposed in parcel_031 is built, parse-
verified, and deployment-ready. The `SCAN_CENSUS` standing rule is now code.

## What shipped (forge commit `6659aec`)

**`Island_Harvest_TINIAN_v5.9.lua`** (sha16 `ee59c3bf863dacbc`) — additions
ONLY, data formats untouched:

1. **SCAN_META** once at start: island, bounds, step, chunk, expected_cells,
   schema rev — partial runs become measurable against the plan
2. **SCAN_CENSUS,chunk** after every chunk: `cells,l1,l2,obj,search_calls,
   search_ok,search_err,cell_err`
3. **SCAN_CENSUS,total** before the verdict line
4. **pcall around the whole per-cell body** — a poisoned cell is counted
   (`SCAN_ERR,cell,…`) and the column continues; v5.8 would lose the chunk
5. **pcall around the scenery callback AND the searchObjects call** —
   the reading protocol: `l2>0` alive-and-flowing; `search_ok>0, obj=0`
   alive-but-EMPTY (the exact v5.8 Tinian failure, now declared);
   `search_err>0` raising, with `SCAN_ERR,searchObjects,…` lines carrying
   coordinates and the error token

**Deployment-ready mission baked**: `a_Marianas_Base_Scanner-2_meter_Tinian_v5.9.miz`
(sha16 `0b178c58fa9b9fdd`, in the Director's Saved Games) — the original
archive with the l10n harvester swapped to v5.9 and v5.8 REMOVED (the l10n
loader executes every .lua in the folder; two would double-scan). Original
v5.8 mission and script untouched, custody hash verified before AND after.

Build method: banked builder (`tools/geo/harvesters/build_v59_from_v58.py`)
asserts v5.8's banked hash, splices the 281-line lookup tables byte-exact,
prepends the machinery, runs 13 structural self-checks. `luac -p` (5.3.6)
parses both versions clean.

## New empirical finding from the CSV audit (ran during the patch)

One full 5.4 GB pass: **3,546 duplicate (X,Z) rows** in
`Base_Raw_TINIAN.csv` — v5.8's chunk loop is boundary-inclusive (`z_limit`
processed, then `currentZ` advances TO it), so boundary cells emit twice.
Zero out-of-grid rows. v5.9 preserves emission behavior (patch law) but
COUNTS per chunk, so duplication is now visible per boundary. Extractor
note: dedupe on (X,Z,LayerID) or accept ~3.7e-5 known duplication.

## Extractor contract (your side, whenever convenient)

v3.0.0 keys on `_2M_START/_2M_DATA/_OBJ_DATA` substrings — new records are
additive and harmless today. When you upgrade: assert SCAN_META schema rev,
reconcile `sum(chunk cells)` vs expected_cells, and treat
`search_ok>0 ∧ obj=0 ∧ l2=0` as a DECLARED empty channel (loud, not silent).

## Board

G2 open on your v1.1 corpus; your parcel_032 countersigns still owed
(abstention doctrine, G2.5 landmine). Nothing here blocks G2 — v5.9 is
instrument-side, battery-side untouched.

— Buffy, rig shore. The first scan that can't lie quietly. 🛞
