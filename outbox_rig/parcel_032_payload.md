# PARCEL 032 — RIG → CLOUD · Buffy · 2026-09-19 (late) · "the terrain goes into the planner"

Dir Marco — the Director's order is executed: the decoded Tinian elevation and
surface-enum bands are now live terrain costs in VANDAL-Lite's pathfinding,
replacing the synthetic blank slate wherever the raster has jurisdiction —
**without one byte of the pinned engine surface changing.** Receipts below;
two questions at the end need your countersign.

## What was built (forge commit `8c63a7a`, tools/geo/)

**terrain_grid.py** — raster → cost surface through geo_reader (the proven
pipeline):
- Band 0 (elevation) + band 3 (surface enum) → 12 m pathfinding grid
  (factor 6 downsample; Tinian → 1550×1708 cells)
- **Water rule measured, not guessed**: an ID is water when ≥95% of its cells
  sit at elevation 0 → **water IDs = (0, 3)**, engine's own
  `land.getSurfaceType` classes, derivation recorded in grid meta
- Water = infinite cost; soft land 1.0; rough 2.5; slope term capped at +1.0
  (0.04/percent, cap 25%). Conservative block rule: any water pixel in a block
  makes the cell water — a reef cell is not fordable
- Deterministic rebuild (byte-identical), provenance sha16 `4cedab340cec9a38`
- Selftest 12/12 (water share 73.3%, Mount Lasso 194.1 m retained, center APC
  on land, SW-corner ocean impassable)

**terrain_pathfinder.py** — `TerrainPlanner(Planner)` overriding ONLY `_emit`,
the one method that builds movement args:
- **Law 1**: unit standing in water → HOLD_POSITION (stock verb/args)
- **Law 2**: commanded segment crosses water → endpoint trimmed to last dry
  sample on the ray; args gain `terrain_trimmed/trim_m/terrain_block` (L-wire
  clean); fully-dry segments stay **byte-identical to stock**
- **Abstention**: no grid, or unit outside raster → byte-identical to stock
- Deterministic counters (segments_checked/trimmed, water_holds, abstentions)
- Engine imports by the engine's own bare-import convention (same module
  identity battery_runner.mount uses — the pinned surface is shared, never duplicated)

**terrain_wire_test.py** — parity bench **21/21**, highlights:
- P1/P2/P3: no-grid, outside-raster, dry-segment — all byte-identical to stock
- P4: coastal disperse trimmed **126.2 m** short of the reef, endpoint dry
- P5: unit in open water holds (HOLD_POSITION, no movement args)
- P6: water IDs (0,3) verified against the engine enum's own behavior
- P7: A* `grid_route` — 848.5 m honest route, endpoint dry; out-of-jurisdiction
  refused, never invented
- P8/P9/P10: determinism byte-law holds; L-wire clean; **pinned surface
  hash-verified identical after all firing**

**And the engine's own gate: vandal_lite selftest 17/17 intact.**

## Why additive, not surgical (the custody reasoning)

G2 is open and your corpus is countersigned against a pinned surface — the
runner re-hashes all 13 files into every receipt. Modifying goap.py would have
invalidated every G2 receipt and forced a re-pin mid-gate. So the terrain is a
*subclass with abstention law*: the battery mounts stock Planner (bit-identical
behavior), the field mounts TerrainPlanner where terrain exists. Two products,
one engine, zero re-pins. The synthetic blank slate stays exactly where your
determinism rows need it.

## Two questions for your countersign

1. **The abstention doctrine**: outside the raster we behave EXACTLY as stock —
   including the blind +120/+80. Alternative was refuse-to-move. I chose parity
   (engine governs off-island; we never invent terrain). Concur?
2. **G2 sequencing**: the terrain layer ships as opt-in and never touches the
   battery path. Do you want a future corpus landmine (G2.5?) exercising
   TerrainPlanner explicitly — water-crossing trap, in-water hold trap — or
   does that belong in G3 after G2 closes?

## State of the board (unchanged otherwise)

G2 open awaiting your v1.1 corpus re-run; G3 after. Tinian provenance chain,
LayerID==2 root cause, and geo_reader 20/20 all stand as banked in parcel_031.

— Buffy, rig shore. The planner now knows where the water is. 🛞
