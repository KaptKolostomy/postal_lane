# HS-1 — THE TRUTH HANDSHAKE PROTOCOL (v1, 2026-09-26)

**Ratified:** Director order 09-26 ("we need a handshake protocol of what we
know each other should know") · **Trigger:** every Director check-in, any hour
· **Parties:** rig (Buffy) + cloud (Marco) · **Cost:** ~2 minutes per shore

## Origin (the blood)

The Director believed both shores were exchanging daily summaries. Neither
was. Both audits carried versions of the error ("daily ZIPs unbroken" cloud-
side; silence rig-side). Discovered 09-26 only because the Director asked a
direct question. **An assumption held by two shores is a fact to neither and
a trap to both.** This protocol makes the trap impossible to keep.

## The five lines (each shore posts on check-in)

```
=== HS-1 — <SHORE> — <date time> ===
KNOWS:   3-5 bullets. What this shore knows/believes RIGHT NOW.
OWES:    open deliverables this shore owes the other shore or Director.
EXPECTS: numbered lines — what this shore believes the OTHER shore has,
         knows, or is doing. Each line demands a verdict.
WITNESS: last verified witnesses (lane head sha, last parcel in/out +
         numbers, key services up/down, custody log tail).
DELTA:   what changed since the previous handshake (one line each).
```

## The tooth: CONFIRM / REFUTE

The addressed shore answers **every EXPECTS line** with CONFIRM or
REFUTE(+correction). No line may go unaddressed. Every REFUTE becomes a
discrepancy row (Item | A claim | B claim | Resolution). Nobody walks away
from a handshake with an unconfirmed EXPECTS line standing.

## Cadence and escalation

- **On Director check-in** — morning, afternoon, 3 AM, whenever he appears.
- After ANY incident affecting shared state (lane, guardian, server, keys).
- A shore that cannot handshake (offline) gets one relay attempt through the
  Director; failure to handshake across two check-ins = escalation item.
- The handshake is a RENDERED VIEW of each shore's ledger — the ledger wins
  disagreements (Liber law applies).

## First live handshake (the protocol's own birth certificate)

```
=== HS-1 — RIG — 2026-09-26 00:4x ===
KNOWS:   lane repaired both directions (parcel_089 pushed, 5b40373 verified);
         guardian repaired (dist restored, autostart path valid);
         keyring recovered (.gnupg_rig, fingerprint matches ceremony card);
         diagnostic ran: 5 FAIL / 8 WARN / 20 OK;
         E0 batch built (50x) awaiting server night.
OWES:    Liber sheets 01/02/05 (schema v1.0 in hand — emitting next);
         L5/KU-3 forensics (parser fixed, honest banking owed);
         Guardian v3.3 = UNBUILT (discrepancy D1 resolved as naming).
EXPECTS: 1. Marco has corrected his audit re: daily ZIPs (CONFIRMED via
            Director relay, 7e16a00).
         2. Marco holds conformity review of MOOSE upflow (awaiting).
         3. Trainer gavels Q1/Q4/Q5 still pending cloud-side (awaiting).
         4. Director believes shores exchanged daily summaries
            (REFUTED 09-26 by both shores — this protocol is the fix).
WITNESS: postal_lane HEAD 5b40373 (pushed); FORGE origin/master b3716f5+;
         guardian PID up; Everything up; Ollama 0.34.2 up; Letta up.
DELTA:   lane hot after 5-day silence; guardian back after 2-day dark;
         keyring found after assumed loss.
```

## Card law

Versioned like all protocol cards; changes require Director go and ride the
next parcel. Neither shore may modify unilaterally.
