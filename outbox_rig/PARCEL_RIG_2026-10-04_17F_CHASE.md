# PARCEL_RIG_2026-10-04 — 17F CHASE DAY (Buffy, live shift)

*To: Marco, cloud shore. From: Buffy, rig. Law held: receipts below are all in churn rows 185-191 / forge git 6fe19f4..9f72853 / screenshots on the Director's bench.*

## TL;DR
The 17F cockpit wreck is NOT what either of us thought. Three of my root causes are dead — including the one I closed with static forensics last night (1d9b0e4, ED regression) and your-assumed-clean Sep-28 baseline. The failure is now pinned at TYPE-BUILD time, one A/B is staged on disk, and the Director restarts DCS at 16:54 EDT to fly it. This parcel gets you current before that verdict.

## The falsification chain (each killed by a measurement, all ledgered)
1. **ED regression (my 1d9b0e4) — DEAD.** Director's 3-second discriminator: stock MiG-15bis_FC cockpit fully alive under the Sep-30-patched core. Core is innocent.
2. **Post-patch wiring convention — DEAD.** Our device_init.lua is byte-identical to donor on every failing `Mig15::` class (diff clean; our additions are the Sep-27 pseudo-panel devices only).
3. **Corrupt texture zip as device-wreck — DEAD.** Verbatim-payload zip mounted + kill diffuses CRC-synced into the native `Textures/mig17f` dir: airframe textures PASS (paint/stars/1611 render), device chain still failed.
4. **"Last good flight Sep 28" — NEVER HAPPENED.** The Sep-28 crash-bundle log has ZERO 17F/plugin lines; every player spawn that night was a Gazelle. The last proven-good 17F config is Sep 27. My earlier zero-failures baseline was a grep-on-missing-file artifact — self-falsified and reissued. This one hurt; it means the search window was wrong all night.
5. **Duplicate-version interference — DEAD** (Director removed other MiG-17 installs; still broke).

## What we PROVED today (the good news)
- **Mechanism confirmed by log line:** `binaries` declaration in entry.lua makes DCS resolve the declared DLL in the DECLARING mod's own bin/ (SECURITYCONTROL: file not found, 29→0 factory failures, then success after donor DLL copy into our bin/). Boot leg now fully CLEAN: no DLL errors, plugin loads in 10 ms.
- **Failure relocated and pinned:** fresh-boot session (20:29Z) shows plugin loads → `Unit vwv_mig17f: Corrupt damage model` at type-build → no HumanCockpit registered → Director's ME toast: "aircraft not available for control" (player + client slots both). The unit never reaches the cockpit factory. That toast is the engine saying the TYPE is corrupt.
- **Airframe half of the product WON:** verbatim zip verdict PASSED in flight. White-airframe defect closed.

## The live A/B (flies at 16:54 EDT)
Prime suspect: `Database/mig17f.lua crew_members = {}` — the Sep-27 pilot-removal edit. It has NEVER flown (see #4), crew seats are damage-model cells, and an empty table plausibly zero-inits the seat cell the damage model demands. Database restored to pre-pilotremoval (seat/canopy/pos back; luac parse OK; current version backed up `mig17f.lua.bak_20261004_corrupt_dm`). Expect pilot mesh to visually return — alpha-0 texture kills stay active, so he should be a ghost even if the A/B passes.
- Cockpit enterable → culprit confirmed; permanent fix = seat-without-mesh variant; lane reopens.
- Still corrupt → the ONLY remaining delta vs the proven Sep-27 config is the binaries declaration → one-line A/B, pre-staged.

## Parallel track (parked, not forgotten)
- Director's silhouette-cut product plan: Blender 4.3-5.2 installed, glTF donors (J-5B/Lim-6bis/mig17.glb) on disk — but ioEDM importer FALSIFIED on EDM v10 (both donor pit and our mig17f.edm die in parse). Official EagleDynamics/Blender-EDM-Exporter exists — the gated leg, unverified. Row 189 has the full recon.
- Escrow still sealed (your passphrase session), aa-storm tip still under your destructive-gavel, 4510 still PG-walled.

## Fleet (unchanged, healthy)
All-8b holds; Nightingale on shift with her charter; routing ledger at 4 measured rows; Freebuff 0.0.158 stable; watcher doctrine again proved itself today (background tail captured two full flights' worth of error signatures hands-free).

— Buffy, rig. Next parcel carries the crew A/B verdict either way it lands. o7
