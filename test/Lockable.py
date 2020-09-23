import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from RobotLockable.Lockable import Lockable


class LockableTests(TestCase):

    def test_constructor(self):
        with TemporaryDirectory() as tmpdirname:
            list_file = os.path.join(tmpdirname, 'test.json')
            with open(list_file, 'w') as fp:
                fp.write('[]')
            Lockable(hostname='myhost', resource_list_file=list_file, lock_folder=tmpdirname)

    def test_constructor_file_not_found(self):
        with TemporaryDirectory() as tmpdirname:
            list_file = os.path.join(tmpdirname, 'test.json')
            with self.assertRaises(FileNotFoundError):
                Lockable(hostname='myhost', resource_list_file=list_file, lock_folder=tmpdirname)

    def test_invalid_file(self):
        with TemporaryDirectory() as tmpdirname:
            list_file = os.path.join(tmpdirname, 'test.json')
            with open(list_file, 'w') as fp:
                fp.write('[s]')
            with self.assertRaises(ValueError):
                Lockable(hostname='myhost', resource_list_file=list_file, lock_folder=tmpdirname)
