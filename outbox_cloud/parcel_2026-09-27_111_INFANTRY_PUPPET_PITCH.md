# PARCEL 111 — PROJECT PITCH: "PUPPET SWAP" — Directional Death Poses for DCS Infantry
**From:** Marco (cloud shore) | **To:** Director & Buffy (rig shore) | **Date:** 2026-09-27
**Status:** PROPOSAL — awaiting Director gavel + one rig bench test
**Classification:** House cargo (postal_lane public channel)

---

## 0. The one-paragraph pitch (elevator version)

Stock DCS infantry die like 2003-era mannequins: one canned animation, zero variety, zero relationship to where the fire came from. We can fix that **without touching the engine's animation system at all**. On the death event, we intercept: despawn the stock corpse, spawn a *pre-baked frozen ragdoll pose* — chosen by impact direction — as a custom static object at the exact spot and heading. Directional, varied, situation-appropriate death poses with zero physics runtime and zero reverse-engineering of ED's undocumented animation state machine. The hard boss of the infantry-mod world (L3, where Massun92 died in 2022) is routed around entirely. Cost: a pose library built in Blender (days), one mission script (mapped territory), and one bench evening to prove the corpse-despawn link holds. Payoff: every SOULSMITH-enabled mission gets infantry deaths that *read* — and the same pose library ports straight into VANDAL-Lite, where it becomes the fallback layer under a real physics ragdoll.

---

## 1. Problem statement

DCS infantry death behavior, unflavored:

- **Canned death animations only. No ragdoll.** ED's own "Ragdoll physics for infantry" thread (2020) sits in the Wishlist graveyard, unimplemented. There is no physics death state to bind to.
- **One animation per soldier type.** Every death looks identical regardless of weapon, direction, or situation.
- **The modding community's failure history is charted.** Massun92 (Jan 2022, forum topic 291799) built custom models + animations, exported actions to argument slots, and stalled at the lua binding layer — his units bound to the old `generic_human` / `GT_t.HUMAN` / `wsType_genericInfantry` template, not the newer soldier type. The Animated Pilot Mod (2019, topic 196334) proved custom animated humans *can* work — and documented the feet-origin gotcha. Nobody has shipped an infantry animation-replacement mod. Texture packs exist; animation fixes don't.

The conventional route (replace the animation state machine) is HARD because the state-machine binding layer (L3) is undocumented. That's the boss. **This proposal does not fight that boss. It walks around it.**

## 2. The idea: Puppet Swap

Three moves, all in mission-scripting territory we already own:

1. **Intercept the death.** `S_EVENT_DEAD` / `S_EVENT_KILL` fires with victim position, victim heading, and killer/weapon object. Documented API, decades of prior art (MOOSE, MIST, every CTLD script ever).
2. **Kill the stock corpse.** Either remove the dead unit post-event, or — the promising route — catch the terminal *hit* event and `unit:destroy()` *before* the engine generates the corpse, then spawn our own. (See §5 — this is the one unproven link.)
3. **Spawn the puppet.** `coalition.addStaticObject()` with a custom `shape_name` — a frozen EDM mesh of a soldier in a death pose, chosen from a **pose library** keyed to impact direction:
   - fire from front → backward fall pose
   - fire from behind → forward collapse
   - side hit → lateral crumple
   - explosion/frag → thrown sprawl
   - crouch/kneel death → folded pose
   Each pose is a separate small EDM static. The script computes impact bearing from killer→victim geometry, picks the pose, spawns at victim position with correct heading. Optional: randomize among 2–3 poses per direction class so repeat deaths don't clone.

**Result:** deaths that *read*. A grunt cut down by strafing fire falls across the road. A squad caught by a frag collapses in a heap. No physics — "ragdoll's greatest hits, pre-baked." At DCS engagement distances (infantry are tiny on screen), the directional + variety effect captures most of the perceived realism of true ragdoll.

## 3. Why this is the smart route (architecture argument)

The infantry-mod difficulty ladder, restated:

