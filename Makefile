PYTHON ?= python3
PROFILE ?= $(shell ls -dt artifacts/device-profile-* 2>/dev/null | head -n 1)
APK ?=

.PHONY: bootstrap test guard build profile verify install smoke clean bundle

bootstrap:
	./scripts/bootstrap.sh

test:
	$(PYTHON) -m unittest discover -s tests -v

guard:
	$(PYTHON) tools/repo_guard.py

build:
	./scripts/build-open-headunit.sh

profile:
	./scripts/collect-ihu-profile.sh

verify:
	@test -n "$(PROFILE)" || (echo "No profile found. Set PROFILE=artifacts/device-profile-..." >&2; exit 2)
	$(PYTHON) tools/profile_report.py "$(PROFILE)" --strict-v333

install:
	@test -n "$(APK)" || (echo "Set APK=dist/file.apk" >&2; exit 2)
	./scripts/install-open-headunit-adb.sh --apk "$(APK)" --acknowledge-parked

smoke:
	./scripts/smoke-test-open-headunit.sh

clean:
	rm -rf dist artifacts .test-output

bundle:
	./scripts/create-git-bundle.sh
