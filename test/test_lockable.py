# pylint: disable=missing-function-docstring,missing-class-docstring
""" Unit test for lockable pytest plugin """
import unittest
import os
from robot import run
from os.path import join

example_root = join(os.path.abspath(os.path.dirname(__file__)), "../example")


class TestRobotLockable(unittest.TestCase):

    def test_e2e(self):

        exit_code = run(example_root, quiet=True)
        self.assertEqual(exit_code, 0)

    def test_remote_lib(self):
        pass