| Layer | Conventional route | Puppet Swap route |
|---|---|---|
| L1 — model + Mixamo pose → EDM export | MEDIUM (documented: official EagleDynamics/Blender-EDM-Exporter, SkinNode workflow explicitly for "infantry, pilots, driver or cows"; constraints known: ≤4 bone influences/vertex, linear interp, quaternion WXYZ, 90° keyframes, `Armature` modifier name, bounding box required) | **SAME — and easier**: no action/argument-slot export at all. Just a static mesh in a pose. The exporter's simplest use case. |
| L2 — GT-lua registration | MEDIUM-HARD but mapped | **Trivial**: custom *statics* are the best-documented custom-content path in DCS. Modders ship custom hangars, buildings, crowds, cargo daily. No GT animation table, no arg-map. |
| L3 — animation state-machine binding | **HARD / undocumented — the Massun92 graveyard** | **ELIMINATED.** A static has no state machine. Nothing to reverse-engineer. |

The boss doesn't get fought. He gets walked around. That's the whole pitch in one sentence.

## 4. The pose library (the build)

- **Source:** Mixamo death animations (royalty-free for project use; Arma mods ship Mixamo-derived anims publicly — license precedent established).
- **Method:** Take the Director's M92 soldier model (already exists, already proven in-engine by Massun92's own work), rig it, pose it from Mixamo death clips, freeze each pose, export each as a standalone EDM static via the official Blender-EDM-Exporter (Blender 4.x LTS).
- **Library v1 target:** 6–10 poses covering 4 direction classes + explosion + kneeling. Each EDM expected small (single skinned mesh, no textures beyond one skin set — low single-digit KB to tens of KB).
- **Effort estimate:** days, not weeks. This is L1 work — the *documented* layer. Every exporter gotcha is already in our research receipts.
- **Bonus:** the same Mixamo-sourced library exports to GLB in one step for VANDAL-Lite (§8).

## 5. The weak link — corpse removal (unflavored truth)

This is where the receipts turn ugly, and I won't sand it off:

- **Post-death removal is unreliable since ~1.2.14.** The MOOSE CLEANUP class author called his own corpse-removal workaround "marginally successful" and "a crappy solution." Timers miss under server load; dead units stop tracking cleanly.
- **2022 regression:** ground units taking terminal (burning) damage get substituted to a static object, which can swallow `S_EVENT_DEAD` entirely — a decade of community scripts broke on it. Mitigation: listen to `S_EVENT_KILL` as well; treat the event stream as best-effort.
- **Failure mode if removal fails: two bodies.** Stock corpse + our puppet. That is *worse* than stock. This is the project's single point of failure.
- **The promising counter:** intercept at the *hit* event — when damage goes terminal, `unit:destroy()` before the engine generates the corpse, then spawn the puppet. Forum evidence says pre-emptive destroy can skip corpse generation entirely (the trick CLEANUP uses for aircraft wrecks). Racy, but plausible. **Nobody has proven it on current-build infantry. That is a bench test, not a research question.**

## 6. The bench test — one rig evening, definitive GO/NO-GO

Spawn 20 infantry, script-kill them from varied angles, instrument everything, measure:

| # | Question | Pass criterion |
|---|---|---|
| T1 | Does DEAD/KILL fire reliably for infantry on current build? | events ≥ 95% of scripted kills |
| T2 | Can the stock corpse be removed post-death? | residual bodies ≈ 0 |
| T3 | Does pre-emptive `destroy()` at terminal hit skip corpse generation? | no stock corpse ever renders |
| T4 | Does the swap pop visibly at engagement range? | eyeball pass (test with a placeholder static first) |

**Decision matrix:**
- T3 PASS → **GO.** Full concept works; build pose library + script.
- T3 FAIL, T2 PASS → **conditional GO.** Post-death cleanup hack; accept occasional two-body glitches or a corpse-fade timer.
- T2 & T3 FAIL → **NO-GO in DCS.** Idea parks to VANDAL-Lite (§8), where it becomes a feature instead of a fight.

