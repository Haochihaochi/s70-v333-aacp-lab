# Contributing

Contributions should be reproducible, licence-clear and safe to test on a bench unit.

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
