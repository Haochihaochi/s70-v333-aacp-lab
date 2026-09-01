# Proton S70 v333 AACP Lab

A reproducible, safety-first foundation for researching **no-dongle Android Auto** on the Proton S70 v333 infotainment unit.

> **Current scope:** Android Auto receiver integration first. Native Apple CarPlay is not implemented because no suitable open-source, licence-clear receiver is available for this Android 9 target.

## Project status

| Track | Status |
|---|---|
| Open-source Android Auto receiver | Pinned to Open Headunit upstream |
| Repeatable local/CI build | Scaffolded |
| Read-only v333 device profiling | Implemented |
| ADB install path | Implemented for an already-authorized device only |
| Public v333 privilege/sideload entry point | **Not discovered** |
| Audio, microphone and USB-role validation | Pending real hardware profile |
| Steering-wheel controls | Pending real hardware profile |
| Recovery image / rollback | Not included; proprietary firmware must not be committed |
| Apple CarPlay without a dongle | Out of scope for v0.1 |

## Why this foundation

There is no substantive, licence-clear public repository implementing an S70 v333 sideload route. The small public `username688/s70unlock` repository contains only HTML links that attempt to open Android Settings and download third-party APKs; it has no actual installation mechanism and no licence. It is documented under `docs/UPSTREAMS.md` but is not copied.

The receiver layer is therefore based on [Open Headunit](https://github.com/andreknieriem/open-headunit), pinned as a Git submodule. The S70-specific layer in this repository focuses on:

1. Identifying the exact v333 hardware/software environment.
2. Building a reproducible receiver APK.
3. Testing only through an already-authorized ADB or bench environment.
4. Recording audio, microphone, USB-host, display and key-event compatibility.
5. Keeping installation-access research separate from the receiver.

## Repository layout

```text
.
├── third_party/open-headunit/     # AGPL-3.0 upstream submodule
├── config/                        # pinned upstream and target template
├── scripts/                       # build, profile, install and smoke-test helpers
├── tools/                         # profile parser, diff and repository guard
├── tests/                         # synthetic tests; no vehicle dumps
├── docs/                          # architecture, safety, research plan and roadmap
└── .github/                       # CI and issue templates
```

## Quick start

### 1. Clone with the receiver submodule

```bash
git clone --recurse-submodules https://github.com/haochihaochi/s70-v333-aacp-lab.git
cd s70-v333-aacp-lab
./scripts/bootstrap.sh
```

When starting from the supplied Git bundle instead:

```bash
git clone s70-v333-aacp-lab.bundle s70-v333-aacp-lab
cd s70-v333-aacp-lab
git submodule update --init --recursive
```

### 2. Run foundation tests

```bash
make test
make guard
```

### 3. Build Open Headunit

Requirements:

- JDK 17
- Android SDK platform 36
- Android NDK `29.0.14206865`
- CMake `3.22.1`

```bash
make build
```

The APK and checksum are copied into `dist/`.

### 4. Collect a read-only device profile

This requires ADB to have already been enabled and authorized by the IHU. The script does not exploit, root, flash or modify the unit.

```bash
ADB_SERIAL=<optional-serial> make profile
```

Then generate the report:

```bash
make verify PROFILE=artifacts/device-profile-YYYYMMDDTHHMMSSZ
```

### 5. Install only through an existing authorized ADB path

```bash
./scripts/install-open-headunit-adb.sh \
  --apk dist/<built-apk>.apk \
  --acknowledge-parked
```

The installer refuses a target that does not expose v333 evidence unless `--force-unverified` is supplied. It uses ordinary `adb install -r`; it contains no privilege escalation.

## Safety boundaries

- Work on a bench unit where possible.
- Do not test while driving.
- Do not flash an unknown `boot`, `system`, `vendor`, `super` or recovery image.
- Do not publish firmware, keys, certificates, VINs, serial numbers, MAC addresses or private log data.
- Do not run the X50 ATLAS/GKUI USB script on an S70.
- Keep CAN injection and safety-critical vehicle-control experiments out of this project.

See [`docs/SAFETY.md`](docs/SAFETY.md) and [`SECURITY.md`](SECURITY.md).

## Licence

The original foundation scripts and documentation are Apache-2.0. The Open Headunit submodule remains licensed under AGPL-3.0 and retains its own copyright and licence. Any modifications to that upstream project must follow its AGPL terms.

This project is independent community research and is not affiliated with Proton, ACO Tech, Geely, Google, Apple or the Open Headunit maintainers.
