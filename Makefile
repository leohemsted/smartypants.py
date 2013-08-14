BUILD_CMD=./setup.py sdist --formats gztar,zip bdist_wininst --plat-name win32

build:
	$(BUILD_CMD)

upload:
	$(BUILD_CMD) upload

.PHONY: build upload
