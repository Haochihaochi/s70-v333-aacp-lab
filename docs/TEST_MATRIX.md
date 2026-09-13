# Test matrix

> For the complete September 2026 test design, environment limits, and requirement traceability, see the [validation and laboratory plan](specs/VALIDATION.md). This foundation checklist alone is insufficient for vehicle qualification.

All in-car tests must be performed while parked.

| Area | Baseline evidence | Pass condition |
|---|---|---|
| Boot | ACC off/on cycles | Factory UI and receiver remain usable |
| USB | Phone enumeration | Stable wired session without reconnect loop |
| Video | H.264 first, H.265 optional | No black screen, artifacts or thermal runaway |
| Display | Resolution/DPI profile | Full touch mapping and readable UI |
| Media audio | Music playback | Correct speakers, no persistent focus lock |
| Navigation audio | Prompt over media | Duck/mix behaviour is acceptable |
| Microphone | Assistant/voice call test | Clear uplink with no factory mic conflict |
| Steering controls | Media/navigation keys | No duplicate or unsafe mappings |
| Camera priority | Reverse/360 activation | Factory camera immediately takes foreground |
| Factory alerts | Parking/chimes | Audible and visible alerts are preserved |
| Disconnect | Cable removal / Wi-Fi loss | Clean return to factory UI |
| Uninstall | Ordinary package removal | Factory state remains functional |
