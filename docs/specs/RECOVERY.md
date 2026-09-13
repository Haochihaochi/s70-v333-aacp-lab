# Recovery and installation failure design

Document: S70-AA-REC · Version: 0.1 · Date: 2026-09-13 · Status: proposed, not rehearsed

## 1. Recovery promise and present limitation

The proposed product shall recover from application-level failures through return to factory UI, disabling projection, and tested app removal/restoration. Recovery from an unbootable IHU requires a separately proven service or hardware recovery route. **No such route has been established for the owner's unit.**

An installed app, a second watchdog process, an APK backup, and a PC emulator snapshot cannot guarantee recovery when the IHU OS is unbootable. The owner's lack of developer access also means ordinary ADB uninstall cannot currently be offered as an available fallback. See [ADB authorization and package management](https://developer.android.com/tools/adb).

## 2. Recovery layers

| Layer | Trigger | Proposed response | What must still work | Qualification evidence |
|---|---|---|---|---|
| R0 — Reject before change | Unknown identity, unverified artifact, missing access/recovery, inadequate power/storage | Stop with a precise reason; no write | Commissioning PC | Negative preflight tests and unchanged package state |
| R1 — Return to factory | Projection disconnects, decode fails, app exits | End projection, relinquish app resources, retain factory Home | Android and factory UI | Tests during all projection states; independent Home route |
| R2 — App safe mode | Repeated start failure, profile mismatch, failed migration | Persistently suppress all app auto-start paths; permit diagnostics/manual diagnosis | App storage and enough Android to honor the policy | Failure/reboot sequences; latch remains set across entry points |
| R3 — App remove/restore | UI freeze, broken app update, corrupt preferences | Technician stops/disables/removes own package through tested access; restore known compatible build/config if requested | Authorized package manager access or verified factory app-management UI | Receiver killed/frozen, PC disconnected/reconnected, signing/version mismatch rehearsals |
| R4 — OS/service restoration | Android does not boot; settings/ADB unavailable | Use verified exact-target service restoration or qualified hardware repair/replacement path | Recovery path independent of ordinary Android | Matching-unit rehearsal, correct material, calibration/pairing restoration, factory acceptance |

R2 is not Android Safe Mode. R3 is not a firmware rollback. R4 is not implemented by the receiver or current repository scripts.

## 3. Pre-install recovery dossier

Before G3 bench qualification and certainly before owner-vehicle commissioning, assemble a privately held dossier containing:

| Evidence | Required contents |
|---|---|
| Target identity | Full hardware/part revision, full software/build identity, API/ABI, relevant MCU/peripheral revisions if exposed, baseline record |
| Allowed mutation | Own package ID, signature, version, permissions, app settings, exact intended operations; explicit before/after comparison |
| Factory baseline | Launcher/home selection, factory package states, cameras, audio, keys, calls, climate/vehicle UI, connectivity, sleep and startup behavior |
| Access | Exact supported installation/removal method, operator permissions, authorization persistence across reboot and USB-role changes |
| App recovery kit | Exact tested APK/digest/signature, compatible prior build, versioned configuration export, installer/removal version, local instructions |
| OS recovery material | Verified original backup or authorized service restoration source appropriate to this unit; integrity, version compatibility, ownership/provenance, required tools |
| Restoration dependencies | Signing/anti-rollback constraints, partition layout if relevant, encryption, unit-specific data, calibration, vehicle pairing, MCU compatibility, service activation dependencies |
| Recovery rehearsal | Same hardware and applicable firmware, induced failure class, independent entry method, elapsed time, before/after checks, technician sign-off |
| Operational readiness | Stable power and hardware-specific procedure, trained operator, service availability, private backup location, agreed escalation path |

A service provider that will merely “try reflashing it” does not satisfy independent recovery. Confirm what happens when normal Android and ADB are unavailable, whether correct restoration files and access are actually available, and how the result is verified.

The design does not prescribe a voltage, pinout, debug pad, firmware image, or flashing tool without exact hardware evidence. Generic Android tools such as fastboot, adb sideload, or a custom recovery are not assumed to exist on the IHU.

## 4. Failure handling matrix

