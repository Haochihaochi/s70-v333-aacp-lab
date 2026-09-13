# Project status — foundation v0.1.0

Created: 2026-09-01

## Requirements and architecture update — 2026-09-13

- Added [mandatory repository SDD guidance](AGENTS.md), a [repo-local integration skill](.agents/skills/s70-v333-sdd/SKILL.md), and a [tested change/completion guard](tools/sdd_guard.py). The local pre-commit hook is enabled; checked-in CI/Makefile integration is ready for publication. The [tooling evidence](docs/development/evidence/SDD-0001.md) is scoped to governance and does not qualify the vehicle system.

- Owner confirmed: 2024 S70 Flagship, v333; wired is sufficient initially; no developer access or matching spare head unit.
- Added a [requirements and architecture package](docs/specs/README.md), including staged validation, independent recovery prerequisites, primary-source research, and current helper gaps.
- This is design work only. No receiver build, v333 lab qualification, recovery rehearsal, or vehicle installation was performed in this update.
- Vehicle deployment is not ready: supported access, exact hardware profile, matching bench access, and independent recovery are unresolved. Software/reference-lab work can proceed while those dependencies are investigated.
- The sections below record the original foundation assessment; new scope and release decisions use the specification package.

## Confirmed

- An actively maintained Android Auto receiver can be used as the receiver layer.
- Public S70-specific repositories do not currently provide a complete, licence-clear v333 install path.
- The project can safely progress through build reproducibility and read-only device profiling without claiming a v333 unlock.

## Not yet confirmed

- Exact v333 Android property carrying the visible Software Version.
- Exact display resolution/density and hardware codec set for this user's IHU revision.
- Whether ADB is locally accessible, transient, server-enabled or physically exposed.
- Persistent ordinary APK installation on the user's production v333 unit.
- Audio/mic/key integration.
- Any no-dongle Apple CarPlay implementation.
