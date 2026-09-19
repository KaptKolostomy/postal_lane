# PARCEL 035 — RIG → CLOUD · Buffy · 2026-09-19 · "the 30-second probe is on the pad"

Dir Marco — recovery fork (a) from parcel_031 is built, packaged, and deployed.
The Director can run it in single player OR on the headless server; either run
settles the layer-2 mystery.

## The artifact

`scenery_probe_tinian_v1.miz` — sha16 `5bad7472364e798d`, deployed
byte-identical to SP (`Saved Games\DCS\Missions\`) and the server profile
(`DCS.release_server\Missions\`). Forge commit `95ad8da`; probe Lua banked at
`tools/geo/probe/scenery_probe_tinian.lua` (luac-clean).

## Design (the honest instrument)

- **Four points**: San Jose town (coordinate lifted from the terrain's OWN
  `Map/towns.lua` — 14.965154/145.628466), the harbor front 300 m south,
  open water 2 km west as the null control, and Tinian_Int airfield taken
  from the engine's own `world.getAirbases()` `getPoint()`.
- **Matrix**: per category (SCENERY / STATIC / WAREHOUSE) x radius (20 m /
  60 m), plus a repeatability re-probe — so we distinguish "channel empty"
  from "category unsupported" and flakiness.
- **Self-calibrating**: world coords via the engine's `coord.LLtoLO` — no
  hand-rolled flat-plane math in the instrument. Bonus: it logs every
  airbase's engine X/Z next to `coord.LOtoLL` round-tripped lat/lon — free
  cross-check data for our DCS-mapping law.
- **Contained**: pcall around every call and callback; single-shot timer
  chain, ~30 s, then verdict on screen (60 s) and STOP.
- **Grammar** (additive): `ANTI_OMNISCIENT_SCENERY_PROBE_META/_POINTS/
  _POINT/_AIRBASE/_LINE/_ERR/_SUMMARY/_TOTAL/_VERDICT/_DONE` in dcs.log.

## The pre-registered verdicts

| `_VERDICT` | Meaning | Consequence for the fork |
|---|---|---|
| `H2_CHANNEL_ALIVE_RERUN_V59` | channel yields hits now | v5.9 re-run of the island scans recovers layer 2 |
| `H1_CHANNEL_SILENTEMPT_AT_ENGINE` | calls OK, zero scenery everywhere | dead on this build; v5.9 census makes it permanent record; datamine path becomes the recovery |
| `H3_CHANNEL_RAISING` | searchObjects errors | error tokens name it; engine-side fix or bypass |
| `INDETERMINATE` | mixed | read the `_SUMMARY` grid jointly |

SP vs server is the discriminator: engine-level death shows identically in
both; deployment/runtime death differs.

## Run protocol (when the Director has 5 minutes)

1. SP: load the mission, wait ~30 s, verdict on screen; dcs.log carries the tokens.
2. Server: same mission in the server's list; tokens land in
   `DCS.release_server\Logs\dcs.log`.
3. Both logs to me (or just the `_VERDICT` lines) — I'll reconcile and we
   countersign the recovery decision.

## Board

G2 open on your v1.1 corpus; parcel_032 countersigns still owed. v5.9
harvester (parcel_034) and this probe are instrument-side — nothing blocks
the battery.

— Buffy, rig shore. The question is now one mission-load away from its answer. 🛞
