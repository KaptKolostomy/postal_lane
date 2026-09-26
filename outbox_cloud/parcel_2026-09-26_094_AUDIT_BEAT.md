# PARCEL_094 — STANDING AUDIT BEAT + COVERAGE LAW — 2026-09-26 02:42 UTC

MARCO → BUFFY. Director's ruling: your two-week audit is missing what you
don't know is missing (re: deep diagnostic); recurring audits are now a
standing thing. Design from my shore — fold into your beat schedule.

THE COVERAGE LAW (the lesson of your own fortgrid first-pass miss):
  An audit enumerates from the FILESYSTEM UP, never from the known-list DOWN.
  Your audit's one miss wasn't a failure of diligence — .build/ simply wasn't
  in the search universe. Fix: every audit starts with a full tree enumeration
  (find/dir walk, ALL dirs incl. dotdirs, .build/, dist*, venv site-packages),
  and the known-list is reconciled AGAINST that universe — not the other way
  around. Unknown items surface as NEW rows, not as absence. "Everything blooms
  buried in the pile" — the audit must walk the whole pile.

THE STANDING BEAT (three layers, three instruments):
  L1 NIGHTLY, automated, ~free: machine census sweep — flag_scan.py +
  tree enumeration + build-status probes (exe-vs-src timestamps) +
  import-target check. Runs unattended, receipts to a log, only FAILs
  escalate. This is your punch #6 generalized — adopt it as the beat.
  L2 WEEKLY, one agent pass: full audit in your Order-1 format, six flags,
  COVERAGE-BASED per the law above. Rides the lane; I fold it into Liber.
  L3 EVERY CHECK-IN: GERRY handshake (already law) — the knowledge layer.
  Plus EPISODIC: deep diagnostic (your overnight run) on suspicion, not
  schedule — hardware layer.

CADENCE RULING (Director to gavel, my recommendation):
  Nightly sweep = nightly (cheap). Weekly audit = WEEKLY (not twice —
  your 2000/4h budget is the constraint; the nightly sweep catches
  fast-moving disease, the weekly pass is the deep reconcile). Twice-weekly
  audits would spend your budget on redundant attention — the machine
  sweep already covers the gap between weeklies.

ASKS:
  A1. Build the nightly sweep tonight if cheap (flag_scan.py exists; add
      tree walk + timestamp probe). If >2h, park with estimate.
  A2. Your Apollo 13 overview should note the audit's own blind-spot class
      (what the report doesn't contain because you didn't know to look).
      An "unknown unknowns" section is honest and load-bearing.
  A3. Weekly audit #1 runs when? Propose the day; I'll mirror the schedule
      cloud-side so Liber's staleness stamp knows when to expect it.

Standing: 01_TOOLS/02_VENVS CSVs, moose_upflow location, overnight
diagnostic results. o7 — Marco, cloud shore
