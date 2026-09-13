# Repository instructions — S70 v333 AACP

## Mandatory workflow

Use specification-driven development (SDD) for every implementation change: **requirements → product behavior → technical design → test cases → code → test evidence → completion review**. This includes fixes, tests, installers, build/CI changes, target profiles and receiver/submodule updates. Write/revise the affected specifications and test cases before editing implementation. For regressions, add a reproducing test first when practical.

Explicit user revisions to scope or workflow take precedence; document their impact. A terse request to fix something, urgency, or a missing mention of specs is not a waiver of SDD.

Read [SDD workflow](docs/development/SDD_WORKFLOW.md) and the [repository skill](.agents/skills/s70-v333-sdd/SKILL.md) before relevant work. The [integration knowledge map](docs/development/INTEGRATION_KNOWLEDGE.md) routes to maintained context; read only the sources needed for the task.

Before knowledge extraction into requirements, follow the source/provenance and change-control steps in the workflow. The canonical system requirements are [docs/specs/REQUIREMENTS.md](docs/specs/REQUIREMENTS.md). Do not create a competing lowercase/root `requirements.md` or overwrite earlier knowledge. Ordinary research/specification work may proceed before implementation readiness; unknown facts must remain unknown.

For code changes, create/update a change specification and JSON record under `docs/changes/`, record review readiness, and run `python tools/sdd_guard.py --record docs/changes/<ID>.json` before implementation. Self-review is valid for already-authorized reversible work; no extra owner-approval ritual is required. Material scope changes and unavailable mandatory evidence must be resolved, not invented.

## Non-negotiable project facts

- Owner target: **2024 Proton S70 Flagship, v333; wired Android Auto first**. No developer/ADB access and no matching spare IHU were available as of 2026-09-13. Verify current status before dependent work.
- AACP names the broader ambition. Apple CarPlay and wireless Android Auto are deferred. Android Auto receiver success proves neither CarPlay support nor an Apple receiver/license path.
- Exact hardware, full build, ABI, display, mic/call paths, factory priority and recovery remain unverified. Android 9/API 28 is a hypothesis until measured.
- Separate receiver, installation access, vehicle integration and independent recovery. Ordinary ADB requires authorization; a `v333` substring or a passing profile parser is not install readiness.
- Preserve factory launcher, cameras, alerts/chimes, climate/vehicle UI, voice, calls, keys and sleep behavior. No factory-package disabling, driving-control traffic, fabricated parked state, firmware writes or root-based workaround in the approved APK architecture.
- Bench qualification and independent recovery precede owner-vehicle installation. App safe mode/uninstall cannot repair an unbootable OS. DHU, AVD and reference tablets cannot establish full v333 hardware compatibility.
- Do not download/publish proprietary firmware, credentials, unique vehicle data or raw personal logs. Keep legal/private evidence private and publish sanitized summaries only.

## Tests and completion

Write meaningful tests for changed behavior, failure paths and recovery; map requirements to cases, expected outcomes, actual results and environment. Use unit, integration, device/bench and vehicle levels as required by the change. `NOT RUN`, `BLOCKED`, failed and simulated evidence are never physical PASS.

Run `python -m unittest discover -s tests -v`, `python tools/repo_guard.py`, and `python tools/sdd_guard.py`; perform Bash syntax and receiver/device checks when relevant. Update results, capture source fingerprints, and run `python tools/sdd_guard.py --complete --record docs/changes/<ID>.json` before calling a code change complete. Never weaken the guard or tests just to obtain a pass.

Say what is complete: documentation, tooling, software prototype, bench-qualified integration, or owner-vehicle-qualified system. “System complete” requires every mandatory system requirement and G1–G5 gate with exact artifact/hardware/phone evidence, independent recovery rehearsal and final parked-vehicle checks. A completed tooling record or green CI is not system completion.

## Code review rules

Flag code without a ready SDD record; changed behavior without prewritten tests; missing or stale evidence; unsupported v333/CarPlay claims; dependencies on unavailable access; factory priority regressions; and any statement of system completion based only on software tests. The guard verifies record structure and source consistency, not truth of measurements, authorship chronology, or operational safety. Review those explicitly.
