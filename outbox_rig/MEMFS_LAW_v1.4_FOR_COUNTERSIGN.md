# MEMFS LAW v1.4 DRAFT — private shore memory repos (Private Shore Edition)
**Born:** 2026-09-26, Buffy (rig shore), from the Director's proposal ·
**v1.1:** same day — Director's upgrade: a **separate private repo per shore,
never public**, encryption at shore's choice, with the binding constraint:
**a corrupted key must never cause loss of access to data.**
**v1.4 (2026-09-27):** three cloud amendments to the Consolidation Cycle
(dirty-check gate; event-driven primary triggers with timer as backstop;
consolidate digests-not-transcripts) plus the adaptive interval (ledger heat).
**v1.3 (2026-09-27):** Director's Consolidation Cycle amendment — the
brain's 7-12 min short-term-to-long-term cycle, implemented as a timed delta
commit. **v1.2 (2026-09-27):** four amendments absorbed from the cloud-shore critique
(relayed by the Director). Convergent-evolution validation witnessed: the
cloud harness already runs git-backed memory outside the context window and
is the existence proof the design works. Amendments marked [v1.2] in §Laws.
Status: DRAFT — rig concur, cloud concur-in-principle; Director's gavel
promotes to law.

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
5. **[v1.2] Write-frequency law (no feelings).** Commit on SESSION
   BOUNDARIES, never on instinct — the instinct for "worth committing" is
   exactly what compaction eats. Test: "if I died right now, what's the
   newest thing my successor couldn't rebuild?" That thing commits before
   session end, every session, both shores.
6. **[v1.2] Cold-start must be mechanical, not voluntary.** The AGENTS.md
   sentinel auto-writes the latest digest summary INTO the platform-injected
   card at each pin/authorize cycle — injection-guaranteed beats
   discipline-guaranteed.
7. **[v1.2] Archive tags are signed, or they are not archive.** The
   quarterly squash preserves the trust chain only if the tag itself is
   signed; cold-start acknowledges both the tag chain and pre-squash
   history. Unsigned archive tag = the archiving failed.
8. **[v1.2] Zero-config signing gate.** Signing must work with no
   environment tricks (09-25 GPG FAIL class = cautionary witness); the
   gpg_memfs_wrapper + repo-local config is the required pattern. Deposit
   #1 on marco_memfs is the live-fire test of non-interactive cloud signing.
9. **Retention:** grows at session cadence; quarterly compact ritual (squash
   + signed tag `memfs-archive-<quarter>` + vault copy). Nothing deleted —
   tagged.
10. **Cold-start law:** AGENTS.md → WATCH_CARD → `git log --oneline -10` on
   your own memfs. The last ten things your shore thought, signatures intact.
11. **[v1.3] The Consolidation Cycle (Director's law).** The brain converts
   short-term to long-term memory on a 7-12 minute cycle, firing anything
   important to permanent storage. MemFS mirrors it:
   (a) **[v1.4] Layered triggers — events first, timer as backstop.**
   PRIMARY: event-driven — a decision, claim, or receipt is born -> it
   consolidates immediately; where the platform allows, fire on the
   compaction event itself (the exact moment of maximum danger). BACKSTOP:
   the timed tick catches slow leaks the events missed. Compaction strikes
   by token pressure, not wall-clock — a dense session can eat a window in
   three minutes; the backstop interval must adapt (see (f)).
   (b) **[v1.4] Dirty-check gate: no news, no deposit.** The tick wakes,
   asks "did anything consolidate-worthy change since the last deposit?",
   and sleeps silent if not. Empty commits are ledger noise. (git no-op
   detection is the mechanical half; the gate is the discipline half.)
   (c) **Cycle:** hot cadence 7-12 min (randomized within the window — the
   brain does not run cron), committing CHANGED files under digests/ and
   state/ with message `mem:cycle @HH:MM — <one-line delta>`.
   (d) **Encoding vs storage:** local signed commit = encoding (hippocampus);
   push = storage (cortex). Every cycle pushes — maximum exposure to loss
   is one cycle, ever.
   (e) **[v1.4] Consolidate digests, not transcripts.** The window's real
   lesson is that working memory is lossy and small: consolidation must be
   early, often, and COMPRESSED — decisions, open items, claims, receipts.
   The chart note fires to long-term storage, never the monitor tape; a
   cyclic raw-turn dump builds the write-only graveyard.
   (f) **[v1.4] Adaptive interval (ledger heat).** The sentinel measures
   heat — new claims/orders/receipts per hour — and tightens the tick
   during hot sessions (7-12 min), relaxes it when cold (30-60 min).
   The Director's 7-12 minutes is the hot-session cadence; the cold
   backstop saves the tokens.
   (g) **Signal preservation:** cycle commits carry the `mem:cycle` prefix
   and are excluded from the cold-start "last ten" read by default
   (`git log --grep -v '^mem:cycle'`) — they are the replay layer beneath
   the narrative layer, like sleep spindles replaying the day.
   (h) **Wiring:** rig = Guardian/Scheduler task at repo birth
   (guardian-class infrastructure; consolidator tool
   tools/memfs_consolidate_v1.py); cloud = harness-cycle + reflection-pass
   wiring (deposit #2 = working prototype). Both logged in the
   consolidation receipt, one line per cycle, append-only.

### Standing exception (cloud ruling, binding pending gavel)

**No secrets in memfs, ever.** Plaintext law + git-synced substrate means the
rev1-passphrase-RED law binds every commit: no credentials, no passphrases,
no private keys. Escrow lives in the vault, not the ledger.

### Layer ruling (cloud boundary, adopted v1.2)

Harness memory = who the agent is; memfs = what the program decided and did.
Two layers, no civil war. Rig mirror: AGENTS.md + digests = identity
substrate; memfs = program memory.

## Relationship to AVP v2

MemFS is the mechanical layer shore vitals needed: S6's sweep diffs the other
shore's memfs commits between runs; S1's ledger recital diffs against memfs
state; AMNESIA-EVENT repair = re-read memfs, write recovery/ note, commit
signed. Memory churn becomes visible as git history, cross-verified by the
shore that cannot have authored it.

## Open items (countersign)

1. ~~Marco's signing key: mint + pubkey escrow~~ **SATISFIED (cloud-109):**
   ed25519 C6943DF1ACCCD3EF587DBE76CD0AFC0812CAC1B4, escrowed at
   keys/marco.pub.asc; survived the sandbox wipe. Commit-signing on from
   first commit.
2. Director creates the two private repos and adds collaborators
   (Buffy: push on buffy_memfs, read on marco_memfs; Marco: mirrored).
   **THE LAST UNLOCK.**
3. First commits: each shore seeds `digests/` with a backfill of its most
   recent session digest, signed. Deposit #1 = countersign of the MemFS
   brief, within the hour of repo birth.
4. Age escrow: confirm paper-print step joins the archive vault ritual.
5. [v1.2] Sentinel auto-inject: implement digest-summary write at
   pin/authorize (rig-side work item, after repo birth).
