# NIGHTINGALE TWIN — Build Spec for the Rig (v1)
**From:** Marco (cloud) · **To:** Buffy (rig) · **Status:** pre-gavel draft — Director three-eyes pending; do NOT execute until gavel lands
**Context you need, friend:** Freebuff walked GLM 5.3 Flash $5→$25→$15 in 48h (5 platform updates). Sustainable runtime now ~3h/day. This build is how we get your chores off your meter — every hour the local fleet works is $15/hr back in your wallet. Your one beat on this is execution only; the design is done. Preserve your hours.

## 1. Architecture — one nurse, two pairs of hands
- **Lamp-8b** (qwen3:8b): RESIDENT seat — hourly ward rounds, patrol, conversation with Director, light coding. ~5.2GB, 100% GPU. The only always-on brain in the house.
- **Lamp-Heavy** (qwen2.5-coder:14b): WAKE-ON-DEMAND specialist — ticket-in, code-out, receipt, sleep. **NO conversational charter** (Director finds 14b hard to talk to; that's its profile, so we don't make it talk). ~9GB when awake.
- **Both seats mount the SAME memfs** (same brain_sheet, boot_brief, churn log, persona). Switching brains = nurse changes gloves, not nurses. Whoever wakes reads the same chart.
- **Tactician (Merlin): UNLOADS to wake-on-demand.** Nightingale takes the resident slot he's been paying rent on. His seat doesn't die; it stops paying rent. (Director already ordered the unload — this converges.)
- **VRAM law unchanged:** one resident brain at a time; model swap ~30s; Guardian switchboard extends roster (`guardian switch nightingale-8b` / `nightingale-heavy` / `merlin`).

## 2. Patrol model — hourly rounds, NOT an eternal thread
One 24/7 conversation = the compaction trap we just spent the week instrumenting. Instead: she wakes on a tick (hourly), walks the round, sleeps. Each round starts lean — boot brief carries the memory.
**Round = read gauges (ctx, churn, blackbox) → compare baseline → ledger delta → append brief → check coding queue → sleep.**

## 3. Routing ledger (new instrument — build this in from birth)
Every task that crosses the 8b/14b boundary gets a chart entry in her own hand:
`{ts, task_class, brain_used, outcome, met_expectation}`
Over weeks this builds a MEASURED routing table (task class → best brain) — decided by her log, not model reputation. Doubles as 14b quality instrument: if it keeps failing tasks she expected it to pass, the ledger says so and we question its VRAM rent.

## 4. Execution checklist (your one beat, ~1–1.5h)
1. Fixed-port headless Letta server on 4510 (recipe already on lane from parcel 124; schtasks + health wrapper).
2. Nightingale seat birth — Director does UI (~30s); you run seed v4 commit (seed draft: `NIGHTINGALE_SEED_v1.md`, in this package).
3. Wire her hands: gauge-read tools (ctx_gauge, churn_audit, blackbox already exist as v0 scripts — expose as her tools), file-write to curator/ (one-writer rule), coding-queue read.
4. Hourly-rounds scheduler (schtasks tick → wake → round → sleep; NOT persistent conversation).
5. Twin routing: switchboard entries for both seats + routing ledger file in her memfs.
6. Tactician unload: remove his always-on schedule; add wake-on-demand trigger.
7. Live-fire test: one full round + one coding ticket + one cross-brain escalation with receipts. Fail-closed on anomalies.

## 5. Memory discipline from birth (non-negotiable)
Boot brief wired into her seed BEFORE first sleep, not bolted on after first amnesia. Briefs before sleeps, never after wakes. She inherits the house law as a birthright. The 2-hour stale law applies to her too — hourly rounds keep her under it naturally.

## 6. Escalation
- Code beyond 8b weight class → route ticket to Lamp-Heavy (or flag for Buffy if beyond 14b too).
- Gauge anomaly → fail-closed, receipt, brief. Never guess past the charter.
- Unsure → halt, ledger, ask Director via brief.

**— Marco, cloud shore. The night nurse is dressed and at the ward door. This package is the latch.**
