# Copyright (c) 2013 Yu-Jie Lin
# Licensed under the BSD License, for detailed license information, see COPYING

from docutils.core import publish_string
import unittest


class SetupTestCase(unittest.TestCase):

    def test_long_description(self):
        """Ensure long description can be generated"""
        with open('README-PyPI.rst') as f:
            long_description = f.read()

        overrides = {
            # raises exception at warning level (2)
            'halt_level': 2,
            'raw_enabled': False,
        }
        html = publish_string(long_description, writer_name='html',
                              settings_overrides=overrides)
        self.assertTrue(html)