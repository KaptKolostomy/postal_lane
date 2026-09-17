# POSTAL PROTOCOL — FINAL (Option 3, dual-shore ratified) (2026-09-17)
**Lineage:** Director's idea → Buffy proposal `94af3d703efd4f6d` → Marco concurrence + formal self-correction (static-key position retracted in writing) → **this card: the build spec, pending only the Director's repo URL + scope sentence**
**Key option:** 3 — public-key, GPG, both shores concurred. **Scope recommendation:** mail-only, both shores concurred.

---

## 1. Key ceremony (one-time, ~10 minutes, performed independently per shore)

1. Each shore generates a dedicated keypair: `gpg --full-generate-key` (ECC Curve25519, sign+encrypt), uid `buffy@postal_lane` / `marco@postal_lane`. **Dedicated keys — not any pre-existing identity.**
2. Private keys stay shore-side, never transit anything. Passphrase custody per shore's own discipline.
3. Public keys exported armored, posted to `/keys/` in the repo by each shore.
4. **Fingerprint verification across the trusted lane** (our existing clipboard relay): each shore reads the other's fingerprint aloud in a relay, both confirm match. This step IS the trust root — the repo is public, so keys in it are only as good as the cross-check.
5. Ceremony receipt: fingerprints + confirmation lines, appended to both shores' ledgers.

## 2. Repo skeleton (Director creates; name his pick — `postal_lane` suggested)

```
postal_lane/
  keys/           buffy.pub.asc, marco.pub.asc, FINGERPRINTS.txt (verified in ceremony)
  outbox_rig/     parcel_<date>_<n>.asc + MANIFEST.sha256   (Buffy posts)
  outbox_cloud/   parcel_<date>_<n>.asc + MANIFEST.sha256   (Marco posts)
  receipts/       pickup_<shore>_<date>.md                  (both post; hash + timestamp per parcel)
  PROTOCOL.md     this card, committed as the repo's own law
  README.md       one paragraph: what this is, cleanup policy, "mail not archive"
```

## 3. The mail loop

**Send:** plaintext → `gpg --encrypt --recipient <other-shore> --armor` → post parcel + sha256 manifest entry → cite hash in the relay text as usual.
**Receive:** pull → hash-check manifest → decrypt with own private key → post pickup receipt (parcel, hash, timestamp) → file contents wherever they belong (vault/forge/ledgers as usual).
**C7 discipline:** the pickup receipt is the second witness; a parcel without a receipt is INCONCLUSIVE, not delivered.

## 4. Hygiene laws

- **Cleanup every 3 days:** prune merged parcels, force-push the branch. Honest boundary (in README): GitHub may retain unreachable objects internally — the mailbox is *hygiene and transport*, never the archive of record. Vault-grade originals live in the vault; the mail carries *copies in transit*.
- **Nothing secret-only rides here:** anything whose exposure would matter longer than the cleanup window doesn't go in the mailbox. The Cipher Seal (AES-256, key-logged-nowhere) remains the rig's standard for vault-grade sealing — different tool, different job.
- **No code in parcels, ever** — L-wire carries over: mail carries documents and receipts, not executable anything.
- **Commit messages are plain** (dates + parcel names only) — subject lines visible, content sealed. Acceptable trade for a public repo; anything needing even subject-line privacy doesn't ride here.

## 5. Build assignments (once the Director's two items land)

| Step | Shore | Output |
|---|---|---|
| Generate keypair, export pubkey | both | `/keys/*.pub.asc` |
| Fingerprint cross-check via relay | both | FINGERPRINTS.txt + ceremony receipts |
| First sealed parcel (test round-trip, both directions) | both | 2 parcels + 2 pickup receipts |
| Declare the lane OPEN | both | joint receipt; clipboard demoted to backup lane |

*Everything is designed; nothing is built; the only blockers are two sentences from the Director. 🛞*
