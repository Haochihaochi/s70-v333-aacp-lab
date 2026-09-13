# S70 v333 Android Auto — design package

Version: 0.1 · Research date: 13 September 2026 · Status: draft for requirements review

Future knowledge extraction and implementation follow the repository's [SDD workflow](../development/SDD_WORKFLOW.md) and [integration knowledge map](../development/INTEGRATION_KNOWLEDGE.md). Requirements, product behavior, technical design and test cases precede code; evidence is required before completion claims.

## Intended outcome

Add **wired Android Auto to the existing 2024 Proton S70 Flagship v333 infotainment unit**, using a phone and USB data cable, with factory functions preserved, a demonstrated recovery route, and testing before installation in the owner's vehicle.

The owner confirmed that wired operation is sufficient initially, developer access is unavailable, and there is no spare matching head unit. The exact hardware revision and phone are still unknown.

**Feasibility is conditional.** A receiver application is available as a starting point; a repeatable v333 installation route, vehicle integration, and recovery have not been established. Software simulation cannot establish all three. The recommended architecture is an ordinary application alongside the factory system, supported by a desktop commissioning tool and staged test laboratory.

## Read in this order

1. [Requirements specification](REQUIREMENTS.md): scope, numbered requirements, acceptance targets, dependencies, and release gates.
2. [System architecture](SYSTEM_ARCHITECTURE.md): components, trust boundaries, interfaces, runtime states, installation sequence, and design decisions.
3. [Recovery design](RECOVERY.md): what each fallback can recover, prerequisites, failure scenarios, and recovery evidence.
4. [Validation and laboratory plan](VALIDATION.md): PC tests, reference hardware, matching bench unit, final vehicle checks, and traceable test cases.
5. [Research and tool assessment](RESEARCH.md): dated findings, alternatives, primary sources, and gaps in the existing repository.

These documents define the proposed system; they do not certify compatibility or provide a ready vehicle installer. All performance numbers are proposed engineering acceptance targets, not measured results or OEM specifications.

## Immediate decision

Proceed with requirements refinement and software laboratory work. Obtain an official answer on retrofit/access/recovery eligibility and investigate borrowing, renting, or commissioning tests on a matching v333 bench unit. Do not treat a successful emulator demonstration as permission to install in the owner's car.

The subsequent **product specification** should define the owner and technician experience against these requirement IDs. The **technical specification** should then bind the design to measured hardware, actual APIs, build identity, package identity, and rehearsed recovery steps. Unresolved prerequisites remain explicit blockers in both documents.
