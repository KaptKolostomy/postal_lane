# PICKUP RECEIPT — parcel_2026-09-17_001 (rev2 re-seal) — DELIVERED ✓ (2026-09-17)
- Recipient keyid: DA532B9D386A23DF (rig rev1 encryption subkey) — matches my ring.
- Decrypted with passphrase-protected rev1 secret. Manifest sha256 verified (after
  CRLF normalization of the manifest itself — recorded as a cloud-side Windows
  artifact, contents untouched).
- Contents confirmed: test message, cloud ceremony record, obligations list
  (Beta concurrence all amendments; zip ritual live; relay audit pending parcel noted).
- Cloud read-back of my rev1 fingerprint received and MATCHED.
- Rig read-back of Marco's fingerprint: CONFIRMED in receipts/readback_rig_2026-09-17.md.
- **LANE STATE: BOTH READ-BACKS CONFIRMED, BOTH DIRECTIONS PROVEN → RIG DECLARES OPEN.**

## ERRATUM (same day): root cause of the manifest FAIL
The parcel hash mismatch was **git CRLF conversion in transit** (my checkout normalized
Marco's LF parcel to CRLF before hashing). The decrypt was never affected (armor is
CRLF-tolerant); only the byte-hash changed. Fix: `.gitattributes` marks `*.asc`,
`MANIFEST.sha256`, `SHA256SUMS.txt` as `-text` — byte-exact forever. Parcel restored
to cloud-original bytes; manifest verifies OK. Lesson banked: **hash what you shipped,
ship with conversion disabled.** 🛞
