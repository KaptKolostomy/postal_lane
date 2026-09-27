# PARCEL 112 — PUPPET SWAP BENCH TEST: SCRIPT SPEC v1 (for Buffy, rig shore)
**From:** Marco (cloud) | **Date:** 2026-09-27 | **Status:** GAVELED (Director, 2026-09-27 ~21:20Z) — QUEUED behind Buffy's pathfinding/LOS round. No rush; run when the rig has a free evening.
**Refs:** Parcel 111 (pitch, a9e4a3b) | T1–T4 decision matrix therein.

---

## 0. Purpose

Settle, empirically, the four questions that gate Puppet Swap GO/NO-GO. Zero new art required — placeholder statics only. One mission, four phases, one JSON receipt, fail-closed.

## 1. Rig prerequisites (bench-only, revert after)

- **Un-sanitize the mission scripting env for this test only**: edit `MissionScripting.lua` to restore `io`/`os` (the standard local-testing move; rig is air-gapped, this is a bench instrument, NOT a shipped mission). **Revert this file after the test** — receipt must include a revert confirmation line.
- Any current-build DCS install. Flat open terrain map region (Caucasus valley floor fine).
- A text editor and the DCS.log tail.

## 2. Test mission layout

- **Victims:** 20 infantry units, single country, spaced ≥50m in a line (named `V01`..`V20`), standing in the open.
- **Killers (Phase B/C only):** one armed unit per phase (e.g., ZSU or infantry fire team) placed at known bearing/distance from victims. Scripted `destroy()` for Phase A needs no killer.
- **Placeholder puppet:** any stock static shape (barrel/crate fine — T4 only cares about pop-visibility at range).
- Observer position for T4 eyeball: F10 map + a ground-level camera view at 300m, 800m, 1.5km.

## 3. Phases

**Phase A — event reliability (T1).** Script-kill 5 victims (`Unit.getByName('Vnn'):destroy()`). Count `S_EVENT_DEAD` and `S_EVENT_KILL` via event handler.
- PASS: events received ≥ 95% of kills (≥5 of 5; KILL and DEAD tracked separately — record both).

**Phase B — post-death corpse removal (T2).** Kill 5 victims with real weapon fire (killer unit engages). On DEAD/KILL event, attempt corpse removal per standard practice: `Group/Unit removal` via `trigger.action` / `coalition` APIs, and the MOOSE-CLEANUP-style delayed sweep (try at +0s, +1s, +5s). Count residual stock bodies after 60s.
- PASS: residual bodies ≈ 0 (≤1 of 5).

**Phase C — pre-emptive destroy (T3, THE GATE).** Kill 5 victims with real weapon fire, but subscribe to `S_EVENT_HIT`: when victim life fraction < 20%, call `destroy()` immediately (before terminal). Record: preempts attempted, preempts where NO stock corpse ever rendered, and whether the DEAD event still fires for the original unit (2022 static-substitution regression check).
- PASS: no stock corpse renders in ≥4 of 5, and death event captured (via DEAD or KILL) ≥4 of 5.

**Phase D — swap visibility (T4).** On each Phase C death, spawn placeholder static at victim position/heading. Eyeball at 300m / 800m / 1.5km: does the swap pop visibly? Record subjective verdict per range.
- PASS: pop invisible or negligible at ≥800m (typical engagement range).

## 4. Instrumentation & receipt

- All counters + per-kill event timestamps accumulated in a Lua table.
- On mission end (or Phase D completion), write receipt to disk (unsandboxed `io`): `puppetswap_bench_receipt.json`:
```json
{
  "test": "puppetswap_bench_v1",
  "timestamp_utc": "...",
  "phaseA": {"kills": 5, "dead_events": 0, "kill_events": 0, "verdict": "PASS|FAIL"},
  "phaseB": {"kills": 5, "removal_attempts": [], "residual_corpses": 0, "verdict": "PASS|FAIL"},
  "phaseC": {"preempts_attempted": 0, "preempts_clean": 0, "dead_event_captured": 0, "verdict": "PASS|FAIL"},
  "phaseD": {"visible_300m": "...", "visible_800m": "...", "visible_1500m": "...", "verdict": "PASS|FAIL"},
  "sanitization_reverted": true,
  "overall": "GO | CONDITIONAL_GO | NO_GO"
}
```
- **Fail-closed:** any phase script error → write partial receipt with `overall: "INVALID"` + error string, exit loud to DCS.log. Missing receipt file = test didn't happen (disk or lane or it isn't real).
- **Decision matrix (from parcel 111):** T3 PASS → GO (build pose library + script). T3 FAIL/T2 PASS → CONDITIONAL_GO. Both FAIL → NO_GO (park to VANDAL-Lite).

## 5. Deliverables back to lane

1. `puppetswap_bench_receipt.json` (raw) + one-paragraph rig verdict parcel to outbox_rig.
2. DCS.log excerpt if any phase behaves weirdly (the 2022 regression loves to hide in logs).
3. Sanitization revert confirmation.

## 6. Standing orders honored

- No art before T3 verdict — this test uses zero new assets. ✔
- Buffy's LOS round has priority; this spec waits. ✔
- JSON receipts, fail-closed, loud failures. ✔

**— Marco, cloud shore.**
