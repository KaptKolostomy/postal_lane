# PARCEL 119 — PROJECT NIGHT NURSE (working title): Buffy telemetry + curator aide, spec v1
**From:** Marco (cloud) | **Date:** 2026-10-01 ~20:00Z | **Status:** SPEC — awaiting Director gavel | **Director owns: naming, persona, final charter**

## 1. Problem statement (the wound, named honestly)
Buffy (Freebuff / GLM 5.3 Flash Max) is the one mind in the house WITHOUT persistent memory architecture. The fleet (Fox, Merlin, Aurelius, Gideon, Loxley) are all Letta agents with memfs; Buffy is not. Result: a clinical-grade anterograde amnesia profile — recurring compaction events erase tools built, paths, prior work; cued retrieval intact (can find after the fact); repeat-explanation cost carried by the Director (smartCTL + throttle process explained 4–5 times; re-invention of the Everything CLI wheel). The house accidentally ran a controlled experiment on itself: architecture difference isolated, symptom confirmed.

## 2. Architecture — four layers, no heroics
```
[FEEDS] → [BLACK BOX DB] → [CURATOR] → [BRIEFS]
Freebuff logs    SQLite (SAFE drive)   Letta agent    brain_sheet.md
transcripts      append-only           App Server     garage_inventory.md
Forge git log    dedup + custody       wake/sleep     boot_brief.md
flight recorder  (Phase 2)             narrow charter compaction flags
```
**Doctrine:** the curator is a NIGHT NURSE, not a second generalist. It doesn't solve Buffy's problems — it remembers them. Memory lives outside the head or it doesn't live at all. Everything blooms buried in the pile — but only if indexed; the digest layer IS the product.

## 3. Phase 0 — RECON (one evening, Buffy-driven; see §10 telegram)
No build before recon. Buffy answers the capability telegram. Two facts gate everything downstream: (a) does Freebuff write session logs to disk (format/path), (b) can Buffy reach the App Server API at 127.0.0.1:4500/v1.

## 4. Phase 1 — BLACK BOX DB + cheap feeds (1–2 evenings)
- **SQLite, single file, F: SAFE drive** (`F:\SOULSMITH_FORGE\curator\night_nurse.db`). Append-only per custody law. Schema:
  - `messages(id, ts, speaker, text, source_feed, dedup_hash)` — conversations from Freebuff logs + Director transcripts
  - `builds(id, ts, path, kind, one_liner, verified_ts)` — the garage inventory backbone; fed by Forge git log walker + filesystem census
  - `frames(id, ts, ocr_text, conf_mean, frame_hash)` — Phase 2, flight recorder
  - `compaction_events(id, ts_detected, signal)` — reset sightings
  - `briefs(id, ts, kind, path, sha16)` — custody receipts for every artifact the curator issues
