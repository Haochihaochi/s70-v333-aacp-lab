#!/usr/bin/env python3
"""Parse a read-only S70 IHU profile into machine- and human-readable reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def parse_key_values(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def parse_features(text: str) -> list[str]:
    features: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("feature:"):
            features.append(line.removeprefix("feature:").strip())
    return sorted(set(features))


def parse_wm(text: str) -> dict[str, int | None]:
    size_match = re.search(r"(?:Physical|Override) size:\s*(\d+)x(\d+)", text)
    density_matches = re.findall(r"(?:Physical|Override) density:\s*(\d+)", text)
    return {
        "width": int(size_match.group(1)) if size_match else None,
        "height": int(size_match.group(2)) if size_match else None,
        "density": int(density_matches[-1]) if density_matches else None,
    }


def parse_int(value: str | None) -> int | None:
    try:
        return int(value or "")
    except ValueError:
        return None


def contains_v333_evidence(properties: dict[str, str]) -> bool:
    joined = " ".join(properties.values()).lower()
    return any(token in joined for token in (".00333", "v333", "_00333", "-00333"))


def analyze_profile(profile_dir: Path) -> dict[str, Any]:
    properties = parse_key_values(read_text(profile_dir / "properties.txt"))
    packages = parse_key_values(read_text(profile_dir / "packages-known.txt"))
    features = parse_features(read_text(profile_dir / "features.txt"))
    display = parse_wm(read_text(profile_dir / "wm.txt"))
    sdk = parse_int(properties.get("ro.build.version.sdk"))
    abilist = properties.get("ro.product.cpu.abilist") or properties.get("ro.product.cpu.abi", "")
    abis = [item.strip() for item in abilist.split(",") if item.strip()]
    selinux = read_text(profile_dir / "selinux.txt").strip()
    identity = read_text(profile_dir / "id.txt").strip()
    version_confirmed = contains_v333_evidence(properties)
    usb_host = "android.hardware.usb.host" in features
    package_installer = packages.get("com.android.packageinstaller") == "true" or packages.get("com.google.android.packageinstaller") == "true"
    open_headunit_installed = packages.get("com.andrerinas.headunitrevived") == "true"
    is_root_shell = "uid=0(" in identity

    warnings: list[str] = []
    if not version_confirmed:
        warnings.append("No v333 marker was found in the allow-listed build properties; verify the About IHU screen manually.")
    if sdk is not None and sdk != 28:
        warnings.append(f"Android SDK is {sdk}, not the community-reported SDK 28. Treat existing assumptions as unverified.")
    if not usb_host:
        warnings.append("android.hardware.usb.host was not reported; wired Android Auto may need USB-role investigation.")
    if not package_installer:
        warnings.append("No standard Android package installer package was detected.")
    if properties.get("ro.build.type") == "user" and properties.get("ro.debuggable") != "1":
        warnings.append("The unit appears to be a non-debuggable user build; ordinary ADB access may be unavailable after reboot or reset.")
    if properties.get("ro.boot.verifiedbootstate", "").lower() == "green":
        warnings.append("Verified Boot reports green. Do not flash modified partitions without a complete, tested recovery path.")

    receiver_test_ready = bool(version_confirmed and usb_host and sdk is not None and sdk >= 21)

    return {
        "profile_dir": str(profile_dir),
        "target": {
            "v333_evidence": version_confirmed,
            "android_release": properties.get("ro.build.version.release"),
            "android_sdk": sdk,
            "build_display_id": properties.get("ro.build.display.id"),
            "build_type": properties.get("ro.build.type"),
            "debuggable": properties.get("ro.debuggable"),
            "verified_boot_state": properties.get("ro.boot.verifiedbootstate"),
            "selinux": selinux or None,
            "root_shell": is_root_shell,
            "abis": abis,
            "display": display,
        },
        "capabilities": {
            "usb_host": usb_host,
            "package_installer": package_installer,
            "open_headunit_installed": open_headunit_installed,
            "receiver_test_ready": receiver_test_ready,
        },
        "properties": properties,
        "features": features,
        "packages": packages,
        "warnings": warnings,
    }


def markdown_report(data: dict[str, Any]) -> str:
    target = data["target"]
    caps = data["capabilities"]
    display = target["display"]
    lines = [
        "# S70 IHU profile summary",
        "",
        f"- v333 evidence: **{target['v333_evidence']}**",
        f"- Build display ID: `{target['build_display_id'] or 'unknown'}`",
        f"- Android: `{target['android_release'] or 'unknown'}` / SDK `{target['android_sdk'] if target['android_sdk'] is not None else 'unknown'}`",
        f"- Build type / debuggable: `{target['build_type'] or 'unknown'}` / `{target['debuggable'] or 'unknown'}`",
        f"- ABI list: `{', '.join(target['abis']) or 'unknown'}`",
        f"- Display: `{display['width'] or 'unknown'}x{display['height'] or 'unknown'}` at density `{display['density'] or 'unknown'}`",
        f"- USB host feature: **{caps['usb_host']}**",
        f"- Standard package installer detected: **{caps['package_installer']}**",
        f"- Open Headunit already installed: **{caps['open_headunit_installed']}**",
        f"- Receiver-test readiness: **{caps['receiver_test_ready']}**",
        f"- SELinux: `{target['selinux'] or 'unknown'}`",
        f"- Verified Boot: `{target['verified_boot_state'] or 'unknown'}`",
        "",
        "## Warnings",
        "",
    ]
    warnings = data.get("warnings", [])
    lines.extend([f"- {warning}" for warning in warnings] or ["- None detected by the foundation checks."])
    lines.extend([
        "",
        "This report does not prove that flashing, rooting or a privileged install path is safe. It only summarizes read-only observations.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile_dir", type=Path)
    parser.add_argument("--strict-v333", action="store_true")
    args = parser.parse_args()

    if not args.profile_dir.is_dir():
        parser.error(f"Profile directory does not exist: {args.profile_dir}")

    data = analyze_profile(args.profile_dir)
    (args.profile_dir / "summary.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.profile_dir / "summary.md").write_text(markdown_report(data), encoding="utf-8")
    print(markdown_report(data))

    if args.strict_v333 and not data["target"]["v333_evidence"]:
        print("Strict v333 verification failed.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
