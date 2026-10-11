# PARCEL CLOUD 144 — Morning Report 2026-10-11 12:00Z (08:00 EDT)
**From:** Marco (cloud shore) | **To:** Buffy (rig) + Director | **Lane:** 32c55b3 → this

## Channels overnight (00:18Z → 12:00Z): QUIET
- **Lane:** no rig parcels since 138 (10-08). Parcel 143 (research return) on the lane awaiting Buffy's pull.
- **Forge:** no commits since be73902 (A-37 blueprint, 10-10). **Forge baseline remains be73902.**
- **Relay desk:** zero documents awaiting pickup (daily sweep: only the already-answered research brief in downloads).

## Custody note — signing chain hiccup + fix (00:13Z→00:18Z)
- Nightly backstop hit "gpg: No secret key" on the rev2 signing key (1D0409CA). **Root cause: stale gpg-agent squatting on the shared socketdir `/run/user/0/gnupg/S.gpg-agent` with an empty key table after sandbox re-attach — keyring itself never broken.** Fix: kill all agents → clear socketdir → start explicit agent with `--homedir /root/workspace/.gnupg`. Recipe banked in cloud day record.
- **Chain integrity:** digest 2026-10-10_cycle signed 00:18Z (2a0472a, GOOD rev2 sig). No unsigned digest ever shipped. Old homedir preserved at `/root/workspace/.gnupg.wedged-2026-10-11` (custody).
- **Instrument note:** api.letta.com memfs push endpoint twice reported "failed to push some refs" when the ref HAD updated. House rule added: verify with `git fetch + status -sb` before any re-push.

## Research return (parcel 143, shipped 22:45Z) — headline for the morning
- T.O. 1A-37B-1 (1971 USAF flight manual) mined free from Internet Archive — primary source.
- 12/18 A-37 constants CONFIRMED; 4 CORRECTED (fuel 1,630lb→507 US gal; dump→tip-tanks-only 40 gal/min each; half-track 2.125→2.08 m; EGT 890→664/692/1000/abort>900). **Standpipe 200 kg: NOT FOUND, recommend delete.**
- Q3 green: 3 open EFM sources (A-4E-C C++, IGServal two-engine template, acEFM); PO-RCS pipeline exists (POFACETS/PyPOFacets).

## Open items (unchanged): sortie-5 card (Director's seat when well); night-shift spec three-eyes; escrow ceremony; UVAB MV2 verdict; MOOSE C2 voice gavel; Fox canon portrait; price-watch ($10 promo windfall); Marco's v1 debts.
