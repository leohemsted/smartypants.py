===========
Development
===========

smartypants_ is hosted on Bitbucket, you can clone the repository or file an
issue report from there.

.. _smartypants: https://bitbucket.org/livibetter/smartypants.py


Contributing
============

You are welcome to contribute whatever you can. Coding, documenting,
reporting issues, requesting features, even correcting typos.


Testing
=======

If you want to contribute to the source code, be sure that you check your
modification can pass tests. Normally, if you use Unix-like system, you should
be able to run all tests with::

  make test

It will test DOC8, PEP8, pyflakes, unittest, and package installation::

  make test_isort
  make test_doc8
  make test_pep8
  make test_pyflakes
  make test_test
  make test_setup

.. note:: They will all be tested with both Python 2 and Python 3. You may need
          to override ``PY2_CMD`` and/or ``PY3_CMD``.

If ``make`` isn't available, ``setup.py`` can be used::

  python setup.py isort
  python setup.py pep8
  python setup.py pyflakes
  python setup.py test

For manual package installation test::

  python setup.py sdist
  pip install --user --upgrade dist/smartypants-<x.y.z>.tar.gz


Building
========

Package
-------

You should be able to build the package with either of::

  make

.. note:: ``make`` builds source tarball, zip, and win32 setup.

or::

  python setup.py sdist


Documentation
-------------

You should be able to build the documentation with either of::

  make doc

or::

  python setup.py build_sphinx


Reporting
=========

Please head over to Issues_ and create an issue for a bug report or feature
request.

.. _Issues: https://bitbucket.org/livibetter/smartypants.py/issues
