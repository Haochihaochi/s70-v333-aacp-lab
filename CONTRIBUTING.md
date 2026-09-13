# Contributing

Contributions should be reproducible, licence-clear and safe to test on a bench unit.

## Specification-driven development first

Follow [AGENTS.md](AGENTS.md) and the [SDD workflow](docs/development/SDD_WORKFLOW.md). Before code, write/revise requirements, product behavior, technical design and meaningful test cases, then create a reviewed `ready` record in `docs/changes/`. Templates and domain context are linked from the workflow. Preserve the existing canonical `docs/specs/REQUIREMENTS.md` when extracting knowledge.

Default SDD checks require every changed implementation path to be named by a changed ready record. Completion additionally requires passing test evidence and matching source/test fingerprints. Run `python tools/sdd_guard.py --complete --record docs/changes/<ID>.json` before calling the change complete. All required bench/vehicle gates still apply to system completion.

The pre-commit hook validates the Git index: stage the relevant specifications, record, tests and evidence along with the code. Enable it using the existing bootstrap or `git config core.hooksPath .githooks` with Bash/Python 3 available. CI runs the SDD guard on the complete pull-request/push diff; repository administrators should make foundation checks required before merging. This local change does not configure remote branch protection.

## Before opening a pull request

```bash
make test
make guard
bash -n scripts/*.sh scripts/lib/*.sh .githooks/pre-commit
```

## Evidence requirements

- State the full S70 Software Version suffix and Hardware Version, but redact unique identifiers.
- Describe whether the test used a bench IHU or a parked vehicle.
- Include checksums for original work you are permitted to distribute.
- Do not attach proprietary firmware, paid packages, private keys or unredacted logs.
- Separate observation from inference.

## Open Headunit changes

Patches to the Open Headunit submodule must retain AGPL-3.0 notices and should be proposed upstream whenever they are generally useful. Do not overwrite the submodule with copied source.
