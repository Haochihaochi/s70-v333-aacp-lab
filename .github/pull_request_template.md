## Summary

## Specification and test traceability

- SDD change record and requirements:
- Product behavior and technical specification:
- Test cases written before implementation:
- Actual results, environment, evidence and source/artifact identity:
- Completion scope and any blocked hardware/recovery gates:

- [ ] Requirements → product behavior → technical design → test cases preceded code
- [ ] Changed implementation paths are covered by a changed ready SDD record
- [ ] No deferred CarPlay/wireless or untested v333 capability is claimed as complete
- [ ] For a completed change, `sdd_guard.py --complete --record ...` passes

## Safety and test environment

- [ ] Bench IHU or non-vehicle Android reference device
- [ ] Parked vehicle only
- [ ] No proprietary firmware/APK/key/certificate added
- [ ] No unique vehicle or personal identifiers added

## Validation

- [ ] `make test`
- [ ] `make guard`
- [ ] Bash syntax check
- [ ] Receiver build, when applicable

## Licence/attribution

Describe third-party code and its licence, or state that all changes are original.
