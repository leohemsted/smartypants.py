#!/usr/bin/env python
# Copyright (C) 2013, 2014 by Yu-Jie Lin
# For detail license information, See COPYING

from __future__ import print_function

import codecs
import sys
from distutils.core import Command, setup
from unittest import TestLoader, TextTestRunner

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    # No need of Sphinx for normal users
    BuildDoc = None
try:
    from sphinx_pypi_upload import UploadDoc
except ImportError:
    # Sphinx-PyPI-upload not compatible with Python 3
    UploadDoc = None


CLI_script = 'smartypants'
module_name = 'smartypants'
module_file = 'smartypants.py'

CHECK_FILES = ('.', CLI_script)

# scripts to be exculded from checking
EXCLUDE_SCRIPTS = (
    'conf.py',  # <- docs/conf.py is a auto-generated disaster of PEP8
    'smartypants_command.py',
)


# ============================================================================
# https://groups.google.com/d/msg/comp.lang.python/pAeiF0qwtY0/H9Ki0WOctBkJ
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name == 'mbcs')
    codecs.register(func)


# ============================================================================


class cmd_test(Command):

    description = 'run tests'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run(self):

        loader = TestLoader()
        tests = loader.discover(start_dir='tests')
        runner = TextTestRunner(verbosity=2)
        runner.run(tests)


class cmd_isort(Command):

    description = 'run isort'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run(self):

        try:
            import isort
        except ImportError:
            print(('Cannot import isort, you forgot to install?\n'
                   'run `pip install isort` to install.'), file=sys.stderr)
            sys.exit(1)

        from glob import glob

        print()
        print('Options')
        print('=======')
        print()
        print('Exclude:', EXCLUDE_SCRIPTS)
        print()

        files = ['setup.py', CLI_script, module_file] + glob('tests/*.py')

        print('Results')
        print('=======')
        print()

        fails = 0
        for f in files:
            # unfortunately, we have to do it twice
            if isort.SortImports(f, check=True).incorrectly_sorted:
                fails += 1
                print()
                isort.SortImports(f, show_diff=True)
                print()

        print()
        print('Statistics')
        print('==========')
        print()
        print('%d files failed to pass' % fails)


class cmd_pep8(Command):

    description = 'run pep8'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run(self):

        try:
            import pep8
        except ImportError:
            print(('Cannot import pep8, you forgot to install?\n'
                   'run `pip install pep8` to install.'), file=sys.stderr)
            sys.exit(1)

        p8 = pep8.StyleGuide()

        # do not include code not written in b.py
        p8.options.exclude += EXCLUDE_SCRIPTS
        # ignore four-space indentation error
        p8.options.ignore += ()

        print()
        print('Options')
        print('=======')
        print()
        print('Exclude:', p8.options.exclude)
        print('Ignore :', p8.options.ignore)

        print()
        print('Results')
        print('=======')
        print()
        report = p8.check_files(CHECK_FILES)

        print()
        print('Statistics')
        print('==========')
        print()
        report.print_statistics()
        print('%-7d Total errors and warnings' % report.get_count())


class cmd_pyflakes(Command):

    description = 'run Pyflakes'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run(self):

        try:
            from pyflakes import api
            from pyflakes import reporter as modReporter
        except ImportError:
            print(('Cannot import pyflakes, you forgot to install?\n'
                   'run `pip install pyflakes` to install.'), file=sys.stderr)
            sys.exit(1)

        from os.path import basename

        reporter = modReporter._makeDefaultReporter()

        # monkey patch for exclusion of pathes
        api_iterSourceCode = api.iterSourceCode

        def _iterSourceCode(paths):
            for path in api_iterSourceCode(paths):
                if basename(path) not in EXCLUDE_SCRIPTS:
                    yield path
        api.iterSourceCode = _iterSourceCode

        print()
        print('Options')
        print('=======')
        print()
        print('Exclude:', EXCLUDE_SCRIPTS)

        print()
        print('Results')
        print('=======')
        print()
        warnings = api.checkRecursive(CHECK_FILES, reporter)
        print()
        print('Total warnings: %d' % warnings)


class cmd_pylint(Command):

    description = 'run Pylint'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run(self):

        from glob import glob
        try:
            from pylint import lint
        except ImportError:
            print(('Cannot import pylint, you forgot to install?\n'
                   'run `pip install pylint` to install.'), file=sys.stderr)
            sys.exit(1)

        print()
        print('Options')
        print('=======')
        print()
        print('Exclude:', EXCLUDE_SCRIPTS)

        files = ['setup.py', CLI_script, module_file] + glob('tests/*.py')
        args = [
            '--ignore=%s' % ','.join(EXCLUDE_SCRIPTS),
            '--output-format=colorized',
            '--include-ids=y',
            '--indent-string="  "',
        ] + files
        print()
        lint.Run(args)

# ============================================================================

with codecs.open(module_file, encoding='utf-8') as f:
    meta = dict(
        (k.strip(' _'), eval(v)) for k, v in
        # There will be a '\n', with eval(), it's safe to ignore
        (line.split('=') for line in f if line.startswith('__'))
    )

    # keep these
    meta_keys = ['name', 'description', 'version', 'license', 'url', 'author',
                 'author_email']
    meta = dict([m for m in meta.items() if m[0] in meta_keys])

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Text Processing :: Filters',
]

setup_d = dict(
    name=module_name,
    long_description=long_description,
    cmdclass={
        'isort': cmd_isort,
        'pep8': cmd_pep8,
        'pyflakes': cmd_pyflakes,
        'pylint': cmd_pylint,
        'test': cmd_test,
    },
    classifiers=classifiers,
    py_modules=[module_name],
    scripts=[CLI_script],
    **meta
)

if bdist_wheel:
    setup_d['cmdclass']['bdist_wheel'] = bdist_wheel
if BuildDoc:
    setup_d['cmdclass']['build_sphinx'] = BuildDoc
if UploadDoc:
    setup_d['cmdclass']['upload_sphinx'] = UploadDoc

if __name__ == '__main__':
    setup(**setup_d)
