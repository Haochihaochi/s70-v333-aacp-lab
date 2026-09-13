# Integration knowledge map — read before SDD

This is a navigation/checklist for future development, not a new hardware finding. Scope and evidence below derive from the owner's 2026-09-13 instructions and the dated specification package. Consult actual sources before relying on a time-sensitive claim.

## Baseline and source of truth

- Owner: 2024 S70 Flagship, displayed v333, wired Android Auto sufficient initially, no developer access or spare matching IHU at the time of confirmation.
- [Requirements](../specs/REQUIREMENTS.md): canonical IDs, measurable targets and scope. Review proposed metrics against real baselines before treating them as achievable.
- [Project status](../../PROJECT_STATUS.md): implementation/evidence state. A script's existence is not proof it was exercised on a car.
- [Research and tools](../specs/RESEARCH.md): dated primary sources, receiver alternatives, OEM-model distinction, regional uncertainty and existing helper gaps.
- [Architecture](../specs/SYSTEM_ARCHITECTURE.md): ordinary-APK components, interface contracts, state model, audio/call ownership, factory priority and release flow.
- [Recovery](../specs/RECOVERY.md) and [validation](../specs/VALIDATION.md): independent restoration, lab levels, G1–G5 prerequisites and test catalog.

## Required integration inputs

| Area | Information to obtain before dependent code/qualification | Design/test consequence |
|---|---|---|
| Identity | Full software/build fingerprint, hardware/part and MCU revisions where exposed, API, ABI, security/boot state | Exact allowlist; never authorize on a v333 substring or newer S70 brochure |
| Installation access | Supported authorized access, package installation/removal, permission handling, authorization after reboot and USB-role changes | Desktop preflight/rollback design; unavailable access is a blocker |
| USB | Which factory port carries data, host/controller behavior, phone AOA enumeration, charging, attach/detach, management-link coexistence | Real-phone wired tests; no PC/dongle/developer server in normal runtime |
| Display/video | Physical and usable pixel dimensions, density/margins, codec capabilities/ABI, surface lifecycle, touch transform | H.264-first measured profile; test borders, latency, decode and camera takeover |
| Audio | Media/navigation/speech routing, mixer/DSP behavior, factory focus and warnings, volume restoration | No blanket volume/stream changes; physically verify chimes and prompts |
| Mic/calls | Factory mic access, capture source/permissions, gain/echo, native assistant coexistence, HFP/SCO and caller-UI ownership | Factory Bluetooth may carry calls during wired projection; phone mic is not a factory-mic pass |
| Factory priority | Real camera/reverse/360 behavior, overlays, warning paths, native Home and climate/vehicle UI | Callback/foreground assumptions must be measured; suppress watchdog focus reacquisition |
| Keys/themes | Actual steering key source, duplicates, press types, reserved driving keys, illumination signal | Preserve reserved keys; conservative theme when signal unavailable |
| Power | Boot vs accessory wake vs sleep, off-state current, thermal limits, watchdog behavior | No auto-start loops, wake locks or silent battery drain; qualified bench measurements |
| Recovery | Exact independent entry/tool/source, backups/digests, signing/rollback constraints, pairing/calibration, trained operator | App recovery and OS recovery are separate; rehearse before owner-vehicle install |
| Phone/service | Owner phone/OS/AA/app versions, region/language, account permission and internet behavior | DHU reference baseline plus real receiver tests; record tested combinations |
| Source/build | Pinned upstream, dependency/native-library and license inventory, app identity/signing, toolchain, artifact hashes | Use exact audited/tested release; debug APK and upstream beta labels are not production qualification |

The repository's current upstream pin and build settings live in [config/upstream.env](../../config/upstream.env). Reuse existing mechanisms only after source review. Profile collection can retain personal connectivity data; a raw dump is not automatically sanitized. The existing installer launches immediately and lacks the new evidence gates; its force option is not approved production behavior.

## AACP boundary

Android Auto and Apple CarPlay have distinct receivers, protocols, authentication/licensing, phone stacks and test requirements. Current development is **Android Auto first**. Before any CarPlay implementation, create separate requirements/product/technical/test designs proving a suitable receiver and distribution path for this hardware. No-dongle CarPlay must not be inferred from AutoKit downloads, Android Auto success or features on a newer S70. Wireless AA also requires an explicitly scoped follow-on design and current compatibility evidence.

## Never substitute these claims

| Available result | Does not prove |
|---|---|
| DHU works on PC | Our receiver APK runs, USB works on the S70, or recovery is possible |
| AVD/reference Android device works | Proprietary S70 mic/camera/MCU/USB drivers or boot behavior |
| APK built/installed | Complete navigation/voice/calls/factory coexistence |
| App uninstall succeeded | Recovery from Android boot failure or corrupted firmware |
| Backup exists and hashes match | Correct signing, rollback allowance, unit pairing or successful restoration |
| CI and SDD checks pass | G1–G5 or full vehicle qualification |

## Development safety and data handling

Use read-only profiling through authorized access; normal package operations only after the relevant gates. Preserve factory software and security enforcement. Do not invent or probe vendor server authorization, transfer X50 recipes, disable factory apps, flash partitions or issue driving-control traffic. Device installation requires concrete task authorization as well as the technical gates; this workflow itself supplies neither.

Raw logs, VINs, serials, network identifiers, conversations, keys and proprietary restoration material remain private. Record sanitized evidence and traceable private references where needed. Tests should use synthetic fixtures and controlled ordinary calls, never private production data as a shortcut.
