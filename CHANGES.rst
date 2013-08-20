CHANGES
=======

Versions without timestamps mean they are future releases.

2.0.0:
    - drop Pyblosxom support
    - drop str-type ``attr``
        - use ``Attr.default`` instead of ``default_smartypants_attr``
    - drop ``smartyPants()``

development:

1.8.1: 2013-08-20T02:27:35Z

    - fix deprecated ``smartyPants`` returns nothing (#2)
    - add test file for deprecated stuff

1.8.0: 2013-08-18T11:47:27Z
    - command-line
        - add ``--version``
        - add ``--skip`` for skipped elements
    - add Makefile:
        - ``test_pep8``, ``test_pyflakes``, and ``test_test`` (unittest)
          targets
        - ``install_test`` target for checking package installation
        - ``test`` target for all tests above
    - add ``style``, ``samp``, and ``tt`` to be skipped HTML elements
    - remove ``tags_to_skip_regex`` and add ``tags_to_skip`` as a list of
      skipped HTML with a helper function to compile a regular expreesion
    - deprecate str-type ``attr`` with:
        - redesign attr input with new ``Attr`` object
            - ``"-1"`` now is ``Attr.s`` (``"s"``)
        - ``_str_attr_to_int()`` to handle str-type before the removal
    - deprecate function name ``smartyPants``, now ``smartypants``

1.7.1: 2013-08-14T06:45:59Z
    - fix ``README-PyPI.rst`` missing while installing

1.7.0: 2013-08-14T05:51:20Z
    - deprecate Pyblosxom support
    - fix ``convert_quot`` always enabled

      It was always turned on. To have same effect of previous ``1`` attr,
      equivalent attrs are ``qbdew``. Now ``1`` means ``qbde``.

    - add Python 3 support
    - add unittest and checks
    - add CLI script

----

The following releases were made by Hao Lian:

1.6.0.3: 2009-04-21
    - ``smartypants.py`` exactly the same as 1.5_1.6
1.6.0.2: 2008-12-20
    - ``smartypants.py`` exactly the same as 1.5_1.6

----

The following releases were made by Chad Miller:

1.5_1.7: Fri, 09 Aug 2013 07:34:16 -0400
    - Add HBS language translation. Patch by by Vera Djuraskovic from
      Webhostinggeeks.com
    - Add Python3 support.

1.5_1.6: Fri, 27 Jul 2007 07:06:40 -0400
    - Fixed bug where blocks of precious unalterable text was instead
      interpreted.  Thanks to Le Roux and Dirk van Oosterbosch.

1.5_1.5: Sat, 13 Aug 2005 15:50:24 -0400
    - Fix bogus magical quotation when there is no hint that the
      user wants it, e.g., in "21st century".  Thanks to Nathan Hamblen.
    - Be smarter about quotes before terminating numbers in an en-dash'ed
      range.

1.5_1.4: Thu, 10 Feb 2005 20:24:36 -0500
    - Fix a date-processing bug, as reported by jacob childress.
    - Begin a test-suite for ensuring correct output.
    - Removed import of "string", since I didn't really need it.
      (This was my first every Python program.  Sue me!)

1.5_1.3: Wed, 15 Sep 2004 18:25:58 -0400
    - Abort processing if the flavour is in forbidden-list.  Default of
      [ "rss" ]   (Idea of Wolfgang SCHNERRING.)
    - Remove stray virgules from en-dashes.  Patch by Wolfgang SCHNERRING.

1.5_1.2: Mon, 24 May 2004 08:14:54 -0400
    - Some single quotes weren't replaced properly.  Diff-tesuji played
      by Benjamin GEIGER.

1.5_1.1: Sun, 14 Mar 2004 14:38:28 -0500
    - Support upcoming pyblosxom 0.9 plugin verification feature.

1.5_1.0: Tue, 09 Mar 2004 08:08:35 -0500
    - Initial release
