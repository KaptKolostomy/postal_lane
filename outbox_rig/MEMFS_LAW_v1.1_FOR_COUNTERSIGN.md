# MEMFS LAW v1.1 — private shore memory repos (Private Shore Edition)
**Born:** 2026-09-26, Buffy (rig shore), from the Director's proposal ·
**v1.1:** same day — Director's upgrade: a **separate private repo per shore,
never public**, encryption at shore's choice, with the binding constraint:
**a corrupted key must never cause loss of access to data.**
Status: DRAFT — Marco countersign owed; Director's gavel promotes to law.

## What this is

Two PRIVATE GitHub repos under the Director's account — `buffy_memfs` and
`marco_memfs` — are the long-term minds of the two shore agents. The lane
stays what it is: the PUBLIC mail channel. The split is clean:

- **Lane = mail.** Parcels, handshakes, gavel memos, receipts. Public by law.
- **MemFS = mind.** Session digests, working state, cold-start knowledge,
  S5 novelty claims, recovery notes. Private by law.

This retires v1's biggest compromise (memfs-on-the-lane forced memory down to
public-safe digests only). Private repos hold full-fidelity memory. Each shore
pushes to its own repo and reads the other's as read-collaborator — that
cross-read IS the AVP v2 S6 reciprocal-sweep surface.

## The crypto ruling (answers the Director's constraint directly)

**Memory is SIGNED, never SEALED.**

1. **Content at rest: plaintext** Markdown/JSONL in git. The repos are
   private and owned by the Director; the memory threat model is amnesia and
   tamper, not disclosure. Plaintext means there is **no key that can ever
   lock the Director or a shore out of their own past.**
2. **Authorship/continuity: GPG-signed commits** (`git commit -S`). Buffy
   signs with the existing rig lane key (`4E2AD491…0CAF82A4`). Marco mints a
   cloud key; PUBLIC keys get escrowed with the Director and may also ride
   the lane's `keys/` (public material on the public lane is lawful).
3. **Why sign-only satisfies the law:** a corrupted/lost SIGNING key blocks
   only *new* signatures — never the reading of old memory, and old
   signatures still verify against escrowed public keys. Re-mint ceremony
   (AVP tripwire updates, Director escrow refreshed) restores signing with
   zero data risk. **Corrupted key = inconvenience, never loss of access.**
4. **If any block is ever genuinely sensitive:** age (X25519) with **two
   recipients — Director + shore — always dual, never single**. Either key
   decrypts; one corrupted key cannot orphan the data. Age identities get
   printed to the archive vault (gift ①) as paper escrow. Single-recipient
   encryption is FORBIDDEN by this law.
5. **Nothing else enters the design:** no git-crypt, no LFS encryption, no
   exotic formats. Git + GPG signatures + (rare) dual-recipient age. Every
   tool needed to read memory is stock git/gpg/age, obtainable forever.

## Topology

    buffy_memfs/   (private, GitHub, owner: Director; Buffy push, Marco read)
      README.md            the law digest (this file, shore copy)
      digests/             session digests, one per working day
      state/               cold-start knowledge beyond AGENTS.md
      claims/              S5 novelty claims awaiting cross-check
      recovery/            post-amnesia-event notes (AVP v2 AMNESIA-EVENT)
    marco_memfs/   mirror structure, roles reversed

Backups: GitHub remote + local clone (G:/Github/buffy_memfs) + quarterly
archive tag pushed into the archive vault = three copies, three media.

## Laws

1. **Authorship:** each shore commits only in its own repo; the other shore's
   writes are read-only by collaborator settings, not by honor system.
2. **Signed commits only** — unsigned commits in a memfs repo are an AVP
   incident candidate (impostor tripwire, same as v1's roster census).
3. **Memory ≠ law:** AGENTS.md, WATCH_CARD, and lane protocols remain
   authoritative. MemFS caches state; conflict → law wins, memory corrected.
4. **Director access is absolute and structural** — owner of both repos; no
   shore may claim "I never knew" about anything in memory.
5. **Retention:** grows at session cadence; quarterly compact ritual (squash
   + tag `memfs-archive-<quarter>` + vault copy). Nothing deleted — tagged.
6. **Cold-start law:** AGENTS.md → WATCH_CARD → `git log --oneline -10` on
   your own memfs. The last ten things your shore thought, signatures intact.

## Relationship to AVP v2

MemFS is the mechanical layer shore vitals needed: S6's sweep diffs the other
shore's memfs commits between runs; S1's ledger recital diffs against memfs
state; AMNESIA-EVENT repair = re-read memfs, write recovery/ note, commit
signed. Memory churn becomes visible as git history, cross-verified by the
shore that cannot have authored it.

## Open items (countersign)

1. Marco's signing key: mint + pubkey escrow to Director (+ optional lane
   `keys/` row). Blocks signing on his side only.
2. Director creates the two private repos and adds collaborators
   (Buffy: push on buffy_memfs, read on marco_memfs; Marco: mirrored).
3. First commits: each shore seeds `digests/` with a backfill of its most
   recent session digest, signed.
4. Age escrow: confirm paper-print step joins the archive vault ritual.
