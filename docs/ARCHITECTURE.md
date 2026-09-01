# Architecture

## Separation of concerns

The project deliberately separates the **receiver** from the **installation/access mechanism**.

```text
Android phone
    │ USB host / Wi-Fi transport
    ▼
Open Headunit receiver (ordinary Android APK)
    │ Android audio, display, microphone and input APIs
    ▼
S70 v333 Android 9 IHU
```

The missing public component is not Android Auto protocol handling; Open Headunit already provides that. The unresolved component is obtaining a repeatable, recoverable and lawful installation path on a locked v333 production IHU.

## Layer 1 — Device identity

Required observations:

- Full Software Version and Hardware Version from About IHU.
- Android API level, ABI and build type.
- Display resolution/density and codec capabilities.
- USB host/role behaviour.
- Audio output/input devices and audio-focus behaviour.
- Input events from steering-wheel controls.
- Verified Boot, SELinux and debuggable state.

Use `scripts/collect-ihu-profile.sh` only after ADB is already authorized.

## Layer 2 — Receiver

Open Headunit is pinned as an upstream submodule. Initial validation order:

1. Build the upstream GitHub debug flavour unchanged.
2. Validate it on an Android 9 reference device.
3. Validate wired Android Auto on a bench S70 IHU.
4. Record display scaling and H.264/H.265 behaviour.
5. Record navigation/media audio routing and microphone uplink.
6. Record reconnect behaviour after ACC cycles.
7. Add S70-specific patches only after a reproducible failure is documented.

## Layer 3 — Access research

This repository currently supports only an existing authorized ADB path. Future access research should proceed in this order:

1. Inventory exported activities, services, receivers and content providers.
2. Observe official update/USB flows without modifying them.
3. Compare legally obtained package manifests between versions offline.
4. Test any hypothesis on a recoverable bench unit.
5. Document rollback before attempting a write.

Do not impersonate vendor servers, publish credentials, bypass payment services or probe production infrastructure.

## Layer 4 — Vehicle integration

The receiver must not interfere with reverse camera, 360 camera, parking alerts, climate overlays, warning chimes or other integrated functions. Android Auto should yield audio focus and foreground visibility whenever a safety-relevant factory UI takes priority.

## Layer 5 — Recovery

No write-path milestone is complete until all of the following exist:

- Exact hardware/software match.
- Verified original backup.
- Checksums.
- Bench-tested restoration steps.
- Power-loss test plan.
- Confirmation that factory camera and vehicle UI recover correctly.
