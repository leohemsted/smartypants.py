# Copyright (c) 2017 Leo Hemsted
# Licensed under the BSD License, for detailed license information, see COPYING

from __future__ import unicode_literals

import os
import tempfile
import unittest
from subprocess import PIPE, Popen

CLI_SCRIPT = './smartypants'


class TestCLI(unittest.TestCase):

    @staticmethod
    def _p(args, T=None):

        if T:
            T = T.encode()

        stdin = PIPE if T else None
        p = Popen(args, stdin=stdin, stdout=PIPE)
        output = p.communicate(input=T)[0]

        if isinstance(output, bytes):
            output = output.decode()  # Python 3

        return output

    def test_pipe(self):

        T = '"foobar"'
        E = '&#8220;foobar&#8221;'

        output = self._p([CLI_SCRIPT], T)
        self.assertEqual(output, E)

    def test_pipe_attr(self):

        T = """"foo" ``bar''"""

        E = T
        output = self._p([CLI_SCRIPT, '--attr', '0'], T)
        self.assertEqual(output, E)

        E = """"foo" &#8220;bar&#8221;"""
        output = self._p([CLI_SCRIPT, '--attr', 'b'], T)
        self.assertEqual(output, E)

    def test_skipped_elements(self):

        T = '<a>"foo"</a> <b>"bar"</b>'

        E = '<a>&#8220;foo&#8221;</a> <b>&#8220;bar&#8221;</b>'
        output = self._p([CLI_SCRIPT], T)
        self.assertEqual(output, E)

        E = '<a>"foo"</a> <b>&#8220;bar&#8221;</b>'
        output = self._p([CLI_SCRIPT, '--skip', 'a'], T)
        self.assertEqual(output, E)

        E = '<a>&#8220;foo&#8221;</a> <b>"bar"</b>'
        output = self._p([CLI_SCRIPT, '--skip', 'b'], T)
        self.assertEqual(output, E)

        E = T
        output = self._p([CLI_SCRIPT, '--skip', 'a,b'], T)
        self.assertEqual(output, E)

    def test_file(self):

        T = '"foobar"'
        E = '&#8220;foobar&#8221;'

        F = tempfile.mkstemp()[1]
        try:
            with open(F, 'w') as f:
                f.write(T)

            output = self._p([CLI_SCRIPT, F])
        finally:
            os.remove(F)
        self.assertEqual(output, E)
