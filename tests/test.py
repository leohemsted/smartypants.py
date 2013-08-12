import doctest
import unittest

import smartypants
from smartypants import smartyPants as sp


class TestSmartypantsAllAttributes(unittest.TestCase):
    # the default attribute is "1", which means "all".

    def test_dates(self):

        self.assertEqual(sp("1440-80's"), "1440-80&#8217;s")
        self.assertEqual(sp("1440-'80s"), "1440-&#8216;80s")
        self.assertEqual(sp("1440---'80s"), "1440&#8211;&#8216;80s")
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

        T = sp(TEXT, 'w')
        E = ('<p>He said "Let\'s write some code." '
             "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
             "is python code.</p>")
        self.assertEqual(T, E)

        T = sp(TEXT, 'qw')
        E = ("<p>He said &#8220;Let&#8217;s write some code.&#8221; "
             "This code here <code>if True:\n\tprint &quot;Okay&quot;</code> "
             "is python code.</p>")
        self.assertEqual(T, E)

    def test_ordinal_numbers(self):

        self.assertEqual(sp("21st century"), "21st century")  # no effect.
        self.assertEqual(sp("3rd"), "3rd")  # no effect.

    def test_educated_quotes(self):

        self.assertEqual(sp('"Isn\'t this fun?"'),
                         '&#8220;Isn&#8217;t this fun?&#8221;')


def load_tests(loader, tests, pattern):

    tests.addTests(doctest.DocTestSuite(smartypants))
    return tests
