PACKAGE=smartypants
SCRIPT=smartypants

INSTALL_TEST_DIR=/tmp/$(PACKAGE)_install_test
# if version or naming isn't matched to environment, for example, Python 2.6,
# run the following to override:
#   make VENV_PY2_CMD=virtualenv-python2.6 install_test
VENV_PY2_CMD=virtualenv-python2.7
VENV_PY3_CMD=virtualenv-python3.2

BUILD_CMD=./setup.py sdist --formats gztar,zip bdist_wininst --plat-name win32

build:
	$(BUILD_CMD)

upload:
	$(BUILD_CMD) upload

install_test: $(VENV_PY2_CMD) $(VENV_PY3_CMD)

$(VENV_PY2_CMD) $(VENV_PY3_CMD):
	rm -rf $(INSTALL_TEST_DIR)
	$@ $(INSTALL_TEST_DIR)
	./setup.py sdist --dist-dir $(INSTALL_TEST_DIR)
	$(INSTALL_TEST_DIR)/bin/pip install $(INSTALL_TEST_DIR)/*.tar.gz
	. $(INSTALL_TEST_DIR)/bin/activate ; type $(SCRIPT)
	$(INSTALL_TEST_DIR)/bin/$(SCRIPT) --version

.PHONY: build upload install_test $(VENV_PY2_CMD) $(VENV_PY3_CMD)
