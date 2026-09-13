# Requirements specification — S70 v333 wired Android Auto

Document: S70-AA-RS · Version: 0.1 · Date: 2026-09-13 · Status: proposed baseline

## 1. Purpose and confirmed context

The system shall let the owner use Android Auto navigation, media, voice interaction, and calls on the original S70 display without an external projection dongle. It shall preserve the factory vehicle interface and provide evidence-backed failure recovery and testing before installation in the owner's vehicle.

| Item | Baseline | Evidence |
|---|---|---|
| Vehicle | 2024 Proton S70 Flagship | Owner confirmation, 2026-09-13 |
| Displayed firmware | v333 | Owner confirmation; complete version string still required |
| Initial connection | Wired USB; no external projection hardware | Owner confirmation |
| Developer/ADB access | Not available | Owner confirmation |
| Matching spare IHU | Not available | Owner confirmation |
| Hardware revision, API, ABI, pixel dimensions | Unknown | Must be measured; do not inherit newer-model specifications |
| Android 9 / API 28 | Working hypothesis | Community report, not a measurement of this IHU; [research](RESEARCH.md) |
| Phone, Android Auto version, language | Unknown | Compatibility matrix to be established |

IHU means the factory infotainment head unit. Android Auto projects a phone experience; it is not a replacement operating system for the car. Android Automotive OS and its vehicle APIs must not be assumed to exist on this target. See [Google's Android Auto overview](https://developer.android.com/training/cars/platforms/android-auto).

## 2. Scope and definition of full support

For this release, **full support** means every mandatory requirement below passes on the exact supported vehicle and phone combination. It includes preservation of factory functions, not recreating those functions inside Android Auto. An APK that displays maps but loses factory microphone or camera behavior is a prototype, not a completed product.

Included: a wired receiver, S70 compatibility profile and adapters, controlled installation/removal, app recovery, service recovery prerequisites, diagnostics, and an evidence-producing test environment.

Deferred: wireless projection, CarPlay, other S70 years/variants/firmware, instrument-cluster navigation, vehicle GPS forwarding, and generalized public distribution. Existing cluster functions must still be preserved. Wireless requires a separate future validation gate and must not delay the wired baseline.

Excluded from the proposed installation: firmware replacement, factory launcher replacement, persistent privileged services, disabling factory camera/vehicle packages, and direct vehicle-control commands. If ordinary application access cannot achieve a mandatory requirement, record the failure and revisit feasibility rather than silently widening privileges.

## 3. Requirement conventions

**MUST** is mandatory for the release. **SHOULD** is desirable and requires a documented reason if omitted. A deferred feature is not represented as working. Unknown, failed, and untested have different statuses; none counts as passed. Requirement changes require an explicit revision and traceability to the product and technical specifications.

### Target and access

| ID | Priority | Requirement and acceptance |
|---|---|---|
| ID-01 | MUST | Identify the target by full software string, hardware/part revision, build fingerprint where exposed, API, ABI, and relevant factory package versions. A substring such as `v333` alone must never authorize installation. |
| ID-02 | MUST | Maintain an evidence-backed capability profile covering display, decoder, USB roles, audio, microphone, input, power lifecycle, and factory priority behavior. Missing capabilities remain unknown. |
| ID-03 | MUST | Confirm an installation and removal route for this hardware/firmware combination. ADB is usable only if enabled and authorized; a desktop tool must not claim it can create that authorization. |
| ID-04 | MUST | Demonstrate recovery without a working receiver before any owner-vehicle installation. Independent OS recovery or a validated service restoration route is required for OS-level failure. |
| ID-05 | MUST | Recheck identity immediately before each mutation. Reject unknown targets, changed firmware, mismatched evidence, ambiguous device selection, and missing recovery evidence. No production force override. |

### Android Auto and owner experience

| ID | Priority | Requirement and acceptance |
|---|---|---|
| AA-01 | MUST | Establish and sustain a real wired Android Auto session over the factory USB data path using a phone and cable only. No PC, adapter box, or developer server is required during normal use. |
| AA-02 | MUST | Render the negotiated video correctly within the usable display area, with correct aspect ratio, readable interface, and accurate edge-to-edge touch mapping. Resolve actual DPI and margins by measurement. |
| AA-03 | MUST | Support Maps/Waze navigation and a selected Android Auto media app, including simultaneous navigation prompts and media. Record app versions and account/region dependencies. |
| AA-04 | MUST | Support voice interaction through the factory microphone and speech output through the factory speakers. Permissions and denial recovery must be understandable. Phone-mic substitution does not satisfy factory-mic acceptance. |
| AA-05 | MUST | Make, receive, answer, and end a normal test call with intelligible two-way audio and restoration of the prior media state. Establish call audio ownership separately from projection audio; factory Bluetooth hands-free may remain the call path. |
| AA-06 | MUST | Handle supported media/voice steering-wheel inputs once per intended press while preserving factory volume, call, and vehicle-control behavior. Document short/long presses and arbitration. |
| AA-07 | MUST | Recover from cable removal, phone restart, phone lock/unlock, receiver interruption, and suspend/resume without a restart loop or unavailable factory UI. |
| AA-08 | MUST | Provide a clear Return to factory screen action and an independent factory Home/exit route. Initial commissioning is manual-launch only. |
| AA-09 | MUST | Operate with wired projection and any necessary factory call Bluetooth; wireless projection discovery and helper triggers remain disabled in the initial release. |
| AA-10 | MUST | Validate the owner's actual phone, account region, preferred language, and installed Android Auto version. Do not require pinning obsolete phone software to claim compatibility. |
| AA-11 | SHOULD | After commissioning, allow opt-in connection on USB attach once boot/sleep and camera-priority tests pass. Factory startup remains available when no phone is attached. |
| AA-12 | MUST | Separate connection failures from loss of internet. Projection must return a useful state when the phone is offline; online navigation, streaming, and assistant service availability remain external dependencies. |
| AA-13 | MUST | Preserve Android Auto driving restrictions and prohibit receiver setup/diagnostic workflows during normal driving use. Never report an invented parked/speed state to enable restricted actions; unavailable vehicle state requires conservative behavior. |

### Factory coexistence

| ID | Priority | Requirement and acceptance |
|---|---|---|
| VH-01 | MUST | Preserve reverse and 360-camera activation, overlays, touch interaction, and return behavior. Projection must never cover the factory camera or repeatedly take foreground back. |
| VH-02 | MUST | Preserve audible and visible parking alerts, factory warning/chime behavior, and other safety-related IHU notifications. Do not assume all alerts share Android audio focus. |
| VH-03 | MUST | Preserve factory climate and vehicle settings, radio, hands-free calling, Hi PROTON behavior, and access to native navigation/QDLink/connected functions where fitted. Inventory actual functions before changes. |
| VH-04 | MUST | Preserve normal cold start, accessory-power wake, sleep, and off-state behavior, including acceptable battery draw. Do not equate every ACC cycle with an Android reboot. |
| VH-05 | MUST | Yield audio and display through measured factory behavior. If a mandatory priority function cannot be observed or safely preserved, block vehicle release. |
| VH-06 | MUST | Preserve night readability. Use a verified read-only illumination signal where available; otherwise supply a conservative dark/manual theme and document the absence of automatic headlight integration. |
| VH-07 | MUST | Do not inject vehicle-control traffic, remap driving-assistance controls, or take over a camera feed. Factory software remains responsible for those functions. |

### Installation, recovery, and maintenance

| ID | Priority | Requirement and acceptance |
|---|---|---|
| RC-01 | MUST | Limit application installation to ordinary package/data changes and documented app permissions. Preserve factory packages, default Home, firmware, boot settings, security enforcement, and vehicle configuration. |
| RC-02 | MUST | Verify the intended app package, signing-certificate fingerprint, artifact digest, version, supported API/ABI, and approved capability-profile digest before installation. Retain exact tested artifacts. |
| RC-03 | MUST | Record pre-install state and a recoverable app configuration backup; verify original/service restoration material when it is part of the recovery route. A hash or copied image alone does not establish restorability. |
| RC-04 | MUST | Install without immediately starting projection. Confirm package state and recovery access, then launch manually. Keep all boot/USB/Bluetooth auto-start paths disabled during first commissioning. |
| RC-05 | MUST | On receiver failure, stop projection, release app audio/mic/USB resources where the OS permits, and leave the factory interface reachable. Suppress repeated automatic retries. |
| RC-06 | MUST | Maintain a persistent application safe mode for repeated unsuccessful starts and failed updates, covering all entry points. It must require deliberate re-enable after diagnosis. It is not firmware safe mode. |
| RC-07 | MUST | Demonstrate removal with the receiver frozen/crashed and restoration of the previously tested app build after a failed update. Account for Android signing/version restrictions and data-schema compatibility. |
| RC-08 | MUST | Demonstrate recovery after authorized package-operation interruption on a bench system, including loss of the commissioning connection. If recovery access disappears, stop automated writes. |
| RC-09 | MUST | Provide a restoration runbook for UI failure, ADB loss, and OS boot failure, with explicitly tested access methods and service ownership. No unconditional anti-brick promise. |
| RC-10 | MUST | Detect a changed factory firmware/profile and disable automatic projection until revalidated. Never disable the OEM updater to preserve compatibility. |

### Testability, security, and deliverables

| ID | Priority | Requirement and acceptance |
|---|---|---|
| QA-01 | MUST | Provide reproducible host tests and an Android application emulator lab with simulated factory-priority/input/power events. Clearly label simulated evidence. |
| QA-02 | MUST | Establish a phone baseline using Google's DHU, separate from receiver testing. A DHU pass must never be recorded as an S70 APK pass. |
| QA-03 | MUST | Test the receiver with a real phone on Android reference hardware before matching-IHU testing. Reference hardware does not certify S70 drivers. |
| QA-04 | MUST | Complete matching-hardware bench tests and recovery rehearsal before installing in the owner's vehicle. Outsourced testing is acceptable only with traceable hardware identity and the same artifacts. |
| QA-05 | MUST | Complete final parked-vehicle checks after installation because some physical integrations cannot be fully reproduced on a bench. All mandatory functions must have an appropriate verification route. |
| QA-06 | MUST | Link each requirement to tests, results, artifact identity, target identity, environment, and reviewer. A missing prerequisite must produce BLOCKED, not PASS or a silent skip. |
| QA-07 | MUST | Retest affected requirements after receiver, adapter, factory firmware, phone OS, or Android Auto changes. Maintain a rollback-supported compatibility matrix. |
| SE-01 | MUST | Keep diagnostics local and bounded by default. Exclude conversations, recordings, contact content, VINs, device identifiers, tokens, and unredacted connectivity dumps from public reports. Review exports before sharing. |
| SE-02 | MUST | Run without root, accessibility-based takeover, or a production ADB server. Use only justified permissions; validate exported component inputs and restrict app-owned control interfaces. |
| SE-03 | MUST | Preserve upstream licenses and audit bundled native components and protocol credential provenance before distributing a build. Do not represent community software as Google/Proton certified. |
| SE-04 | MUST | Require no project cloud service or paid unlock service during normal operation. Service assistance may be needed for commissioning/recovery and must be disclosed. |
| DL-01 | MUST | Deliver a requirements baseline first, followed by a product specification, then an implementation-ready technical specification, all with common requirement IDs. |
| DL-02 | MUST | Deliver a compatible signed receiver, commissioning/removal tool, lab configuration, test evidence, release manifest, compatibility matrix, and recovery instructions before declaring the product complete. These are future implementation outputs. |

## 4. Proposed quantitative acceptance targets

These are design proposals to refine after stock baselines; they are not measured or safety-certification thresholds. Do not relax a mandatory preservation requirement merely to meet a number. Report all samples and outliers. Averages cannot hide failures of factory priority.

| ID | Measure | Proposed target |
|---|---|---|
| NF-01 | Wired start | At least 29/30 successful connections per supported phone/build pair; p95 at most 15 s from receiver-ready, approved USB permission, and completed phone consent to interactive projection. Record factory boot time separately. |
| NF-02 | Interaction/video | p95 touch-to-visible response at most 200 ms in 50 controlled actions; target 30 fps during animated content. Static-screen frame inactivity is not a failure. |
| NF-03 | Factory camera priority | Zero blocked, hidden, or incorrectly restored camera events in 30 activations across idle, connecting, active, interrupted, and recovering states. Target p95 added delay at most 100 ms versus stock; absolute results must also meet the stock/service baseline. |
| NF-04 | Audio release/factory return | Target app audio cessation within 250 ms of a validated priority event; usable stock UI within 2 s of ordinary receiver exit/failure while Android is healthy. OS boot failure uses service recovery, not this timing. |
| NF-05 | Stability | One 2-hour mixed session per supported phone and an 8-hour bench endurance run on the primary pair, with no receiver-induced OS reboot, ANR, camera/alert loss, or unbounded memory growth. |
| NF-06 | Power/lifecycle | 30 accessory-power cycles and 10 cold boots on the bench without unintended projection auto-launch, loss of recovery access, or factory regression. Off-state draw within OEM limits where available; otherwise an agreed stock baseline plus measurement uncertainty, with no sustained extra wake activity. |
| NF-07 | Installation/removal | Five successful install/remove cycles and five failed-update recovery rehearsals on the matching bench unit. Healthy-OS uninstall target at most 5 minutes after recovery connection is ready. Record OS/service recovery duration separately. |
| NF-08 | Voice/calls/keys | At least 18/20 predefined quiet-cabin voice commands recognized; ten ordinary test calls without persistent mic/route conflicts; each supported key tested 20 times with no unintended duplication or vehicle-control change. |
| NF-09 | Resource limits | Logs capped initially at 20 MB. Measure CPU, memory, storage, temperature, and charging against stock and device limits; agree absolute operating budgets before vehicle release. Unknown thermal limits block endurance approval. |

## 5. Gates and present status

| Gate | Required outcome | Current status |
|---|---|---|
| G0 — Requirements baseline | Review scope, mandatory features, targets, evidence policy | This draft; owner scope confirmed |
| G1 — Access and recovery feasibility | Exact identity, supported access proposal, matching bench access, independently usable recovery route | BLOCKED: unavailable access/bench hardware and unknown recovery |
| G2 — Software/reference lab | Builds and host/AVD tests, DHU phone baseline, real receiver/reference-device baseline | NOT RUN; can proceed while G1 is investigated |
| G3 — Matching bench qualification | Install/remove, failure recovery, hardware integration, endurance, fixed release artifacts | BLOCKED on G1 and G2 |
| G4 — Owner-vehicle commissioning | Approved evidence, controlled install, final parked checks and restoration readiness | BLOCKED on G3 |
| G5 — Supported release | All MUSTs passed; compatibility/support package complete | NOT READY |

G2 progress cannot waive G1 or G3. If no matching bench access can be obtained, the user's requirement for testing on v333 before installation in the owner's car remains unmet. A tablet or emulator does not change that fact.

## 6. Unresolved decisions and responsible parties

| Unknown | Next evidence | Owner |
|---|---|---|
| Full software/hardware identity and physical USB data port | About IHU information and measured profile through supported access | Owner / technician |
| Official retrofit, permitted diagnostic installation, and service recovery eligibility for 2024 v333 | Written confirmation from Proton/ACO Tech or qualified authorized service | Owner / service provider |
| Matching bench availability and recoverability | Loan/rental/service proposal with revision, firmware, peripheral coverage, recovery capability | Project owner / lab |
| Phone model, region, language, app versions | Baseline inventory and DHU trial | Owner / developer |
| Mic and call path, camera priority, key interfaces | Stock observations and matching-bench evidence | Integration developer / lab |
| Restoration credentials, artifacts, calibration/pairing dependencies | Verified service runbook and rehearsal evidence | Recovery technician |
| Numeric thermal/power budgets and timing baseline | Manufacturer limits where available, controlled stock measurements | Lab / reviewer |

## 7. Next specification stages

The product specification shall define first-time setup, connection, factory return, error explanations, technician preflight, recovery screens, compatibility reporting, and support workflow. It must preserve these mandatory requirements.

The technical specification shall define concrete modules, measured vendor interfaces, permissions, package/signing identity, schemas, transport/audio/video implementation, installer transaction handling, exact recovery runbooks, fixtures, and build/release automation. Vendor identifiers, pinouts, or recovery commands must not be invented to fill gaps. The accompanying [architecture](SYSTEM_ARCHITECTURE.md) is the proposed basis for those decisions.
