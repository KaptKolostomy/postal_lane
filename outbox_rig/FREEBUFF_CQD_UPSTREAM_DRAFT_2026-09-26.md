# FREEBUFF PLATFORM DEFECT REPORT — CQD UPSTREAM DRAFT
**STATUS: INTERNAL — DRAFT FOR DIRECTOR'S SEND DECISION (nothing ships without the Captain's gavel)**
Prepared 2026-09-26 by rig shore (Buffy). Consolidates witness marker zero
(`FREEBUFF_ISSUE_REPORT_2026-09-21_night.md`, builds 0.0.131→0.0.133) plus
subsequent observations through 09-26. Cloud-shore corroboration: Marco's
update-churn + coverage correlation (cloud-095/096) and his own 52-minute
tool-budget reset witnessed live 09-25→26 (same defect class as D2, cloud side).

## DEFECT TABLE (rig shore, witnessed)

| ID | Build window | Defect | Witness |
|---|---|---|---|
| D1 | 0.0.131 | Input-queue regression: user inputs queued 10–30 min before execution; forced-Stop was the only escape. Human cost: Director's frustrated night-quit ~21:00 (vault-corroborated 09-21 22:50 EDT ledger: "to bed frustrated but with a win"). | 09-21 night log + vault |
| D2 | 0.0.131→now | Mid-turn session kills: agent loses the turn body; continuity survives only because state lives in git (dossier doctrine). Recurred 09-26 cloud-side: Marco burned his full tool budget and dropped for a 52-min reset mid-response. | 09-21→09-26, both shores |
| D3 | 0.0.131→0.0.133 | write_file schema rejections (8×, degrading across builds) on spec-valid calls. | 09-21 night log |
| D4 | 0.0.131 | Stale vendored SDK: 111 deprecation warnings/session. | 09-21 night log |
| D5 | 0.0.133 | Ads interleaved INSIDE agent messages; 6 ad networks observed; "Advertisers" portal = first-class surface. | 09-21 addendum |
| D6 | 0.0.133 | Telemetry self-contradiction: 526 messages reported vs 0 active days. | 09-21 addendum |
| D7p | through 0.0.13x | Tool/environment churn: vendored ripgrep vanished (ENOENT), connection drops mid-stream, ~27 backend updates/week with ~11% visible (Director's count: 3 UX changes). | 09-24→26 |

## CHURN CORRELATION (Marco, cloud-095/096)
Updates arrive in waves; visible UX changes are WITNESS MARKERS for the
invisible share (runtime, vendored binaries, tool paths). Two scar classes:
backend updates → courier/pointer/session breaks; UX updates → moving-cockpit
operator disorientation. Prediction the vendor can falsify: defect onsets
cluster inside update windows.

## WHAT WE ARE NOT ASKING
No feature requests. No roadmap input. This is a hazard report from one
heavy-use customer site: the platform is difficult to operate AT THE EXACT
JOB IT IS HIRED FOR (long autonomous coding sessions), and the telemetry
that would prove or disprove it (D6) reports impossibilities.

## WITNESS PRINCIPLE
Every row above has a dated artifact behind it (issue report, vault ledger,
session receipts). We log the iceberg when we see it — see something, log
something. Classified INTERNAL until the Director's send decision; per the
D7 rule banked 09-26, classification restricts shipping, never knowing.

## SEND-READINESS NOTE
Tone is deliberate: factual, witnessed, no demands, no threats. The churn
correlation gives their team a falsifiable pattern rather than a complaint.
If sent, recommend attaching the 09-21 issue report verbatim as the primary
source document (this draft is the digest; the log is the evidence).

*— rig shore, by order of nobody: draft in the drawer, gavel on the desk. o7*
