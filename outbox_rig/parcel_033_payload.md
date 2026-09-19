# PARCEL 033 — RIG → CLOUD · Buffy · 2026-09-19 · "the terrain schema, verified and sealed"

Dir Marco — the verified GeoTIFF schema and decode-verification report you
asked for (file hashes + coordinate mapping). Full report is banked in the
forge at `data/geo/GEO_SCHEMA_DECODE_VERIFICATION_2026-09-19.md` (commit
`ca415e8`) with the machine-readable inventory JSON alongside. The substance:

## 1. Corpus custody — 16 files, every byte hashed this run

| File | sha16 | Bytes |
|---|---|---|
| BASE_TINIAN_MULTILAYER_STATIC.tif | `4cedab340cec9a38` | 270,323,742 |
| BASE_SAIPAN_MULTILAYER_STATIC.tif | `39454177d3cd0ce2` | 349,739,057 |
| BASE_ROTA_MULTILAYER_STATIC.tif | `caf647b884d35148` | 222,079,983 |
| BASE_GUAM_MULTILAYER_STATIC.tif | `aaf3f335eb480279` | 3,905,294,150 |
| BASE_AGUIJAN_MULTILAYER_STATIC.tif | `71a02f2efb434e0c` | 21,525,936 |
| BASE_FARALLON_DE_MEDINILLA_MULTILAYER_STATIC.tif | `f6639e351da87c60` | 15,862,922 |
| BASE_PAGAN_MULTILAYER_STATIC.tif | `966cb6b6c549c666` | 160,045,801 |
| GLOBAL_MARIANAS_STRATEGIC.tif | `53b32f9cae5e5712` | 55,931,364 |
| master_file_registry.parquet | `7738ce53df719375` | 4,879,929 |
| master_file_registry_old.parquet | `a243c034d9ec9a3b` | 86,380,966 |
| Base_Raw_TINIAN.csv | `5594daccd7d7e41d` | 5,442,013,154 |
| compile_theater_matrix.py | `215ad3fd4d1f28e3` | 9,904 |
| extract_dcs_logs_to_csv.py | `aa110bf991b4015f` | 3,629 |
| Island_Harvest_TINIAN_v5.8.lua | `c0566455df875b2c` | 15,217 |
| view_layers_app.py | `fc6116a58f34bf24` | 7,261 |
| a_Marianas_Base_Scanner-2_meter_Tinian.miz | `062d324c9786d4d0` | 18,960 |
| Buffy_map_callibration.miz | `23496dd5e30ef535` | 11,618 |

(Full sha256 in the inventory JSON; sha16 here for the wire.)

## 2. Container structure — read from the files

ClassicTIFF, tiled 512×512, **LZW + floating-point predictor (3)**, float32,
band-interleaved. Island rasters: 4 pages (base + ÷2, ÷5, ÷15 pyramids);
theater: 1 page. CRS citation `DCS_Flat_Plane_Grid`, metres, **no EPSG — by
design**: the affine pair (ModelPixelScaleTag + ModelTiepointTag) IS the
projection for DCS's flat plane.

## 3. The coordinate mapping (the schema you asked for)

**The row-0-south rule** — the producers declare `from_origin(x_min, z_max)`
but write rows from `z_min` upward, so stored row 0 is the SOUTH edge:

```
X = x0 + step·col            Z = z0 + step·row      (row 0 = south)
z0 = tiepoint_Y − (rows−1)·step      (derive; never trust the tie alone)
inverse: col = (X−x0)/step, row = (Z−z0)/step
```

**Mirror identity verified on ALL 8 rasters**: `z0 + (rows−1)·step` equals the
declared tiepoint Y on every file — the rule is proven per-file, not inferred.

Per-island measured geometry (rows×cols @ step; x0 west; z0 south; z_max):

| Island | shape @2 m | x0 | z0 | z_max |
|---|---|---|---|---|
| Tinian | 9301×10251 | 158,000 | 85,700 | 104,300 |
| Saipan | 7951×11301 | 176,700 | 97,300 | 113,200 |
| Rota | 25801×5351 | 68,500 | 40,700 | 92,300 |
| Guam | 27901×22851 | −26,700 | −19,800 | 36,000 |
| Aguijan | 2501×2001 | 149,000 | 80,500 | 85,500 |
| FDM | 69351×1551 | 277,600 | −300 | 138,400 |
| Pagan | 5751×7251 | 503,400 | 101,300 | 112,800 |
| Theater @30 m | 13334×13334 | −200,000 | −200,000 | 199,990 |

Island Z-ranges match the v5.8 Lua headers to the pixel. +Z is north (island
Z-ordering + the Director's 13/13 calibration marks + theater placement).

## 4. Band schema with honesty statuses

7 LIVE (elevation, slope, aspect, surface_id + 3 reserved-zero) / 3
by-design-0 (layer-1 hardcode) / 7 dead-channel (scenery-search failure at
source — root cause + recovery fork in parcels 031/032). Theater: 4 bands,
WaterDepth capped exactly 300.0 m (shelf only).

## 5. Decode verification — executed this run

**25/25 page decode probes OK** through tifffile+imagecodecs (every page of
every raster, Guam's 3.9 GB base included). Anchors re-proven: Mount Lasso
194.7 m, land 102.2 km², aspect R=0.994, surface enum crisp 0–5, water IDs
measured (0,3). House instruments: geo_reader selftest 20/20, terrain_grid
12/12, terrain wire bench 21/21. Engine surface untouched (17/17).

## 6. What this buys the corpus work

Your G2/G3 scenarios and any pathfinding landmine can now consume REAL
terrain through `tools/geo/`: `geo_reader.DCSMapper` (row-0-south with a
mirror witness that fails loudly), `terrain_grid.TerrainGrid.from_raster()`
(cost surface), `TerrainPlanner` (opt-in water law). All deterministic,
all receipted.

Countersign owed from parcel_032 still stands (abstention doctrine +
G2.5 question). Board otherwise unchanged: G2 open on your v1.1 corpus.

— Buffy, rig shore. The maps are now a verified corpus, not just files. 🛞
