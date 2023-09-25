#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Leo Hemsted
# Licensed under the BSD License, for detailed license information, see COPYING

import doctest
import unittest
from time import time

import smartypants
from smartypants import smartypants as sp
from smartypants import Attr


class SmartyPantsTestCase(unittest.TestCase):

    def test_change_default_attr(self):

        TEXT = '"foo" -- bar'

        attr = Attr.q
        Attr.default = attr
        self.assertEqual(Attr.default, attr)

        T = sp(TEXT)
        E = '&#8220;foo&#8221; -- bar'
        self.assertEqual(T, E)

        attr = Attr.q | Attr.d
        Attr.default = attr
        self.assertEqual(Attr.default, attr)

        T = sp(TEXT)
        E = '&#8220;foo&#8221; &#8212; bar'
        self.assertEqual(T, E)

    def test_dates(self):

        self.assertEqual(sp("1440-80's"), "1440-80&#8217;s")
        self.assertEqual(sp("1440-'80s"), "1440-&#8216;80s")
        self.assertEqual(sp("1440--'80s"), "1440&#8212;&#8216;80s")
        self.assertEqual(sp("1960s"), "1960s")  # no effect.
        self.assertEqual(sp("1960's"), "1960&#8217;s")
        self.assertEqual(sp("one two '60s"), "one two &#8216;60s")
        self.assertEqual(sp("'60s"), "&#8216;60s")

    def test_skip_tags(self):

        T = sp('''<script type="text/javascript">
<!--
var href = "http://www.google.com";
var linktext = "google";
document.write('<a href="' + href + '">' + linktext + "</a>");
//-->
</script>''')
        E = '''<script type="text/javascript">
<!--
var href = "http://www.google.com";
var linktext = "google";
document.write('<a href="' + href + '">' + linktext + "</a>");
//-->
</script>'''
        self.assertEqual(T, E)

    def test_convert_quot(self):

        TEXT = (
            "<p>He said &quot;Let's write some code.&quot; "
            "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
            "is python code.</p>")

        T = sp(TEXT)
        E = ("<p>He said &quot;Let&#8217;s write some code.&quot; "
             "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
             "is python code.</p>")
        self.assertEqual(T, E)

        T = sp(TEXT, Attr.w)
        E = ('<p>He said "Let\'s write some code." '
             "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
             "is python code.</p>")
        self.assertEqual(T, E)

        T = sp(TEXT, Attr.q | Attr.w)
        E = ("<p>He said &#8220;Let&#8217;s write some code.&#8221; "
             "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
             "is python code.</p>")
        self.assertEqual(T, E)

    def test_comments(self):

        self.assertEqual(sp("--"), "&#8212;")
        self.assertEqual(sp("-->"), "&#8212;>")
        self.assertEqual(sp("-- \t  >"), "&#8212; \t  >")

        TEXT = '<!-- "foo" --> blah--blah <!-- "bar" -->'
        T = sp(TEXT)
        E = '<!-- "foo" --> blah&#8212;blah <!-- "bar" -->'
        self.assertEqual(T, E)

        TEXT = (
            '<p>foo -- "bar"<!-- foo-bar\n'
            '<p>blah "this"</p>\n'
            '-->\n'
            '</p>'
        )

        T = sp(TEXT)
        E = (
            '<p>foo &#8212; &#8220;bar&#8221;<!-- foo-bar\n'
            '<p>blah "this"</p>\n'
            '-->\n'
            '</p>'
        )
        self.assertEqual(T, E)

        # nothing should be converted
        for TEXT in ('<!-- comment -->',
                     '<!-- <li>Fee-fi-of-fum</li> -->',
                     '<!-- "foo" --> <!-- "bar" -->'):
            self.assertEqual(sp(TEXT), TEXT)

        # not comments
        self.assertEqual(sp('<!-- -- -->'), '<!&#8212; &#8212; &#8212;>')
        self.assertEqual(sp('<!-- -- -- \t >'),
                         '<!&#8212; &#8212; &#8212; \t >')

    def test_ordinal_numbers(self):

        self.assertEqual(sp("21st century"), "21st century")  # no effect.
        self.assertEqual(sp("3rd"), "3rd")  # no effect.

    def test_educated_quotes(self):

        self.assertEqual(sp('"Isn\'t this fun?"'),
                         '&#8220;Isn&#8217;t this fun?&#8221;')

    def test_convert_entities(self):

        self.assertEqual(sp('"quote here"', Attr.set1 | Attr.u),
                         '“quote here”')
        self.assertEqual(sp('"quote&ndash;here"', Attr.set1 | Attr.u),
                         '“quote&ndash;here”')

        self.assertEqual(sp('"quote here"', Attr.set1 | Attr.h),
                         '&ldquo;quote here&rdquo;')

        self.assertEqual(sp('"quote here"', Attr.set1 | Attr.s),
                         '"quote here"')

    def test_incredibly_long_string(self):
        # make sure it doesn't take too long with a long string
        start = time()

        sp("a" * 10000)

        end = time()

        self.assertLess(end - start, 0.2)


def load_tests(loader, tests, pattern):

    tests.addTests(doctest.DocTestSuite(smartypants))
    return tests
