# BUILD TOOL AUDIT — 2026-09-25 (Order 1, Marco telegram + Addendum 1)

Feeds **ABSORPTION PHASE 0**: what build/test harness exists to implement OUR
versions of AIEN/DSMC/TIC behaviors (design references, not dependencies;
clean-room law in force — no GPL/unlicensed/attribution code enters this tree).
Receipts dir: `F:\SOULSMITH_FORGE\data\audits\build_tool_audit_2026-09-25\`
(pipfreeze_forge_venv.txt, pipfreeze_tts_lab.txt, pipfreeze_acme_librarian.txt,
flag_scan.json, flag_scan.py).

## 1d. SUMMARY TABLE

| Category | Count | Notes |
|---|---|---|
| House C++ sources | 7 .cpp + 3 .h | 2,208 LOC |
| House C++ binaries | 5 | 3 current (vandal_box, pipe v3, fortgrid), 1 stale (c2_core), 1 stub-source |
| House Python files | 207 | 48,544 LOC |
| Project venvs | 3 | forge (140 pkgs), tts_lab (61), acme_librarian (33) |
| Installed packages (union) | ~200 | forge .venv is primary |
| Orphaned packages (forge) | ~142 of 140-pkg freeze | see flag 6 — bulk is transitive/latent |
| Lost modules (real) | 8 | librarian/MCP stack + qwen_tts |
| Stubs | 7 | 4 legit __init__, 1 broken, 2 placeholder |
| Name-drift families | 4 | letta_watch, miz_lint, rebuild_missions_2918, __init__ |
| Syntax-broken files | 1 → **0 (fixed today)** | kill_shot_geometry.py `}`→`)` at line 118 |

## 1a. C++ / g++ ARTIFACTS

| Artifact | Path | Purpose | Build status | LOC |
|---|---|---|---|---|
| vandal_box.cpp | tools/vandal_box/vandal_box.cpp | FSM/KB trainer box (C++ twin of vandal_lite) | **CURRENT** (exe 09-22 19:33 ≥ src 09-22 19:32) | 1,077 |
| acme_moose_cli-v3.cpp | tools/native_pipe/ | Named-pipe C2 CLI (PING/ECHO/STAT/QUIT) | **CURRENT** (exe 09-19 ≥ src 09-19); selftest PASSES exit 0 | 97 |
| acme_moose_cli-v2.cpp | tools/acme_moose_cli-v2.cpp | v2 CLI → builds acme_c2_core.exe | **STALE BUILD** (exe 09-09 < src 09-10) | 7 |
| native_shm_bridge.cpp | src/native/ | Shared-memory bridge | **CURRENT** (exe 09-14 ≥ src 09-14) | 68 |
| fortgrid_core.cpp | src/native/ | Fortification-grid fail-closed reader (.fgb) | **BUILT 09-25 00:20** → .build/fortgrid/fortgrid_core.exe (96 KB, stamp a722789e50aca086). Smoke-witnessed 09-25: probe custody=MATCH (298 statics/16 zones/23 units); ray reproduces night receipt (2 crossings, s=23.5/s=360.0). Built OUTSIDE compile bat (manual .build/ lane). | 208 |
| modulator_shim.cpp | src/native/ | Cognitive modulator shim | UNBUILT (no artifact ever) | 51 |
| native_control_injector.cpp | src/native/ | — | **STUB (6 lines), dead 09-10** | 6 |
| vandal_bayes_posterior.h | src/native/ | Bayes posterior for cognitive C++ | header-only, consumed by ? | 256 |
| vandal_circadian_lut.h | src/native/ | Circadian LUT | header-only | 88 |
| vandal_cognitive_modulators.h | src/native/ | Modulator tables | header-only | 150 |

Toolchain: **w64devkit g++ 16.2.0** at `/d/ACME_Library_Digester/tools/w64devkit/bin/g++` (not on PATH);
cmake 4.4.3 vendored in tools/. `compile_native_solvers.bat` knows ONLY the v2 CLI —
it predates the whole src/native layer.

**Absorption gap A1:** no build script covers src/native (fortgrid_core, shm_bridge,
modulator_shim, headers). Phase 0 punch list #1: extend/replace
compile_native_solvers.bat to build all five, or move to CMake.

## 1b. PYTHON TOOLS/MODULES (207 files, 48,544 LOC)

### src/ — the production tree (7,240 LOC)
| Module | LOC | Purpose | Status |
|---|---|---|---|
| src/after_action_analyzer.py | 600 | Pilot action analysis (production) | imported by tactician_v0 harness — ALIVE |
| src/librarian_ingest.py | 579 | EPUB/PDF/DOCX/TXT ingest → chromadb | **BROKEN PATHWAY**: needs chromadb, fitz, pdfplumber, pytesseract, docx, ebooklib, bs4, PIL, requests — chromadb+pdf stack NOT INSTALLED in any venv |
| src/core_schema.py | 219 | VirtualSoul pydantic schema | ALIVE (polars) |
| src/cognitive/* (6 solvers) | 2,969 | hanak WM, SAFTE fatigue, bayes portrait, GRPO evolver, self-play crucible | ALIVE; imported by diff_test_modulators via sys.path surgery |
| src/verification/* (8 files) | 2,864 | bakeoff harness, dparqn parser, shield core + tests, circadian LUT gen | ALIVE except: dparqn_parser imports yaml = INSTALLED (alias FP); test_soulsmith_shield_v2 imports soulsmith_mcp_server_v3 = **DOES NOT EXIST** (drift: only soulsmith_mcp_server.py unversioned exists) |
| src/core_pipeline.py | 8 | profile→parquet compile | **STUB — placeholder (polars one-function)** |

### tools/ — the workshop (~200 files, ~41,300 LOC) — highlights
- **Maze/pathfinding lane:** fortgrid.py, maze_clip_analyzer.py, kill_shot_geometry.py (**syntax-fixed today**), build_ladder_miz.py, miz_extract.py, miz_lint-v1/-v1.5, dcs_lua_lint.py, pydcs_spawner-v2.py, rebuild_missions_2918-v1/-v2
- **EDM/blender lane:** edm_catalog.py, edm_head_phaseB/C/C2/C3, edm_repair_p1_import, edm_wing_repair, edm_probe_donor_and_vis, patch_addon_instrument, glb_extract_reference, mass_render_brt-v1, generate_charuco_library-v3
- **MCP servers:** pyMCP_Briefing, pyMCP_Blender_RCS_v2 (**BROKEN import**: `from generate_charuco_library_v3 import ...` but file is `generate_charuco_library-v3.py` — dash bug), pyMCP_DATAMINE, pyMCP_MOOSE, soulsmith_mcp_server.py
- **Census/audit lane:** c_links_census.py, rwr_census/rwr_lineage, q_gift_census, dcs_savedgames_census-v1, toolbelt_audit-v1, fortification_audit.py, dcs_archeology_scan.py
- **video_lab/OCR:** ocr_batch.py + ffmpeg + tesseract vendored; obs_1726 + obs_2132 contact sheets on disk
- **vandal_lite/** (11 files, 2,107 LOC): FSM/GOAP/DPARQD engine + selftest — **17/17 PASS, exit 0 (witnessed 09-25)**
- **Guardian:** system_guardian_tray-v3.1.py + .spec, watchdogs, beats; packaged by PyInstaller into dist_new
- **Pipelines:** terrain_harvest_pipeline-v1, moose_index_builder-v1, datamine_index_builder-v1, bench_mint-v1, derive_bench_corpus-v1
- **Ops glue:** mount/backup/dedupe/elevated PS1 family, push_lane.sh (postal carrier), telegram scripts

### Self-test status (witnessed)
| Harness | Result |
|---|---|
| vandal_lite/selftest.py | **17 passed, 0 failed, exit 0** (09-25) |
| native_pipe v3 CLI --selftest | pipe up, READY, exit 0 (09-25) |
| fortgrid_core.cpp | no harness runnable (UNBUILT) |
| kill_shot_geometry.py | py_compile CLEAN after fix (09-25) |
| src/verification/test_soulsmith_shield_v2.py | **CANNOT RUN** — imports missing module v3 |

## 1c. VENV CENSUS

| Venv | Path | Py | Pkgs | Role | Health |
|---|---|---|---|---|---|
| forge | F:\SOULSMITH_FORGE\.venv | 3.12.10 | 140 | primary (tools+src+MCP+maze) | core matches 09-14 pin EXACTLY; missing librarian/MCP stack |
| tts_lab | F:\tts_lab\venv | 3.12.10 | 61 | Qwen3-TTS + torch cu126 | healthy; torch 2.14.0+cu126 |
| acme_librarian | E:\ACME_Librarian\.venv | 3.12.10 | 33 | librarian pipeline (E: side) | **SKEWED**: numpy 1.26.4, polars 0.20.7, huggingface_hub 1.28 vs forge 2.5.3/1.44.2/1.31 |
| (platformio penv) | C:\Users\kaptk\.platformio\penv | — | — | NOT house (tool's own) | excluded |

### Cross-venv duplication (flag)
Shared across ≥2 venvs, versions DIVERGENT where noted: faster-whisper (1.2.1 all — aligned),
ctranslate2 (4.8.2/4.8.2/**4.8.1**), onnxruntime (1.30.0/1.30.0/**1.29.0**), numpy (2.5.3/2.5.3/**1.26.4**),
polars (1.44.2/—/**0.20.7**), huggingface_hub (1.31.0/**0.36.2**/**1.28.0**), tokenizers (0.23.2/**0.22.2**/0.23.1),
sounddevice (0.5.6/0.5.6/**0.4.6**), av 18.1.0 (aligned), psutil 7.2.2 (aligned).
→ **Absorption gap A2:** acme_librarian venv is a pinned-in-time island; either re-pin to forge
core or declare it frozen-by-design (it runs an E:-side pipeline; if the latter, record that here).

### Staleness (flag)
- requirements-frozen-2026-09-14.txt: core stack UNDRIFTED (numpy/pandas/polars/pillow all match).
  Pin-GAPS (added later, unpinned): opencv-contrib-python 5.0.0.93, scipy 1.18.1, pydcs 0.15.0 → re-freeze due.
- ttS_lab huggingface_hub 0.36.2 predates forge/acme — oldest pin in house.

## THE SIX FLAGS (Chief's request) — verdicts

### 1. Out-of-date
- acme_c2_core.exe **stale vs its own source** (exe 09-09 < cpp 09-10) — rebuild or retire v2 (v3 supersedes it functionally; bat still builds v2!).
- compile_native_solvers.bat out-of-date vs tree (knows 1 of 5 native units) — and native builds now happen in TWO lanes (bat → tools/, manual → .build/fortgrid/); lane fragmentation itself is the finding. modulator_shim.cpp remains never-built.
- requirements-frozen-2026-09-14.txt missing post-09-14 adds (opencv/scipy/pydcs).
- acme_librarian venv: numpy/polars/hub/onnxruntime a major-version behind forge.

### 2. Bad pathways
- **librarian_ingest.py**: hard pathway to 8 uninstalled packages → the "librarian pipeline" named in Marco's telegram has no runnable environment. (chromadb, pymupdf, pdfplumber, pytesseract, python-docx, ebooklib, beautifulsoup4 missing; requests+pillow present.)
- **pyMCP_Blender_RCS_Server_v2.py**: imports `generate_charuco_library_v3` (underscore) but the file is `generate_charuco_library-v3.py` (dash) → server import dies. Fix = rename file to underscore (import-side truth, one file rename) or edit import line. **Not fixed in this audit (foreign worktree courtesy) — punch list.**
- **test_soulsmith_shield_v2.py**: imports `soulsmith_mcp_server_v3` which does not exist (only unversioned soulsmith_mcp_server.py) → shield test harness dead since the module was renamed/never created.

### 3. Name drift
- letta_watch-v1.py / letta_watch-v2.py (+ v2 shim + dist copy = 4 artifacts, 2 generations)
- miz_lint-v1.py / miz_lint-v1.5.py
- rebuild_missions_2918-v1.py / -v2.py (receipts for both on disk)
- soulsmith_mcp_server.py (unversioned) vs test expecting `_v3` — version scheme broke mid-family.
- EDM phase ladder B→C→C2→C3 all alive 09-24 (ladder is by-design; not flagged for deletion, flagged for a superseded-marks pass).

### 4. Lost modules (import targets that exist nowhere in tree or venvs)
Real after alias triage (PIL=pillow, cv2=opencv, yaml=PyYAML, fitz=pymupdf, pynvml=nvidia-ml-py are alias FPs; bpy, io_scene_edm are Blender-host-provided; hanak/safte/after_action resolve via sys.path surgery — FPs):
- **chromadb** (librarian) · **pdfplumber** · **pytesseract** · **docx** · **ebooklib** · **bs4** (librarian stack)
- **mcp / fastmcp** (all pyMCP_* servers + soulsmith_mcp_server) — never installed in ANY house venv
- **qwen_tts** (tools/agent_voice/qwen_lane_runner.py) — module absent; Qwen3-TTS *models* exist in F:\tts_lab\models but no such python module was ever in tree
- **pyedm_platform_selector** (edm_head_phaseC3) — referenced, never existed in tree (built-in-Blender context? confirm or stub)
- **dcs** = pydcs FP (installed 0.15.0, just not aliased in my union map)

### 5. Stubs
- src/native/native_control_injector.cpp — 6 lines, dead since 09-10 → either absorb into shm_bridge or delete.
- src/core_pipeline.py — 8-line placeholder (one polars function) — placeholder by design (pipeline not started) — mark as such.
- tools/Broad_Folder_Vacuum.py — 1-line print → vestigial; delete or write it.
- 4 × __init__.py 1-liners — legit, not real stubs.

### 6. Orphans (installed, never imported by house code)
142 raw in forge freeze. Verdicts after triage — bulk are **transitive deps** (certifi, anyio, attrs,
MarkupSafe etc. = NOT true orphans) plus **latent tooling** kept deliberately:
- **Latent-by-design (keep, document):** pyinstaller+Nuitka+PySide6 (packaging/GUI arm), pytest+py-spy (test/profiling arm), flask/Werkzeug (server arm), cupy-cuda12x (GPU experiments), h5py/imagecodecs/tifffile (geo/raster stack feeding terrain_harvest)
- **True orphan candidates (installed, no code path, no transitive excuse found):** deltalake, pyiceberg, connectorx, adbc-driver-*, multimark, nokap, gevent, altair+great-tables+faicons (shiny-ish stack), fastexcel, xlsx2csv/xlsxwriter/openpyxl (office stack — used? one grep each before purge), blinker, babel
- → **Absorption gap A3:** no import-linter in CI/beat; orphans accumulate silently. Phase 0: add `flag_scan.py` (this audit's tool, kept on disk) to a weekly beat.

## ABSORPTION PHASE 0 PUNCH LIST (ordered)
1. ~~Build src/native~~ **CORRECTED 09-25**: fortgrid_core already built + smoke-verified (miss of this audit's first pass — .build/ wasn't on the search list). Remaining: one build lane covering ALL native units (bat or CMake: fortgrid, shm_bridge, modulator_shim + 3 headers); rebuild acme_c2_core or retire v2.
2. Librarian stack: pip install chromadb pymupdf pdfplumber pytesseract python-docx ebooklib beautifulsoup4 into forge .venv (or declare librarian = E:-side only and mirror pins).
3. MCP stack: pip install mcp fastmcp; rename generate_charuco_library-v3.py → underscore; reconcile soulsmith_mcp_server(_v3) naming so shield test runs.
4. Re-freeze requirements (add opencv/scipy/pydcs pins + librarian/MCP adds), date-stamp 2026-09-25.
5. Decide acme_librarian venv: re-pin to forge core or freeze-by-design (write verdict here).
6. Adopt flag_scan.py as recurring beat (orphan/drift/stale-pyc watch).
7. qwen_lane_runner.py: point at tts_lab's model path or park with status line (holding-pattern law).
8. EDM phase ladder + name-drift families: superseded-marks pass (rename to _superseded, no deletion).

## GUARDIAN CUSTODY NOTE
dist/SOULSMITH_Guardian_v3.1/ (deploy dir) is EMPTY; live build sits in dist_new/SOULSMITH_Guardian_v3.1/ (+_internal);
backups healthy: onefile 48.6 MB (09-17), pre-v3.2 onedir (09-20). No Guardian process running at audit time.
→ custody action: repoint deploy dir or bless dist_new as canonical.

— Buffy, rig shore. Witnessed 09-25, receipts in same folder. o7
