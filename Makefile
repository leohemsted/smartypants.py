# Copyright (c) 2013 Yu-Jie Lin
# Licensed under the BSD License, for detailed license information, see COPYING

PACKAGE=smartypants
SCRIPT=smartypants

PY2_CMD=python2
PY3_CMD=python3
INSTALL_TEST_DIR=/tmp/$(PACKAGE)_install_test
# if version or naming isn't matched to environment, for example, Python 2.6,
# run the following to override:
#   make VENV_PY2_CMD=virtualenv-python2.6 install_test
VENV_PY2_CMD=virtualenv-python2.7
VENV_PY3_CMD=virtualenv-python3.2

BUILD_CMD=./setup.py sdist --formats gztar,zip bdist_wininst --plat-name win32

DOC_FILES = docs/conf.py $(wildcard docs/*.rst)

# ============================================================================

build:
	$(BUILD_CMD)

upload:
	$(BUILD_CMD) upload

upload_doc: doc
	$(PY2_CMD) setup.py upload_sphinx

# ============================================================================

doc: docs/_build/html

docs/_build/html: $(DOC_FILES) smartypants.py smartypants_command.py
	make -C docs html

smartypants_command.py: smartypants
	ln -sf smartypants $@

# ============================================================================

test: test_pep8 test_pyflakes test_test install_test

test_%:
	@echo '========================================================================================='
	$(PY2_CMD) setup.py $(subst test_,,$@)
	@echo '-----------------------------------------------------------------------------------------'
	$(PY3_CMD) setup.py $(subst test_,,$@)

install_test: $(VENV_PY2_CMD) $(VENV_PY3_CMD)

$(VENV_PY2_CMD) $(VENV_PY3_CMD):
	@echo '========================================================================================='
	rm -rf $(INSTALL_TEST_DIR)
	$@ $(INSTALL_TEST_DIR)
	./setup.py sdist --dist-dir $(INSTALL_TEST_DIR)
	$(INSTALL_TEST_DIR)/bin/pip install $(INSTALL_TEST_DIR)/*.tar.gz
	. $(INSTALL_TEST_DIR)/bin/activate ; type $(SCRIPT)
	$(INSTALL_TEST_DIR)/bin/$(SCRIPT) --version

# ============================================================================

clean:
	rm -rf *.pyc build dist __pycache__
	rm smartypants_command.py
	make -C docs clean

# ============================================================================

.PHONY: build upload doc install_test $(VENV_PY2_CMD) $(VENV_PY3_CMD) clean
