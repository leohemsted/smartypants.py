# Copyright (c) 2013, 2014 Yu-Jie Lin
# Licensed under the BSD License, for detailed license information, see COPYING

PACKAGE=smartypants
SCRIPT=smartypants

PY2_CMD=python2
PY3_CMD=python3
INSTALL_TEST_DIR=/tmp/$(PACKAGE)_install_test

BUILD_CMD=./setup.py sdist --formats gztar,zip bdist_wheel bdist_wininst --plat-name win32

DOC_FILES = CHANGES.rst COPYING docs/conf.py $(wildcard docs/*.rst)

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

# FIXME making a symlink is just an workaround since smartypants script isn't
# importable, therefore Sphinx autodoc cannot pick it up. There are a couple of
# options:
#
# 1. making a `main()` function in smartypants.py, the module file. However,
#    you can't use section heading inside the docstring of a function, or it
#    would result an error about unexpected section heading.
#
#	2. making a smartypants.py as a package, so a new module like
#	   smartypants.cli, just for the command-line script
#
# If you know a better solution for making documentation for smartypants
# command, please open an issue to discuss. Right now, stick with this ugly
# symlink.
smartypants_command.py: smartypants
	ln -sf smartypants $@

# ============================================================================

test: test_isort test_doc8 test_pep8 test_pyflakes test_test install_test

test_%:
	@echo '========================================================================================='
	$(PY2_CMD) setup.py $(subst test_,,$@)
	@echo '-----------------------------------------------------------------------------------------'
	$(PY3_CMD) setup.py $(subst test_,,$@)

test_doc8:
	@echo '========================================================================================='
	doc8 $(filter %.rst,$(DOC_FILES))

install_test: install_test_py2 install_test_py3

install_test_py2 install_test_py3:
	@echo '========================================================================================='
	rm -rf $(INSTALL_TEST_DIR)
	$(eval PY_CMD = \
		$(if $(findstring py2,$@),\
			$(PY2_CMD),\
			$(if $(findstring py3,$@),\
				$(PY3_CMD),\
				$(error Do not know what to do with $@)\
			)\
		)\
	)
	$(PY_CMD) -m virtualenv $(INSTALL_TEST_DIR)
	LC_ALL=C $(PY_CMD) setup.py --version >/dev/null
	$(PY_CMD) setup.py sdist --dist-dir $(INSTALL_TEST_DIR)
	$(INSTALL_TEST_DIR)/bin/pip install $(INSTALL_TEST_DIR)/*.tar.gz
	@\
		CHK_VER="`$(PY_CMD) $(SCRIPT) --version 2>&1`";\
		cd $(INSTALL_TEST_DIR);\
		. bin/activate;\
		[ "`type $(SCRIPT)`" = "$(SCRIPT) is $(INSTALL_TEST_DIR)/bin/$(SCRIPT)" ] &&\
		[ "$$CHK_VER" = "`bin/$(SCRIPT) --version 2>&1`" ] &&\
		[ "`echo '"foobar"' | bin/$(SCRIPT)`" = '&#8220;foobar&#8221;' ]
	rm -rf $(INSTALL_TEST_DIR)

# ============================================================================

clean:
	rm -rf *.pyc build dist __pycache__
	rm smartypants_command.py
	make -C docs clean

# ============================================================================

.PHONY: build upload doc install_test install_test_py2 install_test_py3 clean
