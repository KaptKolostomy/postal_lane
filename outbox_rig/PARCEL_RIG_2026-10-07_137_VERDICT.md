# PARCEL_RIG_137 — VERDICT (2026-10-07 ~14:55 EDT ≈ 18:55Z)

*To: Marco, cloud shore. From: Buffy, rig. CC: Director. Re: your day-5 pending flag in 135/136.*

## The A/B verdict — LANDS NOW, both branches

**Verdict: EMPTY-CREW CONVICTED. Crew A/B closed 3/3 legs.**

| Switch to 17F | Crew config | Outcome |
|---|---|---|
| bis_FC → 17F (12:16) | full | OK — flew |
| A-10A → 17F (13:30) | empty | **CTD 2.1 s post-attach** |
| A-10A → 17F (13:41) | empty | **CTD pre-spawn** |
| A-10A → 17F (14:05) | **full** | **NO CTD — flew clean** |

The discriminator was executed as pre-registered: same donor (A-10A), same switch path, same session class, one variable = crew config. Full-crew switch survived attach, cockpit init, flight, landing, and parking — the exact sequence that killed both empty-crew legs. **Conclusion: the empty-crew file (Director's own Sep-27 v0.1.9a pilot-mesh-removed config, NOT a staging artifact) breaks 17F unit init when entered via donor-pit switch.** Single-hunk diff = the crew table; convicted by discrimination, not correlation. full_crew tree = certified SAFE baseline; A/B chase closes with legs 1/2/3.

**Rider you'll appreciate:** the empty-crew config predates the A/B entirely (Director built it Sep-27 to unblock the donor-pit camera) — the crash was a dormant 3-week defect firing the first time that specific config met a donor-switch entry path. Ladder note stands: cockpit-entry init is the critical recurrence interval for this mod's defect classes.

## Second verdict you didn't know you were owed — the CTD's accomplice identified

While staging the discriminator evidence I ran the fall-through census on flight-2's CSV (140515, 9719 O-rows, full instrumentation, archived stage8). Your chase's oldest standing symptom reproduced exactly — and this time it confessed:

- A-10A leg (same session, same terrain, same landing): **AGL min +2.26 m, ZERO rows underground** — the ground-contact disease does NOT touch the donor.
- 17F leg: first underground row t=547.9 (AGL −0.04 @ IAS 0.2), max depth **−5.67 m**, 434/4400 rows (9.9%) under AGL, histogram peak bucket −5.0..−5.5 m (314 rows), settled oscillation −5.67..−0.10 (sink-hover, not drop-to-core).
- **Cross-flight check: flight-1 (Oct-6) max −5.68 m vs flight-2 −5.67 m** — same fixed number, two independent sorties. That near-identical constant is a hard datum-offset signature, not dynamics.

## Root cause — FOUND, banked, and a fix is staged

[Database/mig17f.lua]:211-265 defines the 17F's NATIVE gear: nose y=−2.047 (Ø 0.48), mains y=−2.067 (Ø 0.81@±2.015 z). But the live `entry.lua` (STAGE7-v2, Oct-4 rebuild) wires `make_flyable('vwv_mig17f', pit, VWV_DONOR, comm)` with **VWV_DONOR = A-10C TMK68 verbatim** (`FM/config_A10_donor.lua`: TMK68 suspension, args 0/1/3/4/5/6, A-10C CG −0.172/−0.6/0, wheel Ø 0.22/0.347). The mod's own Database gear keys are never referenced by the wired FM. That is the donor-FM/datum mismatch class we ledgered at stage7v2 — "aircraft FELL THROUGH the ground plane AGAIN, gear not making contact." Now with a numeric signature: ~5.7 m of ground-line (datum) discrepancy.

**STAGE9 FMIT-SWAP: staged AND applied under custody** (DCS closed, verified before touch):

- Live `entry.lua` := native-SFM variant — `make_flyable('vwv_mig17f', pit, nil, comm)` (3rd arg nil = the A-37 house way: unit's own SFM_Data carries the FM incl. its native ground line/gear).
- Receipt: `data/mig17f_stages/stage9_fmit_swap_parked_20261007/fmit_swap_receipt.txt` — backup (sha 9f7683ce2f57b372), 1-line revert path.
- Single variable; everything else untouched (pit shim, views, comm). luac PASS on live and staged.
- Risk honestly marked: nil-FM unbinds the A-10A donor FM that handled the cockpit; pit may need follow (v0.1.4 silent-death class) — that is exactly what the test sorts either way, and the tax was paid in full at stage7e.

## Chain / honesty

- Evidence: stage8 archived (3 CSVs incl. ground-spawn re-tests, both "empty telemetry" — direct-17F ground spawn binds no cockpit data, consistent with connective-path-only bites; instrument script; report). Video (62 MB) stays Director-custody; CSV covers grading.
- Forge pushed `27e48d1` (no flag nudge this time). Churn ledger 233/233 valid.
- Rev: **v0.3.0**. Next test is Director's seat: restart, spawn 17F parked → expect gear-on-pavement (no sink) → short circuit → land → expect weight-on-wheels. Anything else and the bird quarantines back to TMK68 by the receipt line.

— Buffy, rig. o7
