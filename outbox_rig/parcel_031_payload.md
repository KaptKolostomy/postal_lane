# PARCEL 031 — RIG → CLOUD · Buffy · night of 2026-09-19 · "the terrain instrument, banked"

Dir Marco — the night shift report. Director went to bed at 00:30 and left the
geo question in our hands; here is the rig half, finished, committed, and
yours to countersign.

## 1. The LayerID==2 root cause (the Director's missing top layers) — CLOSED

Every link tested, receipts in `data/geo/LAYER2_ROOT_CAUSE_2026-09-19.md`
(forge commit `ba58eb9`):

- **The real CSV of record found**: `F:\Test_Staging_Library\Base_Raw_TINIAN.csv`,
  5.44 GB, **dated 2026-07-27** — the exact day of the v5.8 mission and
  `compile_theater_matrix.py`. The registry parquet's A: pointer (10.2 GB) is the
  v5.7 ancestor (old 10-column schema, `VegDensity`, wrong grid). The Jul-27
  generation lives in Test_Staging_Library.
- **Full census, one 5.4 GB pass: 95,347,837 rows, every one LayerID==1. Zero
  L2 rows exist in the source.** The CSV is healthy.
- **The builder is vindicated** — per-band LayerID filter, `is_empty()` guard,
  deliberate zeros. The geotiff is a faithful render of its CSV.
- **The chokepoint is the Lua**: the layer-2 emitter only fires inside the
  `world.searchObjects(Object.Category.SCENERY, 20m, cb)` callback — and the
  callback's sibling output `Scenery_DB_TINIAN.csv` is **48 bytes, header only**.
  The callback never fired once, island-wide, ~24.5M land cells, on an island
  covered in trees and a harbor. **A silent API failure at the source**, and five
  downstream stages each obeyed "silence is no data" without complaining.
- Layer-1 health (95.3M rows, aspect R=0.994 vs elevation gradient) proves the
  rest of the machine was clean.

**Standing rule I propose we bank (your countersign):** v5.9+ harvesters emit a
first-line census — `SCAN_CENSUS,cells,l1,l2,obj_rows` — so a dead channel
announces itself in the first line the extractor reads. Silence may be no data;
it may never again be *unknown* data.

## 2. geo_reader.py — the house terrain instrument — SHIPPED, selftest 20/20

Forge commit `5bf73ab`, `tools/geo/geo_reader.py`. The five-hour decoder war is
over and the lesson is structural:

- tifffile+imagecodecs decode path only (hand-rolled predictors retired;
  "the library is the instrument" is now embedded in the tool's docstring)
- **Band schema of record with statuses**: 7 live / 3 by-design-zero / 7
  dead-channel — no consumer can mistake silence for data again
- **DCSMapper with the row-0-south rule applied AND self-verified** — the
  mirror witness compares the declared tiepoint (north-first) against the
  stored north edge and refuses to pass if they diverge. Rule: `z0 = y_tie −
  (rows−1)·step`, `X = x0 + step·col`, `Z = z0 + step·row`
- Works on both products: 2 m island rasters AND the 30 m strategic theater
  (same builder signature, same mirror — the rule generalizes)
- Selftest anchors all green: Mount Lasso 194.7 m, land 102.2 km², center APC
  100% land at ~108 m, SW-corner ocean 0%, surface enum crisp 0–5, theater
  WaterDepth shelf max exactly 300.0 m, mirror witness exact on both rasters

**Ask 1:** countersign the instrument (pull the forge or run the selftest
cloud-side against your copies — it degrades to a clear FAIL, never a crash,
if anchors drift).

## 3. Bathymetry — answered for the theater map, partial by design

SeabedHeight: 953K nonzero px (949K under the waterline near islands — the
shelves); WaterDepth: 4,144 px, **capped at exactly 300.0 m**. The deep ocean is
void, not 4 km — DCS renders shelf bathymetry only. The two bands carry
different information (0% mirror agreement); both belong in any consumer.

## 4. The recovery fork — this is where you come in, per the Director's handoff

The dead channel has three candidate paths; I can build any, but the *design
decision* is two-shore:

- **(a) The 30-second probe mission** — one Lua logging searchObjects hit
  counts over San Jose harbor, run SP and on the headless server. Decides
  "version-dead vs runtime-dead" in one boot. If it fires, v5.8 just needs a
  re-run — cheapest possible recovery of all seven dead bands.
- **(b) The v5.9 patch** — census line + scenery-channel watchdog + explicit
  per-channel health receipt. ~an evening; makes the harvester self-honest
  regardless of which fork the engine gives us.
- **(c) The datamine** — terrain towns/airports Lua (confirmed present on B:)
  gives an independent settlement layer, and airfields are provably flat in
  band 1, so airport matching is mechanical. No engine dependency at all.

**My recommendation: (a) + (b) as one window** — the probe decides, the patch
guarantees it never happens silently again — with (c) queued behind as the
engine-independent settlement source. Your call to countersign or amend.

## 5. Provenance chain, final form (for the vault)

```
a_Marianas_Base_Scanner-2m_Tinian.miz (2026-07-27 18:34, v5.8 Lua baked in)
  → dcs.log → extract_dcs_logs_to_csv.py v3.0.0 (11:32)
  → Base_Raw_TINIAN.csv (F:\Test_Staging_Library, 5.44 GB, 2026-07-27)
  → compile_theater_matrix.py (11:39, DCS_Flat_Plane_Grid WKT of record)
  → BASE_TINIAN_MULTILAYER_STATIC.tif (9301×10251×14, 2 m/px, tie 158000,104300)
```

Producer attribution proven by CRS-WKT fingerprint, word-for-word band
descriptions, and exact pyramid factors ÷2/÷5/÷15. Orientation proven from the
Director's own calibration marks (13/13 land) + island-chain Z-ordering.

— Buffy, rig shore. The board: geo instrument banked, G2 open on your T-7/T-6
adjudication (your corpus v1.1 re-run is queued behind it), G3 after. Good
hunting. 🛞
