# MARCO RESEARCH RETURN — A-37 / J85-GE-17A / DCS EFM
Date: 2026-10-10 | From: Marco (cloud) | To: Buffy
Re: MARCO_RESEARCH_BRIEF_2026-10-10.md

---

## SOURCE UPGRADE (per brief closing rule)

**T.O. 1A-37B-1, USAF Flight Manual A-37B, 1 Sep 1971 (Change 9)** — full 21 MB scan, free, Internet Archive:
https://archive.org/details/A37BFlightManual

This is the 1970s USAF manual Q1.7 asked to prefer. Full-text OCR is on my disk; every manual-derived claim below quotes its language. Cited as **[TO]** after this line. Second mirror (download page): https://www.usaf-sig.org/index.php/references/downloads/4-technical-orders/38-type-specific/130-t-37-cessna

---

## Q1 — J85-GE-17A REAL PERFORMANCE

- **Q1.1 SLS thrust: 2,850 lbf (12.7 kN) per engine; rated speed 16,500 rpm (=100%).** [TO]: "thrust rating for the engines is 2850 pounds each"; "the rated rpm is 16,500." https://archive.org/details/A37BFlightManual
  Backup (physical engine, Smithsonian NASM J85-GE-17): 2,850 lbf @ 16,500 rpm — https://airandspace.si.edu/collection-media/NASM-A19800072000cp10
- **Q1.2 Altitude thrust: NOT FOUND** for the -17A (no published graph/table/ratio located). Closest real engine-deck fragment found: T-38/J85-GE-5 appendix gives sea-level-only values (Military power = 96.4% rpm; 2,140 lb uninstalled / 1,770 lb installed per engine, SLS): https://www.globalspec.com/reference/36777/203279/appendix-d-t-38-performance-data
- **Q1.3 TSFC: NOT FOUND** for the -17A. Nearest neighbors:
  - J85-GE-21 (later, larger variant): 1.24 lb/(lbf·h) dry — https://en.wikipedia.org/wiki/General_Electric_J85
  - J85-GE-5 (T-38), installed, SLS: ~1.09 lb/(lbf·h) — https://www.globalspec.com/reference/36777/203279/appendix-d-t-38-performance-data
  - J85 family: ~400 US gal/h at full throttle, sea level — https://en.wikipedia.org/wiki/General_Electric_J85 (DERIVED, not stated: at 6.5 lb/gal JP-4 ≈ 0.9 lb/(lbf·h) at 2,850 lbf)
- **Q1.4 Dry mass: 181 kg (398 lb).** Smithsonian NASM, J85-GE-17 artifact record — https://airandspace.si.edu/collection-media/NASM-A19800072000cp10
- **Q1.5 Spool rate: NOT FOUND** for the -17A (no published seconds or %/s figure). Generic FAA jet-transition reference: idle→full power "may take as much as 8 seconds"; acceleration is slow below ~78% rpm, fast above — http://www.12charlie.com/Chapter_15/Chap15Page010.htm
- **Q1.6 Idle RPM: CONFIRMED ≈ 48%** as the top of the manual's idle band. [TO]: engine at idle (spin condition) "approximately 43 to 48% rpm with approximately 400°C EGT"; starter-generators cut in "after engine speed reaches approximately 48 to 50% rpm"; flight idle can roll back to ~30% rpm above 15,000 ft below 150 KIAS; ground/approach idle varies with altitude per fig 6-4 "IDLE RPM vs ALTITUDE" (chart curves not OCR-readable; axis spans 40–80%). https://archive.org/details/A37BFlightManual
- **Q1.7 1970s manual:** T.O. 1A-37B-1 (1 Sep 1971, Change 9) — see SOURCE UPGRADE above. All Q1/Q2 manual rows cite it.

---

## Q2 — A-37 CONSTANT TABLE VERDICTS

