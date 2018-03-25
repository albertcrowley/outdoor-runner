#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from outdoor-runner.outdoor-runnerapp import Outdoor-runnerApp


class TestOutdoor-runnerApp(unittest.TestCase):
    """TestCase for Outdoor-runnerApp.
    """
    def setUp(self):
        self.app = Outdoor-runnerApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'outdoor-runner')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
