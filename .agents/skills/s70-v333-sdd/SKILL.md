---
name: s70-v333-sdd
description: Develop or review this repository's Proton S70 v333 Android Auto and future CarPlay integration using specification-driven development, sourced requirements, test-first planning, and evidence-based completion. Use for knowledge extraction, receiver/access/recovery changes, integration tooling, and readiness reviews in this repo.
---

# S70 v333 specification-driven development

Apply the repo's [AGENTS.md](../../../AGENTS.md) and [SDD workflow](../../../docs/development/SDD_WORKFLOW.md). Resolve these links from this skill folder. This skill supports the owner's scope; it does not authorize vehicle writes, external messages, proprietary downloads, or scope expansion.

Explicit user changes to scope/workflow remain authoritative; record them and update affected specs. Do not infer a process waiver from a brief request to fix code.

## Choose the current stage

- **Knowledge extraction / requirements:** read the workflow's knowledge-extraction section and [integration knowledge map](../../../docs/development/INTEGRATION_KNOWLEDGE.md). Capture source, date, exact target/version, observation versus inference, confidence and unresolved contradictions. Merge into the existing canonical requirements with stable IDs and acceptance criteria. Do not begin implementation just because source material was found.
- **Product / technical design:** connect requirements to owner/technician behavior, exact interfaces, failure states, factory priority, permissions, recovery, and tests. For small tooling changes, one change document may contain all three specification layers. For a vehicle feature, use concrete feature product/technical specs; a generic architecture is not implementation readiness.
- **Code / fixes:** prepare a change record, review readiness and write test cases first. Add executable regression/unit tests before implementation where practical, observe the expected failure, then implement only the specified behavior. Keep unknown hardware work blocked while independent host work continues.
- **Completion / review:** run applicable tests and both guards, record environment and actual outcomes, bind evidence to source fingerprints, and use `sdd_guard.py --complete --record ...`. Qualify completion by scope; apply the system gates separately.

## Domain invariants

The current baseline is 2024 S70 Flagship v333, wired Android Auto without a dongle. The owner reported no developer access or matching bench IHU. Read current project status rather than assuming these prerequisites have since appeared. CarPlay and wireless remain deferred until explicitly scoped with a suitable receiver/protocol/license/access/test plan; an Android Auto implementation supplies no CarPlay proof.

Keep four independent questions visible: can the receiver run, can it be installed, can it coexist with factory functions, and can the unit be recovered? Use ordinary APK architecture; preserve cameras, warnings, controls and factory Home. Do not invent vendor APIs, privileged permissions, pinouts, firmware compatibility or recovery commands. Recheck time-sensitive upstream information using primary sources when it affects a decision.

DHU validates the phone against a separate desktop receiver. AVD validates Android software behavior. Reference hardware validates that hardware. Matching v333 bench evidence and independent recovery are needed before owner-vehicle installation, followed by final parked checks. Never relabel simulation as real vehicle evidence.

## Practical outputs

Use the [change-spec template](../../../docs/development/templates/CHANGE_SPEC.md) and [record template](../../../docs/development/templates/change-record.json). Keep substantive technical information in the specification package and change documents rather than duplicating it inside this skill.

Report requirement/test IDs, files changed, commands actually run, pass/fail/blocked outcomes, and the next unresolved gate. “The guard passes” means the selected change has structurally consistent SDD evidence, not that Android Auto/CarPlay is safe or fully supported on the owner's car.
