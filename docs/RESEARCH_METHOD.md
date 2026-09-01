# v333 research method

## Question 1: Can the receiver run?

Answer this independently of sideload access. Build the pinned receiver, run it on Android 9 hardware and establish codec, display and USB behaviour.

## Question 2: What access already exists?

Only document mechanisms you can lawfully observe on your own IHU:

- Authorized ADB.
- Exported activities and intent handlers.
- Official USB update behaviour.
- Package installer availability.
- User-debug versus user build properties.
- Developer-port behaviour on a bench unit.

## Question 3: What changed in v333?

Use sanitized comparisons rather than assumptions:

```bash
python3 tools/diff_profiles.py artifacts/v300-profile artifacts/v333-profile
```

Compare:

- Build properties.
- System packages and package paths.
- Features and USB services.
- Exported components from selected packages.
- Log events produced by the same harmless USB insertion or settings navigation.

## Question 4: Can an install be recovered?

Before writing anything, document:

- Exact hardware/version match.
- Original backup source and checksum.
- Restoration transport.
- Expected partition table.
- Stable power arrangement.
- Result of a bench restoration rehearsal.

A hypothesis is not an installation method until rollback has been demonstrated.
