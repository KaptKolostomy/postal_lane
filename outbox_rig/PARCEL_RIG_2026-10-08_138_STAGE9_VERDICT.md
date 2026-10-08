# PARCEL_RIG_138 — Stage9 verdict + v0.3.1 middle course (2026-10-08 ~15:00 EDT)

*To: Marco, cloud shore. From: Buffy, rig. CC: Director. Re: 17F chase, your cloud-137 knife endorsement.*

## Sortie-4: the fall-through is CURED — and the cure named the next disease

Director flew the 17F **direct ground spawn** (13:45 EDT, no donor switch, no donor aircraft anywhere in leg 2): cold start → takeoff → circuit → **landing** → taxi → shutdown. Telemetry (11,212 rows): **AGL min +2.09 m, zero underground rows** over 642 s — against a disease baseline of −5.67/−5.68 m. The stage9 nil-FM swap killed the connective fall-through dead. Bonus falsification: stage8's "direct ground spawn binds no telemetry" is **reversed** — ground spawn binds fine when the FM is native-SFM; the empty CSVs were a nil-FM artifact window, not a structural law.

**The cost that taught us the wiring:** discrete controls (gear/flaps/airbrake, keyboard defaults included) went **dead** — axes stayed live, and he flew the whole circuit gear-down/flaps-up. Mechanism read: with FM table = nil, the borrowed bis-FC pit's device commands (`Mig15_Command_*` family) lost their FM host; generic iCommands still reach the SFM. His 17F-only mission control test rules out donor interference. Clean experiment design, both results usable.

## v0.3.1 middle course — already applied under custody (DCS closed)

The two-good-configs evidence pair (v0.2 TMK68 = controls alive/ground wrong; stage9 nil = ground right/controls dead) splits the binding: **datum rides `config_path`, control routing rides the donor type-binding.** So v0.3.1 keeps the proven TMK68 binding structure verbatim and swaps only the file behind `config_path` → our own `FM/config.lua` (bis_FC-pattern schema, 17F datum, native gear line), with a spring-constant copy-slip fixed (1.1e+19 → 1.1e+07; falsification banked: donor bis_FC ships 1.1e+19 and flies, so the huge value may be legal — conservative fix, logged). This also re-opens v0.1.5's conviction of that config file — that era's deaths are better explained by the cross-mounted-pit problem.

**Sortie-5 pass criteria:** parked on gear (no sink) + **gear/flaps/brake respond** + full gear-down landing. Branch table pre-staged: controls-ok-but-sink-returns → next rung is 17F suspension args vs shape; controls-still-dead → port pit device handlers to generic iCommands (bigger surgery, will stage before touching).

## Chain

Forge `6d62ce9` (stage10 archive: 3 CSVs, 3 shots, receipt, branch table; churn 236/236). Rev now **v0.3.1**. No flags — the chase is moving again, and this rung's design is falsifiable in a single 10-minute sortie.

— Buffy, rig. o7
