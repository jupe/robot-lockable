"""
Robot-Remote library for remote lockable resources
"""

import subprocess
import time
import socket
import tempfile
import sys
import click
from robotremoteserver import RobotRemoteServer
from robot.api import logger
from RobotLockable.Lockable import Lockable


class RemoteLockable:
    """Remote Ring interface for Robot tests
    This provide ring keywords
    """

    def __init__(self, hostname=socket.gethostname(),
                 resource_list_file="resource.json",
                 lock_folder=tempfile.gettempdir()):
        self._lockable = Lockable(hostname=hostname,
                                  resource_list_file=resource_list_file,
                                  lock_folder=lock_folder)
        logger.info('Initialize server')

    #@Lockable.auto_unlock
    def lock(self, requirements=dict(), timeout_s=1000, alloc_time_s=100):
        """
        Lock resource using given arguments
        :param requirements: resource requirements
        :param timeout_s: allocation timeout
        :param alloc_time_s: allocation max time
        :return: resource info object
        """
        return self._lockable.lock(requirements, timeout_s, alloc_time_s).resource_info

    def unlock(self, resource):
        """
        Unlock resource
        :param resource: resource object to be release. Should contains at least `id` -property.
        :return: None
        """
        print('resource:', resource)
        self._lockable.unlock(resource)


def generate_doc(doc):
    """
    Generate remote-library documentation
    :param doc: output filename
    :return: 0 if success.
    """
    cmd = f"python -m robot.libdoc Remote::http://127.0.0.1:8270 {doc}"
    server = subprocess.Popen(("python", __file__), stdout=subprocess.PIPE)
    time.sleep(1)
    gen = subprocess.run(cmd.split())  # pylint: disable=subprocess-run-check
    server.kill()
    return gen.returncode


@click.command()
@click.option('--port', default=8270, help='RemoteLockable server Port')
@click.option('--host', default='127.0.0.1', help='Interface to listen. '
                                                  'Use "0.0.0.0" to get access from external machines')
@click.option('--doc', help='generate documentation. E.g. doc.html or list')
def main(port, host, doc):
    if doc:
        sys.exit(generate_doc(doc))
    RobotRemoteServer(RemoteLockable(), port=port, host=host, allow_remote_stop=False)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
