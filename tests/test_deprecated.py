#!/usr/bin/env python
# Copyright (c) 2013 Yu-Jie Lin
# Licensed under the BSD License, for detailed license information, see COPYING

import unittest
import warnings

import smartypants as sps
from smartypants import Attr, smartypants as sp, smartyPants as sP


class SmartyPantsDeprecatedTestCase(unittest.TestCase):

    def test_str_attr(self):

        TEXT = '"foo" -- bar'

        with warnings.catch_warnings(record=True) as w:

            T = sp(TEXT, 'q')
            E = '&#8220;foo&#8221; -- bar'
            self.assertEquals(T, E)

            T = sp(TEXT, 'qd')
            E = '&#8220;foo&#8221; &#8212; bar'
            self.assertEquals(T, E)

            # should only get warning 'once'
            self.assertEquals(len(w), 1)

    def test_smartyPants(self):

        TEXT = '"foo" -- bar'

        with warnings.catch_warnings(record=True) as w:

            T = sP(TEXT, Attr.q)
            E = '&#8220;foo&#8221; -- bar'
            self.assertEquals(T, E)

            self.assertEquals(len(w), 1)

    def test_educateQuotes(self):

        TEXT = '"foo" -- bar'

        with warnings.catch_warnings(record=True) as w:

            T = sps.educateQuotes(TEXT)
            E = '&#8220;foo&#8221; -- bar'
            self.assertEquals(T, E)

            self.assertEquals(len(w), 1)