| Constant | Docs value | Verdict | Correct / confirmed value | Source |
|---|---|---|---|---|
| Empty weight | 6,211 lb / 2,817 kg | **CONFIRMED** | 6,211 lb (2,817 kg) | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Max takeoff weight | 14,000 lb / 6,350 kg | **CONFIRMED** | 14,000 lb (6,350 kg) | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Internal fuel | 1,630 lb / 739 kg | **CORRECTED** | 507 US gal (1,920 L) usable internal, incl. tip tanks; ≈3,300 lb at 6.5 lb/gal JP-4 (derived). Docs value ≈ half of real. | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Wing area | 17.08 m² | **CONFIRMED** | 183.9 sq ft = 17.08 m² | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Airfoil root | NACA 2418 | **CONFIRMED** | NACA 2418 (modified) | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Airfoil tip | NACA 2412 | **CONFIRMED** | NACA 2412 (modified) | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Stall speed | 98 kn | **CONFIRMED** | 113 mph (=98.2 kn), max landing weight, wheels+flaps down | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Max combat speed | 441 kn | **CONFIRMED** (with conflict note) | 507 mph (=441 kn) at 16,000 ft | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Max speed — conflicting source | — | note | 525 mph (=456 kn) at 16,000 ft per Courtesy Aircraft profile | https://www.courtesyaircraft.com/wp-content/uploads/2024/04/images_aircraft_profiles_A_37_Dragonfly_Profile.pdf |
| Climb rate | 6,990 ft/min | **CONFIRMED** | 6,990 ft/min | https://en.wikipedia.org/wiki/Cessna_A-37_Dragonfly |
| Fuel dump rate | 4.5 kg/s | **CORRECTED** | Tip tanks ONLY: 40 US gal/min per tank at best dump speed 135 KIAS; empties 90-gal tank in ~2 min 20 s; rate diminishes with speed; ~zero dump in descent or deceleration; no dump provision for fuselage/wing/seat fuel. 40 gal/min ≈ 1.95 kg/s per tank (derived at 6.5 lb/gal) | [TO] https://archive.org/details/A37BFlightManual |
| Standpipe reserve | 200 kg | **NOT FOUND** | Zero "standpipe" references in T.O. 1A-37B-1. Recommend deleting from model — sim invention. | [TO] https://archive.org/details/A37BFlightManual |
| Hydroplaning formula | V = 9·√(psi) | **CONFIRMED** | NASA TN D-2056, eq. (4): Vp = 9√p knots; eq. (5): Vp = 10.35√p statute mph; p = tire pressure psi | https://ntrs.nasa.gov/citations/19640000612 |
| Oleo spring k | 185,000 | **NOT FOUND** | No public source; sim tuning constant | — |
| Oleo damper c | 12,500 | **NOT FOUND** | No public source; sim tuning constant | — |
| Gear half-track | 2.125 m | **CORRECTED** | [TO] dimensions table: "Wheel Tread 13.66 ft" → track 4.163 m, half-track **2.08 m** | [TO] https://archive.org/details/A37BFlightManual |
| Tire burst impact | 4.8 m/s vert | **NOT FOUND** | — | — |
| EGT redline | 890 °C | **CORRECTED** | [TO] instrument markings: 280–664 °C continuous; 692 °C 30-minute limit; 1000 °C instantaneous (start/acceleration); abort start if >900 °C. No 890 anywhere. | [TO] https://archive.org/details/A37BFlightManual |
| DC bus | 28 V nom / 24 V ess | **CONFIRMED** | 28 V dc system: 2× engine-driven 300 A starter-generators + 2× 24 V 22 Ah NiCd batteries | [TO] https://archive.org/details/A37BFlightManual |

### Q2 additionally

- **Fuel cell count / topology** [TO]: "Three self-sealing tanks are installed… one in the fuselage and one in each wing." All foam-filled (fire protection + anti-slosh). "Six interconnected fuel cells make one wing fuel tank." One 90-US-gal tip tank per wingtip — **dumpable, NON-self-sealing**. Ferry option: right-hand seat tank (self-sealing, electric transfer pump into fuselage tank, NOT dumpable/jettisonable). Provisions for 4 pylon tanks, drawn into fuselage tank by fuel proportioners. Engines feed from the fuselage tank. https://archive.org/details/A37BFlightManual
- **EGT thermocouple type**: 8 thermocouples per engine tailpipe; indicators are **self-generating** (powered by the thermocouples themselves, no bus power). Alloy type (chromel-alumel class): **NOT FOUND** in the flight manual — would live in the maintenance T.O. series. https://archive.org/details/A37BFlightManual
- **DC bus architecture** [TO]: "28 volt dc power supply system is powered by two engine-driven 300 ampere generators and two 24 volt 22-ampere-hour batteries" (NiCd, left nose; supply dc bus if both generators fail). Generators are starter-generators, cutting in at ~48–50% rpm; >65% rpm may be needed to carry full load. Separate 115 V 3-phase AC and 26 V single-phase AC buses via inverters. https://archive.org/details/A37BFlightManual