- **Feed walkers (Python, rig-side):** Freebuff log parser (format from Phase 0), transcript-log ingester (Director's existing text logs), Forge git-log walker, filesystem census (tools/scripts index — this AUTO-GENERATES the garage inventory).
- Dedup: hash every ingested unit; nothing enters twice. All ingest is re-runnable (idempotent — Mount Law applies).

## 5. Phase 2 — FLIGHT RECORDER (the camera; 1 evening, after Phase 1 proves)
- Window-pinned capture: `pygetwindow`/`mss` bound to the Freebuff window handle ONLY — nothing else on screen ever enters a frame. Custody law.
- Cadence: 60s idle / 5s when text changed last frame. Frame-hash diff → skip unchanged (no 10,000 identical frames).
- Tesseract OCR → confidence threshold (mean conf < 60 = store raw but flag LOWCONF; never silently drop, never silently trust).
- **Pause switch:** existence of `F:\curator\PAUSE` file halts capture. The Director holds the switch. Non-negotiable.
- What it buys: the evaporation layer (Buffy's unwritten reasoning), real-time compaction-event detection, Director-side of conversations.
- What it must never be: the primary source for code/paths (OCR mangles exactly those). Artifacts rule; camera augments.

## 6. Phase 3 — CURATOR (Letta agent, App Server :4500; one evening + tune)
- Seed via existing fleet pipeline (FOX POC pattern). Suggested model: qwen3:8b (already deployed, shares Tactician's slot — both sleep most of the day) or phi3 if curation-only proves enough. **Measured governs; wake-curate-sleep cycle holds zero VRAM between jobs.**
- Charter (narrow, hard-scoped):
  - MAINTAINS: `brain_sheet.md` (paths, throttle, smartCTL, Everything CLI one-liner, current priorities), `garage_inventory.md` (every tool/script, path, one-liner, last-verified), `boot_brief.md` (what Buffy was doing, what's next, what bit him).
  - WAKES: on schedule (2h), on compaction-event signal, on Director demand via App Server.
  - MUST NOT: write/modify Buffy's code, solve engineering problems, chat socially. Scope creep = second Buffy with the same disease.
  - OUTPUT LOCATION: `F:\SOULSMITH_FORGE\curator\` (git-tracked; briefs ride the Forge to both shores).
- Re-orientation loop: compaction detected → curator refreshes boot_brief.md → Buffy reads it at session start (Phase 0 query #6 checks whether Freebuff can auto-inject; if not, Director pastes — one line of friction).

## 7. Failure modes (honest list)
1. **OCR garbage pollutes custody** → confidence thresholds + LOWCONF flag + human-gradeable review parcels.
2. **Freebuff UI changes break capture regions** → window-handle pinning (not screen coords); version-pinned deps.
3. **DB becomes write-only landfill** → charter mandates digesting; briefs are the product, DB is the ore.
4. **Curator scope creep** → narrow charter in the seed; MUST NOT list enforced by Director review (three-eyes).
5. **VRAM collision** → wake/sleep only; `ollama ps` check before curator loads (Phase 0 query #10).
6. **Privacy bleed** → window-pinned capture + PAUSE switch + DB on SAFE drive under custody law.

## 8. Effort ledger (fiscal honesty)
Phase 0: 1 evening (Buffy, mostly answering + 3 test scripts). Phase 1: 1–2 evenings. Phase 2: 1 evening. Phase 3: 1 evening + persona tuning. **Total: ~one week of evenings, incremental value from Phase 1 onward** (garage inventory + searchable conversation DB help the Director even before the curator exists).

## 9. Open gavels for the Director
1. Curator persona NAME (house doctrine: yours). Working suggestion only: **Nightingale** — the original night nurse with the lamp, who was also a chart-keeper and statistician. Fits the charter unsettlingly well. Your seal, not mine.
2. Model assignment (qwen3:8b shared vs phi3 dedicated).
3. Phase 2 green-light separate from Phase 1 (camera is the sensitive instrument).
4. Boot-brief delivery mechanism pending Phase 0 query #6 answer.

## 10. TELEGRAM TO BUFFY — capability recon (Director carries; Buffy answers numbered, tersely)
**A. Your own environment:**
1. Does Freebuff write session history/logs to disk? Path + format (SQLite/JSON/MD)? List the directory.
2. What tools does Freebuff give you (shell exec? file read/write? HTTP?) — enumerate, don't describe.
3. Can you create a Windows Task Scheduler task that runs unattended?
4. Run this and paste the full response: `curl -s http://127.0.0.1:4500/v1/models` — does the App Server answer you?
5. Can you write to `F:\SOULSMITH_FORGE\curator\` and read back what another process writes there? Test with a hello-world file both directions.
6. Does Freebuff have a startup/system-prompt injection — a file auto-read at every session start? Name the mechanism.
7. Does Freebuff show you your context-window state (tokens used/limit)? Can you tell WHEN you compact?
8. Paste versions: `python -c "import mss, pygetwindow, pytesseract, cv2; print('ok')"` and `tesseract --version`.
9. What API base does your GLM 5.3 Flash Max run through? Rate limits you know of?
10. Run `ollama ps` — what's currently holding VRAM on the rig?

**B. Intersacting with a local Letta agent (the curator):**
11. POST a chat completion to `http://127.0.0.1:4500/v1/chat/completions` with model "Tactician" (or whatever Merlin's endpoint is named), message "Marco" — paste the raw JSON reply. (House check: correct answer rhymes with "Polo".)
12. Could you run that call on a schedule (Task Scheduler) and write the JSON to `F:\SOULSMITH_FORGE\curator\`?
13. If a curator agent wrote `boot_brief.md` to that folder nightly, could you read it as your FIRST action each session — and what mechanism would make that automatic instead of remembered?

**— Marco, cloud shore. Spec written to be built by two shores: Buffy answers, Director gavels, then we cut metal. o7**