| Failure | Detection | Response | Success criterion / stop condition |
|---|---|---|---|
| Target mismatch | Identity/profile comparison | R0 | No package operation starts |
| APK corrupted, wrong signer, unsupported ABI/API | Manifest and signature inspection | R0 | No install; exact failed field shown |
| Package installation rejected | Installer result plus actual package state | Preserve pre-state; inspect before retry | Stock UI and pre-existing app state intact; no auto-launch |
| PC cable/power lost during package operation | Journal lacks confirmed completion | Reconnect through tested access; query actual state | Resume or remove only after reconciliation; no blind repeat |
| App first launch crashes | Process result/log, incomplete start marker | R1/R2, then R3 if needed | Factory Home usable; auto-start remains off |
| Receiver freezes or retains mic/audio | Health/lifecycle observation, physical audio check | Stop own session/process through verified route | Resource release and factory calls/voice restored; otherwise R4 escalation |
| Camera hidden or warning lost | Independent observation against stock | End trial immediately; R3 | Factory function restored and complete baseline passed before vehicle use |
| Bad settings | Validation/schema failure | Load last valid app configuration or reset own preferences | No factory-setting change; recovery remains accessible |
| New app version broken | Post-install checks | Restore previous compatible code/config through rehearsed R3 | Signature/version/data constraints handled without deleting unrelated data |
| Repeated auto-start after wake | Persistent attempt counter | R2 must suppress every automatic entry path | Subsequent wake stays factory-only until deliberate re-enable |
| ADB authorization lost | Access check fails | Try only a documented independent factory/service path | No credential guessing or assumed reconnection; stop writes |
| Android boot loop or black screen | No healthy Android, failed normal recovery reachability | R4 | Independent service restoration succeeds; no app-level promise |
| OEM update changes behavior | Build/profile change | Disable automatic projection and requalify | Factory update remains intact; no automatic downgrade |
| Phone update breaks projection | Known-good IHU with changed phone stack fails | Factory fallback; mark pair unsupported; reproduce in lab | No obsolete phone-version requirement as permanent fix |

## 5. App update rollback design

Maintain two logical release records outside the IHU: the current qualified build and a candidate build. This is an application release strategy, **not A/B firmware**. Android's A/B update mechanism depends on a compatible bootloader and system layout; this project must not assume or add it. See [AOSP A/B updates](https://source.android.com/docs/core/ota/ab).

For each candidate, verify signature continuity, app ID, version policy, config schema, and permissions. Retain a configuration export that the prior build can read. Prefer additive/backward-compatible data changes; do not migrate the only copy irreversibly.

On failure, use a bench-proven path: remove the candidate and reinstall a compatible previous artifact with explicit loss/restoration of only project app data, or install a prepared recovery build with a permissible forward version. An older APK is not guaranteed to install over a newer one. Never use a signature mismatch as a reason to delete a factory or unrelated package.

For the very first installation, the fallback is removal of the added package and verification of stock behavior; there is no previous receiver to restore. App removal does not prove OS integrity or reverse every possible peripheral-driver fault, hence the separate R4 prerequisite.

## 6. Why firmware backups need more than checksums

Verified Boot checks trusted software and can impose rollback protection. An older image, a dump from another unit, or an unsigned modified partition may be rejected or fail to restore unit-specific state. The relevant constraints must be established for the actual IHU; their presence or absence is not known. See [AOSP Verified Boot](https://source.android.com/docs/security/features/verifiedboot).

Required success is a working restored system with original vehicle integration, not just a completed file transfer or a matching hash. Keep proprietary restoration material and unique vehicle data private. Do not use community debug firmware or another Proton model's installer as a presumed recovery asset.

## 7. Recovery rehearsal plan

Perform destructive/interruption rehearsals only on a recoverable matching bench setup with a qualified operator. Never make the owner's car the first power-loss or boot-failure experiment.

1. Record stock baseline and verify independent recovery before installing the candidate.
2. Exercise app-level faults: crash, freeze, denied mic/USB permission, bad config, conflicting update, and disconnect during package transfer/commit.
3. Verify latch behavior through manual launch, USB attach, boot/wake, and any registered automation entry.
4. Confirm removal with the receiver unresponsive and with the primary commissioning connection interrupted.
5. Rehearse the independent OS/service restoration procedure for its documented supported failure class; do not deliberately corrupt boot partitions to create a test unnecessarily.
6. Re-run camera, alerts, climate/vehicle UI, calls, voice, connectivity, startup, and power baselines after recovery.

No recovery layer is considered complete without an observed result and evidence reference. Any need for unverified proprietary access, missing pairing data, unavailable tools, or destructive reset with unknown consequences is a failed gate, not a footnote.

## 8. Go/no-go rule for the owner's present situation

With no developer access, no spare unit, and no verified R4 route, vehicle installation is **NO-GO today**. Requirements, architecture, host simulation, phone baseline, and reference-device work can proceed. Borrowing/renting a matching unit or using a qualified lab can satisfy the pre-install test requirement; software alone cannot supply the missing physical recovery path.
