# pylint: disable=missing-function-docstring,missing-class-docstring
""" Unit test for lockable pytest plugin """
import unittest
import os
from threading import Thread
from contextlib import contextmanager
import requests
import subprocess
from requests.exceptions import ConnectionError, HTTPError
from retry import retry
from robot import run as run_robot
from os.path import join, abspath
from RobotLockable.Remote import RemoteLockable, RobotRemoteServer, generate_doc

root_dir = abspath(join(os.path.dirname(__file__), '..'))
sample_local = abspath(join(root_dir, "example/local.robot"))
sample_remote = abspath(join(root_dir, "example/remote.robot"))
remote_lib = abspath(join(root_dir, 'RobotLockable', 'Remote.py'))
resources_list_file = abspath(join(root_dir, 'example/resource.json'))


@retry((ConnectionError, HTTPError), tries=3, delay=2)
def wait_response(uri):
    print(f'verify uri {uri}')
    response = requests.get(uri)
    print(f'uri responses: {response}')


@contextmanager
def remote_server():
    print('spawn remote server')
    remote = RemoteLockable(hostname='localhost', resource_list_file=resources_list_file)
    server = RobotRemoteServer(remote, serve=False, allow_remote_stop=False)
    thread = Thread(target=server.serve)
    thread.start()
    wait_response('http://127.0.0.1:8270')
    print('run test against remote server')
    yield
    # kill remote server
    server.stop()
    thread.join()


class TestRobotLockable(unittest.TestCase):

    def test_local_keywords(self):
        exit_code = run_robot(sample_local, quiet=True, log=None, report=None, output=None)
        self.assertEqual(exit_code, 0)

    def test_remote_lib(self):
        with remote_server():
            exit_code = run_robot(sample_remote, quiet=True, log=None, report=None, output=None)
            self.assertEqual(exit_code, 0)

    def test_doc_gen(self):
        html_file = abspath(join(root_dir, 'api.html'))
        self.assertEqual(generate_doc(html_file), 0)
