# Roadmap

## Milestone 0 — Foundation

- [x] Pin an actively maintained Android Auto receiver.
- [x] Preserve upstream licence and history through a submodule.
- [x] Add read-only ADB profiling.
- [x] Add profile parsing, comparison and synthetic tests.
- [x] Add build and repository-guard automation.

## Milestone 1 — Confirm the target

- [ ] Capture a sanitized v333 profile.
- [ ] Record exact Hardware Version.
- [ ] Confirm Android API and ABI.
- [ ] Confirm display resolution/density.
- [ ] Confirm USB host and phone enumeration.
- [ ] Confirm hardware video decoder capabilities.

## Milestone 2 — Receiver baseline

- [ ] Build pinned Open Headunit in CI.
- [ ] Run on an Android 9 reference device.
- [ ] Test wired Android Auto on a bench IHU.
- [ ] Establish usable DPI and H.264 settings.
- [ ] Measure cold start and reconnect behaviour.

## Milestone 3 — Existing authorized access

- [ ] Confirm package install and launch using ordinary ADB.
- [ ] Confirm persistence across ACC restart.
- [ ] Confirm clean uninstall.
- [ ] Confirm no conflict with factory launcher or QDLink.

## Milestone 4 — Vehicle integration

- [ ] Navigation and media audio focus.
- [ ] Voice microphone uplink.
- [ ] Steering-wheel key mapping.
- [ ] Day/night signal.
- [ ] Reverse/360 camera foreground takeover.
- [ ] Factory warning and chime coexistence.

## Milestone 5 — v333 access research

- [ ] Build a sanitized package/component inventory.
- [ ] Identify official updater/engineering components.
- [ ] Compare public v300/v333 observations.
- [ ] Validate any write hypothesis on a recoverable bench unit.
- [ ] Publish only original code and reproducible evidence.

## Milestone 6 — CarPlay track

Deferred until a licence-clear and technically suitable receiver exists. Do not advertise no-dongle CarPlay support based on the Android Auto receiver.
