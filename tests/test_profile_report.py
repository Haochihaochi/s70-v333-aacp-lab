from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from profile_report import analyze_profile, parse_wm  # noqa: E402


class ProfileReportTests(unittest.TestCase):
    def make_profile(self, root: Path, display_id: str = "SWSS11R1022H8BNI.00333") -> Path:
        root.mkdir(parents=True, exist_ok=True)
        (root / "properties.txt").write_text(
            "\n".join([
                f"ro.build.display.id={display_id}",
                "ro.build.version.release=9",
                "ro.build.version.sdk=28",
                "ro.build.type=user",
                "ro.debuggable=0",
                "ro.product.cpu.abilist=arm64-v8a,armeabi-v7a",
                "ro.boot.verifiedbootstate=green",
            ]) + "\n",
            encoding="utf-8",
        )
        (root / "features.txt").write_text("feature:android.hardware.usb.host\nfeature:android.hardware.wifi\n", encoding="utf-8")
        (root / "packages-known.txt").write_text(
            "com.android.packageinstaller=true\ncom.andrerinas.headunitrevived=false\n",
            encoding="utf-8",
        )
        (root / "wm.txt").write_text("Physical size: 1920x720\nPhysical density: 240\n", encoding="utf-8")
        (root / "selinux.txt").write_text("Enforcing\n", encoding="utf-8")
        (root / "id.txt").write_text("uid=2000(shell) gid=2000(shell)\n", encoding="utf-8")
        return root

    def test_v333_profile(self):
        with TemporaryDirectory() as temp:
            profile = self.make_profile(Path(temp) / "profile")
            data = analyze_profile(profile)
            self.assertTrue(data["target"]["v333_evidence"])
            self.assertEqual(data["target"]["android_sdk"], 28)
            self.assertTrue(data["capabilities"]["usb_host"])
            self.assertTrue(data["capabilities"]["receiver_test_ready"])
            self.assertEqual(data["target"]["display"]["width"], 1920)

    def test_non_v333_is_not_confirmed(self):
        with TemporaryDirectory() as temp:
            profile = self.make_profile(Path(temp) / "profile", "SWSS11R1022H8BNI.00300")
            data = analyze_profile(profile)
            self.assertFalse(data["target"]["v333_evidence"])
            self.assertFalse(data["capabilities"]["receiver_test_ready"])

    def test_override_density_wins(self):
        parsed = parse_wm("Physical size: 1280x720\nPhysical density: 160\nOverride density: 200\n")
        self.assertEqual(parsed, {"width": 1280, "height": 720, "density": 200})


if __name__ == "__main__":
    unittest.main()
