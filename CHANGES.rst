=======
Changes
=======

.. notes on writing changes

  - use reStructuredText as much as possible, code in backticks or code blocks
  - no period in the end of line
  - lower case, base form, e.g. "add" and "remove" not "added" nor "adds"
  - line wrapping at 80 characters, i.e. max line length is 79 characters
  - use symbols, even though they look same in Sphinx doc

    - "*" for modifications, fixes, or a set of grouped changes
    - "+" for additions
    - "-" for removals

    .. note:: need to group each type into block, if without blank lines to
              separate, Sphinx gives warnings.

    Normally, they should be ordered in and separated by blank lines

    - deprecates

    - removals

    * fixes

    * sets

      - removals

      + additions

    + additions

.. note::

  Releases without timestamps mean they will be released in the future.

  *Development* means it's current changes in development repository.


Releases 1.7 and greater
========================

Release 2.0.0
-------------

Development
-----------

- drop Pyblosxom support

- drop str-type ``attr``

  - use ``Attr.default`` instead of ``default_smartypants_attr``

- drop fooBarXyz functions, such as  ``smartyPants``, ``educateQuotes``,
  and ``processEscapes``

+ add ``Attr.u`` and ``Attr.h`` for Unicode characters and HTML named entities
  outputs, respectively. The ``stupefy_entities`` has become
  ``convert_entities`` to support all three types of conversions. (#6)

* Makefile

  - do not build ``bdist_wininst --plat-name win32`` per
    :pep:`527#bdist-dmg-bdist-msi-and-bdist-wininst`

  + test packages build in ``test_setup`` target

  * rename target ``install_test`` to ``test_setup``


Release 1.8.6: 2014-07-19T11:20:52Z
-----------------------------------

* Makefile

  + add ``LC_ALL=C`` test for locale setting on ``setup.py`` wrt #5

  * change virtualenv invocation method in ``install_test`` target

* fix UnicodeDecodeError on opening ``smartypants.py``, which includes Unicode
  characters, when running ``setup.py`` with Python 3 and specific locales
  (#5, patch by Benoît Monin)


Release 1.8.5: 2014-07-03T01:56:03Z
-----------------------------------

* fix requirement of Wheel, now optional (#4)


Release 1.8.4: 2014-06-29T04:39:59Z
-----------------------------------

+ add missing ``COPYING`` and ``CHANGES.rst`` to package (#3)
+ add ``bdist_wheel`` to the building process for Python Wheel format
+ add ``test_doc8`` target

* fix ``install_test`` on missing of Wheel package
* fix argparse version option breaks CLI on Python 3


Release 1.8.3: 2013-11-08T03:03:43Z
-----------------------------------

* fix ``_tokenize`` can not handle HTML comment properly

  This fix includes pull request #1 with modification for handling
  ``--`` appears in a comment, which makes the comment not a comment

Release 1.8.2: 2013-08-28T11:38:42Z
-----------------------------------

- deprecate fooBarXyz functions, such as ``educateQuotes`` and
  ``processEscapes``

* fix ``---`` being converted in ``educateDashes``

  The Perl doesn't do such, and it's possibly a mistaken in
  version v1.5_1.5 (eed4a8a16f11)

  If you want the same behavior with default attributes, you need to use
  ``Attr.q | Attr.b | Attr.i | Attr.e``

* setup.py

  - add ``build_sphinx`` and ``upload_sphinx`` commands

* Makefile

  - add ``doc`` for documentation generation
  - add ``upload_doc`` for uploading to PyPI
  - add ``clean`` for cleaning up built files

+ add documentation generation

Release 1.8.1: 2013-08-20T02:27:35Z
-----------------------------------

- fix deprecated ``smartyPants`` returns nothing (#2)

+ add test file for deprecated stuff

Release 1.8.0: 2013-08-18T11:47:27Z
-----------------------------------

- deprecate str-type ``attr`` with:

  - redesign attr input with new ``Attr`` object

    - ``"-1"`` now is ``Attr.s`` (``"s"``)

  - ``_str_attr_to_int()`` to handle str-type before the removal

- deprecate function name ``smartyPants``, now ``smartypants``

- remove ``tags_to_skip_regex`` and add ``tags_to_skip`` as a list of
  skipped HTML with a helper function to compile a regular expression

* command-line

  - add ``--version``
  - add ``--skip`` for skipped elements

* add Makefile:

  - ``test_pep8``, ``test_pyflakes``, and ``test_test`` (unittest)
    targets
  - ``install_test`` target for checking package installation

    - ``test`` target for all tests above

+ add ``style``, ``samp``, and ``tt`` to be skipped HTML elements

Release 1.7.1: 2013-08-14T06:45:59Z
-----------------------------------

* fix ``README-PyPI.rst`` missing while installing

Release 1.7.0: 2013-08-14T05:51:20Z
-----------------------------------

- deprecate Pyblosxom support

- remove HBS language translation added in 1.5_1.7.

* fix ``convert_quot`` always enabled

  It was always turned on. To have same effect of previous ``1`` attr,
  equivalent attrs are ``qbdew``. Now ``1`` means ``qbde``

+ add Python 3 support
+ add unittest and checks
+ add CLI script

Releases 1.6
============

The following releases were made by Hao Lian:

Release 1.6.0.3: 2009-04-21
---------------------------

``smartypants.py`` exactly the same as 1.5_1.6

Release 1.6.0.2: 2008-12-20
---------------------------

``smartypants.py`` exactly the same as 1.5_1.6


Releases 1.5
============

The following releases were made by Chad Miller:

Release 1.5_1.7: Fri, 09 Aug 2013 07:34:16 -0400
------------------------------------------------

- Add HBS language translation. Patch by by Vera Djuraskovic from
  Webhostinggeeks.com
- Add Python3 support

Release 1.5_1.6: Fri, 27 Jul 2007 07:06:40 -0400
------------------------------------------------

- Fixed bug where blocks of precious unalterable text was instead
  interpreted.  Thanks to Le Roux and Dirk van Oosterbosch

Release 1.5_1.5: Sat, 13 Aug 2005 15:50:24 -0400
------------------------------------------------

- Fix bogus magical quotation when there is no hint that the
  user wants it, e.g., in "21st century".  Thanks to Nathan Hamblen
- Be smarter about quotes before terminating numbers in an en-dash'ed
  range

Release 1.5_1.4: Thu, 10 Feb 2005 20:24:36 -0500
------------------------------------------------

- Fix a date-processing bug, as reported by jacob childress
- Begin a test-suite for ensuring correct output
- Removed import of "string", since I didn't really need it
  (This was my first every Python program.  Sue me!)

Release 1.5_1.3: Wed, 15 Sep 2004 18:25:58 -0400
------------------------------------------------

- Abort processing if the flavour is in forbidden-list.  Default of
  [ "rss" ]   (Idea of Wolfgang SCHNERRING.)
- Remove stray virgules from en-dashes.  Patch by Wolfgang SCHNERRING

Release 1.5_1.2: Mon, 24 May 2004 08:14:54 -0400
------------------------------------------------

- Some single quotes weren't replaced properly.  Diff-tesuji played
  by Benjamin GEIGER

Release 1.5_1.1: Sun, 14 Mar 2004 14:38:28 -0500
------------------------------------------------

- Support upcoming pyblosxom 0.9 plugin verification feature

Release 1.5_1.0: Tue, 09 Mar 2004 08:08:35 -0500
------------------------------------------------

- Initial release
