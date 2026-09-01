# Upstream assessment

## Selected receiver: Open Headunit

Repository: https://github.com/andreknieriem/open-headunit

Reasons selected:

- Complete Android APK rather than a Linux-only head-unit stack.
- Supports wired USB and multiple wireless modes.
- Supports old Android versions, including the expected Android 9 environment.
- Contains active handling for display, audio, microphone, media buttons and Chinese Android head-unit variants.
- Clear AGPL-3.0 licence.
- Active upstream as of the pinned commit.

## Rejected as the primary base: username688/s70unlock

Repository: https://github.com/username688/s70unlock

Observed contents:

- `index.html`
- `2`

Both files are essentially duplicate HTML pages. They attempt to launch Android Settings through an intent and link to external Settings Shortcut and Carlinkit APK downloads. There is no installer, privilege path, Android project, reverse-engineering tooling, test suite or recovery mechanism. No licence is present. The repository is therefore evidence of an attempted UI entry point, not reusable sideload code.

## Reference only: X50 ATLAS/GKUI installers

Repositories:

- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS
- https://github.com/xeon1989/Proton-X50-APK-Installer-GKUI

Their value is architectural: they demonstrate that a receiver APK and a model-specific privileged file execution/install path are separate concerns. Their known USB triggers and package paths are not assumed to work on S70 v333.

## Reference only: S70 issues

- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/84
- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/112

These threads indicate community investigation of S70 firmware and later v333 restrictions, but they do not provide a complete public v333 installer.