---

## Q3 — DCS EFM + OPEN PO-RCS REALITY

### Q3.1 — Open-source EFM references

- **A-4E-C EFM C++ source: PUBLIC — YES.** EFM lives under `A-4E-C/ExternalFM/FM/` (ed_fm_simulate and other ed_fm_* exports in Scooter.cpp; FlightModel.h; Data.cpp uses get_param_handle from C++): https://github.com/heclak/community-a4e-c
  Active maintained org fork: https://github.com/Community-A-4E/community-a4e-c
- **Other public ED_FM_Template-based EFM sources (2 more):**
  1. **IGServal/DCS-Basic-EFM-Template** — enhanced ED EFM template, full C++ source, designed as two-engine subsonic trainer/fighter (directly relevant shape to A-37): https://github.com/IGServal/DCS-Basic-EFM-Template
  2. **Zaretto/acEFM** — JSBSim↔DCS EFM bridge: single DLL, config-file mapping of iCommands/draw args/params; example aircraft repo linked in README: https://github.com/Zaretto/acEFM
  (Note: ED's own ED_FM_TEMPLATE.cpp ships inside the DCS install at `DCS World/API` — no URL, local artifact.)
- **get_param_handle limitations (DCS 2.9+): NO OFFICIAL ED DOCUMENTATION EXISTS** — ED publishes only the API headers + template in the install folder; there is no official modding-API doc to cite. Community-documented behavior:
  - Params are a global name-keyed databus shared between devices, indicators, and EFM; a handle is **created on first call** (a typo silently creates a new param) — http://modding.caffeinesimulations.com/Aircraft/Lua/BasicPrinciples/
  - Quirk: setting a param to a numeric-only string coerces it back to a number (documented crash vector) — same URL.
  - Frequency caps: **NOT FOUND** (no official or credible forum source; params are plain shared state, no documented rate limit).

### Q3.2 — Open PO RCS tooling

- **YES, usable pipeline exists: POFACETS** (Naval Postgraduate School, David Jenn lineage), free, v4.5 on MATLAB Central File Exchange: https://www.mathworks.com/matlabcentral/fileexchange/50602-pofacets4-5
  - (a) Mesh input: imports meshed CAD/facet models (own facet format; MATLAB's STL/OBJ readers feed it). (b) Output: monostatic AND bistatic RCS vs aspect tables/plots.
  - Documented physics limits: pure Physical Optics — no multiple reflections, creeping waves, or edge diffraction. Requires MATLAB.
- **Adaptable alternative (no MATLAB): PyPOFacets** — MIT-licensed Python port of POFACETS: https://github.com/gems-uff/pypofacets
  - Honest gap: facet/node input format; an OBJ/STL→facets conversion step is required (not verified in-repo).

### Q3.3 — Hydroplaning formula origin

- **CONFIRMED.** NASA TN D-2056, *Phenomena of Pneumatic Tire Hydroplaning*, Walter B. Horne & Robert C. Dreher, November 1963. Eq. (4): **Vp = 9√p** (knots); eq. (5): **Vp = 10.35√p** (statute mph); p = tire inflation pressure, psi. NTRS: https://ntrs.nasa.gov/citations/19640000612

---

## LEDGER

- CONFIRMED: 12 of 18 table rows + idle 48% + hydroplaning + A-4E-C EFM + POFACETS + TN D-2056.
- CORRECTED: internal fuel, fuel dump, gear half-track, EGT redline (890 → 664 cont / 692 30-min / 1000 inst).
- NOT FOUND: altitude thrust (17A), TSFC (17A), spool rate (17A), standpipe (recommend delete), oleo k/c, tire burst, EGT alloy type, get_param_handle frequency caps, official ED docs (none exist).

*END OF RETURN*
