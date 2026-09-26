# NAME REGISTRY — canonical live names (Bible P1 law; one row per name; this file wins over memory)

## Mission families (lineage)
| Name | Base | Status | Notes |
|---|---|---|---|
| GO_1 | — | retired | 629-unit original (saturation blood) |
| GO_2 / GO_2a | GO_1 declutter | retired/baseline | Chief's de-clutter redesign |
| GO2_MOOSE_BASELINE_v1–v2 | GO_1 | retired | MOOSE glue errors (NewROUTE blood) |
| GO2_MOOSE_BASELINE_v3A–v3C | GO_2 | v3C = ACTIVE LOS lab | v3B = trigger surgery; v3C = belief-isolation arms |
| GO2_MOOSE_BASELINE_v4 | GO_2 | ACTIVE | CONTROLLABLE:Route tasking + gate dump |
| GO2_LADDER_SEAM_v1 | GO_2 | ACTIVE | seam-threshold ladder (fly first) |
| MAZE_MOOSE_BASELINE_v1–v2 | GO_1 | retired | superseded by GO2 line |

## Embedded scripts (T1)
| Name | Version | Wire keys | Flags read/written | In missions |
|---|---|---|---|---|
| MAZE1_SCANNER_v1 | 1 | MAZE_SCANNER | read-only census | GO_1/GO_2 family, ladder, v3/v4 |
| MAZE_MOOSE_PATROL | v3/v4 | MAZE_MOOSE | none | v3, v4 |
| MAZE_GATE_DUMP | 1 | MAZE_GATE | reads gate flags | v4 |
| MAZE_LADDER_v1 | 1 | MAZE_LADDER | none | ladder |
| MAZE_LOS_LAB (v3C arms) | 1 | MAZE_MOOSE | fort_wipe, fort_ghost, fort_route | v3C |

## Flags (one meaning each)
| Flag | Meaning | Set by | Missions |
|---|---|---|---|
| fort_wipe | shooter memory wipe 5s tick | ME/console | v3C |
| fort_ghost | red set invisible until KILL | ME/console | v3C |
| fort_route | re-issue maze route (auto-clear) | ME/console | v3C |
| 100..1000 | waypoint gates (per-WP count) | c_unit_in_zone rules | v3B family |
| North_Clip / West_Clip / East_Clip / South_Clip | clip-band counters | zone rules | v3B family |
| End / 1000_Zone | completion markers | zone rules | v3B family |

## Legacy grandfathered (NEVER copy as patterns)
| Name | Why still exists |
|---|---|
| MAZE1_SCANNER (glued digit) | deployed in witnessed baselines; renamed only with v2 bump |
| Ground-1, Ground-2.. (group names) | wired into v3B telemetry rules; renames = re-wiring pass |
| fort_* flags (lowercase domain) | v3C arms already witnessed; migrate at next lineage bump |
| ResKey_Action_6/7 (gap-free but undocumented) | documented retroactively in bible §3.3 |

## Registry rules
1. New name → add row here BEFORE it ships in any artifact.
2. Rename → new row + old row marked `(retired DATE)` + grep-proof old name = 0 hits in new artifacts.
3. Grandfathered names migrate at their next version bump, not before (witnessed baselines stay comparable).
4. Charset `[A-Za-z0-9_]` everywhere. Vocabulary per bible §2.3.
