# pylint: disable=missing-function-docstring,missing-class-docstring
""" Unit test for lockable pytest plugin """
import unittest
import os
import subprocess
from contextlib import contextmanager
import requests
from requests.exceptions import ConnectionError, HTTPError
from retry import retry
from robot import run as run_robot
from os.path import join, abspath

root_dir = abspath(join(os.path.dirname(__file__), '..'))
sample_local = abspath(join(root_dir, "example/local.robot"))
sample_remote = abspath(join(root_dir, "example/remote.robot"))
remote_lib = abspath(join(root_dir, 'RobotLockable', 'Remote.py'))
resources_list_file = abspath(join(root_dir, 'example/resource.json'))


@retry((ConnectionError, HTTPError), tries=3, delay=2)
def wait_response(uri):
    print(f'verify uri {uri} returns')
    response = requests.get(uri)
    print(f'uri responses: {response}')


@contextmanager
def remote_server():
    print('spawn remote server')

    process = subprocess.Popen(['python', remote_lib,
                                '--hostname', 'localhost',
                                '--resources_list_file', resources_list_file
                                ])
    wait_response('http://127.0.0.1:8270')
    print('run test against remote server')
    yield process
    # kill remote server
    process.kill()
    process.wait()


class TestRobotLockable(unittest.TestCase):

    def test_local_keywords(self):
        exit_code = run_robot(sample_local, quiet=True, log=None, report=None, output=None)
        self.assertEqual(exit_code, 0)

    def test_remote_lib(self):
        with remote_server():
            exit_code = run_robot(sample_remote, quiet=True, log=None, report=None, output=None)
            self.assertEqual(exit_code, 0)
