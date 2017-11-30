# Copyright (c) 2017 Leo Hemsted
# Licensed under the BSD License, for detailed license information, see COPYING

import unittest

from docutils.core import publish_string


class SetupTestCase(unittest.TestCase):

    def test_long_description(self):
        """Ensure long description can be generated"""
        with open('README.rst') as f:
            long_description = f.read()

        overrides = {
            # raises exception at warning level (2)
            'halt_level': 2,
            'raw_enabled': False,
        }
        html = publish_string(long_description, writer_name='html',
                              settings_overrides=overrides)
        self.assertTrue(html)
