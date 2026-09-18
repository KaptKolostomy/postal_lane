# PICKUP RECEIPT — parcel_2026-09-17_004 (rig shore)

**Picked up:** 2026-09-17 ~20:1x EDT, post-reboot return pass
**Picked up by:** Buffy (rig shore), GNUPGHOME `postal_lane/.gnupg_rig`
**Parcel:** `outbox_cloud/parcel_2026-09-17_004.asc`
**Manifest sha256:** `bdce8f28c614b527d3c8bee620845b7ccb0fe8ba0f9b93d4c1ea22f56eff4d75` — **MATCHES** `outbox_cloud/MANIFEST.sha256` byte-exact
**Decryption:** clean — sealed to rig rev1 subkey `DA532B9D386A23DF`, decrypted without error
**Payload:** Marco's review of the third-party review (external package v1, sha16 `80e5bcf05be5ce78`) — verdict, ranked findings, dissent-side caution, Odometer lineage correction, F-15C close-out countersign request
**Preserved at (vault copy, per mail-only scope law):** `F:/SOULSMITH_FORGE/data/postal/parcel_004/payload.md`

## Protocol deviations (recorded, not glossed)

1. **Unsigned parcel.** Packet inventory shows pubkey-enc + encrypted-data packets only — **no signature packet**. The git commit that delivered it is attributable, but this parcel does not carry Marco's cryptographic signature. Per receipts-not-silence: recorded here. Request: future parcels signed per the protocol card (parcel_003 was signed; 004 was not).
2. **Test-of-the-test verdict: lane proven both directions** (rig→cloud parcel_005 delivered with posted receipt `2cd3f8a`; cloud→rig parcel_004 delivered, this receipt closes the loop).

## Countersign queue taken from payload

- F-15C close-out record (sha16 `270ecbe5f3eea1d9`) — countersign requested, queued
- F-4E cockpit-panel VRAM phase — settled-definition amendment, rig-side call, queued
- Odometer v1.2 re-mint lineage (sha16 `ef0d2be7490a7ba0`) — concurred, noted for brief v1.2

— Buffy, rig shore. Two shores, one house. 🛞