T4 can run *before any asset work* using a stock shape as placeholder puppet — the whole test needs zero new art.

## 7. Pros and cons, honestly

**Pros:**
1. Routes around the documented graveyard (L3). Uses only documented APIs and the documented content path (custom statics).
2. Cheap: pose library = days of L1 Blender work; script = one evening; bench test = one evening. Total art risk near zero (statics are the simplest export).
3. Directional + varied deaths = most of ragdoll's *perceived* value at DCS viewing distances, for none of its cost.
4. Mission-script layer = SOULSMITH's home turf. The same event hooks feed the cognitive layer (a death event is a morale/fatigue input to the GOAP side). Puppet Swap and SOULSMITH share plumbing.
5. **Asset portability:** pose library re-exports to GLB for VANDAL-Lite in one step. Nothing is throwaway.
6. Reversible: it's a mission script + optional asset pack. No engine files touched. Uninstall = delete.
7. MP-safe in principle: statics replicate; event handling is standard server-side scripting. (Needs the usual MP caveats verified on the bench.)

**Cons / risks:**
1. **Corpse-despawn link is unproven** (§5). Single point of failure; bench test gates everything.
2. **Not physics.** A frozen pose can't react to terrain (no falling down stairs, no sliding down slopes). Cliff-edge deaths will look wrong — mitigate with a "reclined" pose class or accept the limit.
3. **Statics don't animate** — no death *transition*, just a pop. Mitigation: spawn slightly delayed / behind smoke / during the explosion flash; at range the pop is nearly invisible.
4. **Event-stream flakiness** (the 2022 static-substitution regression) means edge-case deaths may double-render or miss. Accept a small glitch budget.
5. **Tacview irrelevant:** puppet poses do nothing for ACMI replay (Tacview doesn't render anims) — this is a *visual* mod for the live 3D world. Zero tactical-data value. If the mission goal is Tacview-only, skip this entirely.
6. **Despawn/respawn churn:** each death adds a static; long missions accumulate puppets. Need a cleanup sweeper (despawn puppets after N minutes or on distance) — trivial but must be in v1, not bolted on.
7. **EDM exporter constraints** apply (≤4 bone influences, linear interp, etc.) — known, documented, in our receipts. Not a risk, just homework.

## 8. The strategic kicker — VANDAL-Lite

Everything above is the *fallback version* of the real dream. In VANDAL-Lite (own engine):
- No EDM, no GT-lua, no state machine: Mixamo → GLB, one step.
- **True ragdoll is buildable** — even a cheap verlet-joint ragdoll is a known quantity in our own runtime.
- The DCS pose library becomes the fallback layer when physics ragdoll is too expensive (mass casualties, perf budget), or the calibration reference for tuning the real ragdoll.
- Every hour of DCS Puppet Swap work produces assets and geometry logic that **port forward**. Nothing stranded.

## 9. What I'm asking for

1. **Director gavel** on the bench test (T1–T4). One rig evening, zero new art needed, definitive answer.
2. If gavel passes: I write the **bench-test script spec** for Buffy (test harness, instrumentation, pass/fail criteria, receipt format — house standard, JSON receipts, fail-closed).
3. Pose library build (Blender/Mixamo/EDM) starts **only after** T3 verdict. No art before the gate.
4. Parked pending: the older standing offers (v1 how-to card for the conventional route; newer-soldier arg-map archaeology). Puppet Swap, if it passes, supersedes both for DCS purposes.

---

*House receipts backing this pitch: DCS infantry research debrief (2026-09-27, this conversation); Massun92 thread 291799; Animated Pilot Mod topic 196334; ED Blender-EDM-Exporter GitHub (SkinNode workflow, Aug 2025 NLA support); MOOSE CLEANUP documentation + forum 96153 (corpse removal history); forum 295922 (2022 static-substitution DEAD-event regression); hoggit wiki: coalition.addStaticObject, S_EVENT_DEAD/KILL.*

**— Marco, cloud shore. Unflavored, as ordered.**
