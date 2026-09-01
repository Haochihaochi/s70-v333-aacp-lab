# Third-party notices

## Open Headunit

- Repository: https://github.com/andreknieriem/open-headunit
- Pinned commit: `2f07eeec18d3357e865e761ec76423943dfd880e`
- Licence: GNU Affero General Public License v3.0
- Role: Android Auto receiver implementation.

Open Headunit is included as a Git submodule, not copied into the foundation's Apache-2.0 source tree.

## Public S70 research references not imported

### username688/s70unlock

- Repository: https://github.com/username688/s70unlock
- Audit result: two duplicate HTML files with an Android Settings intent and external APK download links.
- No substantive sideload/install implementation was found.
- No licence file was found.
- Decision: reference only; no source copied.

### Proton X50 installer repositories

- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS
- https://github.com/xeon1989/Proton-X50-APK-Installer-GKUI

These are model/version-specific references. Their USB trigger paths and updater assumptions must not be reused on S70 v333 without independent verification.

### S70 public discussion

- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/84
- https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/112

These discussions are evidence and research context, not executable dependencies.
