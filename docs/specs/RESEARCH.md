# Research findings and tool assessment

Document: S70-AA-RES · Version: 0.1 · Checked: 2026-09-13

## 1. Conclusion

There are useful tools for the receiver, simulation, diagnostics, and ordinary app recovery. **No complete, verified solution was found in the reviewed sources that combines dongle-free Android Auto, installation on a locked 2024 S70 Flagship v333, full factory integration, and independently proven recovery.** This is a scoped research result, not proof that no private or future method exists.

The recommended route is a pinned Android receiver APK, minimal S70-specific integration, a separate commissioning tool, and staged verification. For this owner, access, matching-bench availability, and independent recovery are the main feasibility dependencies. No vehicle was connected or tested during this research.

## 2. Evidence classification

| Finding | Evidence | Confidence and implication |
|---|---|---|
| Owner has a 2024 Flagship, v333, no developer access or spare IHU; wired is sufficient initially | Owner response on 2026-09-13 | Confirmed project scope; full hardware/build identity still unmeasured |
| Newer S70s advertise native projection | Proton's [2026 announcement](https://www.proton.com/happenings/2026/february/proton-defines-malaysia-s-sporty-sedan-with-the-2026-proton-s70) and [model page](https://www.proton.com/models/s70) | OEM evidence for newer product; does not prove a retrofit, matching hardware, or safe firmware transfer to 2024 v333 |
| S70 Android 9 basis has been reported | Maintainer/community [S70 issue #84](https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/84), including an April 2024 comment | Firsthand community discussion, not a profile of this owner's production unit |
| v333 sideload restrictions have been reported | August 2025 [issue #112](https://github.com/xeon1989/Proton-X50-APK-Installer-ATLAS/issues/112); related February 2025 comments in #84 discuss restricted engineering access | Evidence of a problem report; no reproducible complete v333 install/recovery procedure in the inspected threads |
| Open Headunit is an Android receiver candidate | [Project](https://github.com/andreknieriem/open-headunit) and [maintainer FAQ](https://headunit.andrerinas.com/guides/faq/) | Available source and documented receiver behavior; S70 support remains untested |
| Existing project pin is a beta baseline | [Pinned commit](https://github.com/andreknieriem/open-headunit/commit/2f07eeec18d3357e865e761ec76423943dfd880e), dated 2026-08-31; [Gradle source](https://github.com/andreknieriem/open-headunit/blob/2f07eeec18d3357e865e761ec76423943dfd880e/app/build.gradle.kts) reports `3.3.0-beta4` | Build input verified from source; not a validated release artifact |
| Upstream has moved since that pin | GitHub latest-release API returned [v.3.4.0-beta2](https://github.com/andreknieriem/open-headunit/releases/tag/v.3.4.0-beta2), published 2026-09-12 | Current release label at research time; beta status argues for deliberate comparison and qualification |
| Wireless behavior changes with phone software | Current [upstream README](https://github.com/andreknieriem/open-headunit) warns about AA 17.4+ helper/self-mode triggers; [wireless guide](https://headunit.andrerinas.com/guides/wireless/) covers alternate modes | Maintainer report, not independent S70 reproduction; wireless deferred and version-sensitive |
| Region availability needs direct confirmation | [Google requirements/region list](https://support.google.com/androidauto/answer/6348019?hl=en-GB) omits Malaysia when checked; [Proton 2026 brochure](https://cms-assets.proton.com/proton-cms-blob/media/hsxlpppe/2026-protons70_brochure_fa.pdf) includes an availability qualification | Official materials do not fully resolve local service availability. Validate the owner's account/phone/apps and seek OEM clarification; do not infer either universal availability or universal failure |

The old [2024 multimedia manual URL](https://www.proton.com/assets/pdf/S70/S70_Multimedia_Manual_Aug2024_compressed.pdf) redirected to Proton's homepage during direct access. Search indexing still exposed historical snippets, but those are not used to assert exact target specifications. Obtain the correct manual from the [official owner's-manual entry point](https://www.proton.com/after-sales/owners-manual) or service provider. Do not substitute a 2026 manual as a v333 service guide.

## 3. Receiver and platform alternatives

| Candidate | Suitability | Decision |
|---|---|---|
| Open Headunit | Android APK with inspectable source and an existing repository pin; APIs/features can be adapted | Primary experimental base; hardware/protocol audit and release qualification required |
| [Headunit Reloaded / HUR](https://play.google.com/store/apps/details?id=gb.xxy.hr) | Commercial receiver app offered for Android; useful as a separately licensed comparison | Optional reference-device/bench comparator; not the source base and does not grant v333 install access |
| [OpenAuto](https://github.com/f1xpl/openauto) with [aasdk](https://github.com/f1xpl/aasdk) | Desktop/Linux/Raspberry Pi-oriented receiver stack | Protocol reference only; porting burden and an external runtime do not fit the proposed original-IHU APK architecture |
| [Google DHU](https://developer.android.com/training/cars/testing/dhu) | Official desktop testing receiver for phone apps | Phone baseline and comparison tool; not a production redistributable S70 APK |
| OEM retrofit/update | Potentially the strongest integration if actually available for this exact unit | Check eligibility with OEM/service before investing in access research; not verified by reviewed public sources |
| AAOS image/emulator | Useful for AAOS applications and standardized vehicle-property experiments | Not a drop-in replacement or faithful v333 simulator |
| Carlinkit/AutoKit or another dongle-dependent route | Conflicts with the required no-dongle runtime | Excluded |
| [s70unlock](https://github.com/username688/s70unlock) / X50 installer recipes | Existing repository assessment found UI links rather than a complete S70 installation mechanism; X50 instructions are model-specific | Not accepted as a v333 installation or recovery dependency |

The receiver project's [license at the pinned revision](https://github.com/andreknieriem/open-headunit/blob/2f07eeec18d3357e865e761ec76423943dfd880e/LICENSE) is AGPL-3.0. Plan to preserve its terms, notices, and corresponding source when distributing derivatives. A repository license is not evidence that every bundled dependency or protocol credential is suitable for the proposed distribution; audit those separately. No certification or vendor endorsement is assumed.

## 4. Tool coverage against the owner's requirements

| Need | Tool/resource | What it contributes | Missing piece |
|---|---|---|---|
| Build a native IHU app | Android SDK/NDK/Gradle + Open Headunit | Compiled receiver APK | S70 access and integrations |
| App-only simulation | Android AVD and synthetic host harness | UI, lifecycle, state and fault tests | Vendor hardware behavior |
| Phone/Android Auto reference | Google DHU | Phone apps, projection reference, simulated focus/input | Proposed APK execution and v333 tests |
| Device profiling | [ADB](https://developer.android.com/tools/adb), selected dumpsys/logcat, local profile tools | Readable device evidence where permitted | Enabled authorized access; redaction |
| App installation/removal | Authorized Android package manager via PC or supported factory UI | Ordinary package operations | Not an unlock and not a boot repair tool |
| Artifact checks | [apksigner](https://developer.android.com/tools/apksigner), Android APK inspection | Signature and package verification | Functional/vehicle compatibility |
| Automated UI trials | [UI Automator](https://developer.android.com/training/testing/other-components/ui-automator) | Android UI/system-dialog automation | Must choose target-compatible version and restrict test actions |
| Timing/resource diagnosis | [Android profiling tools](https://developer.android.com/studio/profile), [Perfetto](https://perfetto.dev/docs/), in-app timestamps | Performance analysis | API 28/vendor access may restrict available captures |
| Offline package research | [jadx](https://github.com/skylot/jadx), [Apktool](https://apktool.org/) | Inspect legitimately obtained code/resources/manifests | Cannot create install privilege, simulate the SoC, or guarantee correct decompilation |
| Transport diagnosis | [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html), supported USB capture | Lab traffic metadata and fault investigation | Encryption and hardware/driver visibility limitations |
| Full v333 pre-install qualification | Matching bench IHU with representative peripherals and technician | Real hardware/firmware tests and recovery rehearsal | Must source access; unavailable to owner today |
| OS boot failure fallback | Verified target-specific OEM/service recovery | Independent restoration | Exact method, materials, and rehearsal not yet obtained |

No paid software purchase, plugin installation, firmware download, vendor-server interaction, or vehicle mutation is needed for this design phase. Hardware and service costs should be quoted once the exact IHU and required fixture are established.

## 5. Existing repository assessment

Inspected the local repository at baseline commit `dd4b0f6` and its scripts/configuration. This was a source review, not a device test. The foundation is reusable but does not satisfy the new release requirements yet.

| Existing component | Useful foundation | Gap before vehicle use |
|---|---|---|
| [Build helper](../../scripts/build-open-headunit.sh) and CI | Pins upstream and records APK checksum | Builds a debug APK; release signing, strict output identity, dependency review, and qualification are pending |
| [ADB installer](../../scripts/install-open-headunit-adb.sh) | Ordinary package install with authorized-device check | Weak firmware substring check and force option; no full hardware/signing/recovery/evidence gate; launches immediately; no journal or controlled rollback |
| [Uninstaller](../../scripts/uninstall-open-headunit-adb.sh) | Removes the known upstream app ID | Requires working ADB; no independent recovery; future custom app identity must be handled explicitly |
| [Profile collector](../../scripts/collect-ihu-profile.sh) | Read-only platform observations and error files | Raw audio/Wi-Fi/connectivity dumps can include personal data; output is not sanitized merely because properties are allowlisted |
| [Profile report](../../tools/profile_report.py) | Parses useful target/capability summaries | `receiver_test_ready` only combines a version marker, USB feature and API threshold; it is not a vehicle-install readiness assessment |
| Package-presence checks | Attempt to detect installed packages | Depend on `pm path` exit behavior; require checking returned package paths and denied/unknown cases before trusting booleans |
| [Smoke test](../../scripts/smoke-test-open-headunit.sh) | Launch and diagnostic collection | Clears logcat, tolerates failures, and does not assert real projection or factory coexistence; cannot be a release gate |
| Foundation tests / guard | Synthetic report checks and tracked-file restrictions | No receiver, recovery, hardware, privacy-export, or complete installation tests yet |

The specification task does not modify these scripts. The current helpers remain research tools and must not be represented as the finished commissioning or fallback product.

The selected receiver's [pinned manifest](https://github.com/andreknieriem/open-headunit/blob/2f07eeec18d3357e865e761ec76423943dfd880e/app/src/main/AndroidManifest.xml) declares broad optional capabilities and multiple automatic entry points. A wired S70 release needs a reviewed permission/component profile. Its [settings documentation](https://headunit.andrerinas.com/guides/settings/) exposes several routing choices; none is accepted as an S70 preset without measurement.

## 6. Research scope and remaining evidence

Reviewed the project documentation and scripts; live upstream code/build metadata and release information; the existing S70 access issue threads; OEM current S70 material; Google Android Auto, DHU, USB, ADB, emulator, audio, Verified Boot and A/B documentation; and primary tool/project documentation. Searches included S70/v333 installation, OEM retrofit eligibility, receiver alternatives, testing environments, and recovery limitations.

No suitable public turnkey v333 access/recovery method was established. Community claims and newer S70 specifications were kept distinct from this target. Unknown exact OEM packages, signal mappings, SoC/recovery tools, storage layout, calibration dependencies, and thermal limits remain unresolved rather than inferred from another model.

Next evidence should answer four decisive questions:

1. Can a normal receiver APK be installed and removed on the exact IHU through supported, repeatable access?
2. Can the factory mic, USB path, audio, keys, cameras and alerts coexist with that ordinary app?
3. Can a matching unit be restored when the app, UI, or Android itself is unavailable?
4. Can those results be obtained on a matching bench setup before the owner's vehicle is changed?

Until then, the architecture is actionable for laboratory development but conditionally feasible for the vehicle. The [requirements gates](REQUIREMENTS.md#5-gates-and-present-status) carry those limitations into the product and technical specifications.
