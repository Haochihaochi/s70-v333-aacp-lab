# Security policy

## Reporting

Open a private security report when possible. Do not publish vendor credentials, signing material, personal identifiers, production service endpoints or a method that could affect vehicles you do not own or have permission to test.

## Data handling

Before sharing a profile or log:

1. Run `tools/redact_text.py` on free-form logs.
2. Remove VIN, serial, IMEI/MEID, MAC addresses, account identifiers and location history.
3. Do not upload APKs pulled from the IHU or any partition image.
4. Share hashes and independently written observations instead of proprietary binaries.

## Supported scope

Supported reports concern this repository's scripts, parsers, build configuration and receiver-integration patches. Proprietary firmware vulnerabilities should be disclosed responsibly to the relevant vendor rather than published here without remediation planning.
