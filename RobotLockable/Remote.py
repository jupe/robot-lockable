"""
Robot-Remote library for remote lockable resources
"""
import json
import subprocess
import time
import socket
import tempfile
import sys
from datetime import datetime
import click
import logging
from robotremoteserver import RobotRemoteServer
from lockable import Lockable

logger = logging.getLogger('Remote')


def setup_logger(filename):
    global logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if filename:
        fh = logging.FileHandler('remote.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class RemoteLockable:
    """Remote Lockable interface for Robot tests
    This provide general locking keywords
    """

    def __init__(self, hostname=socket.gethostname(),
                 resource_list_file="resource.json",
                 lock_folder=tempfile.gettempdir()):
        logger.info('Initialize server..')
        self._lockable = Lockable(hostname=hostname,
                                  resource_list_file=resource_list_file,
                                  lock_folder=lock_folder)

    def lock(self, requirements, timeout_s=60):
        """
        Lock resource using given arguments
        :param requirements: resource requirements as string or dict
        :param timeout_s: allocation timeout
        :return: resource info object
        """
        info = self._lockable.lock(requirements, timeout_s).resource_info
        logger.info(f'{datetime.now()} resource locked: {json.dumps(info)}')
        return info

    def load_resources_list(self, resources_list):
        """
        Load resources list info
        :
        """
        self._lockable.load_resources_list(resources_list)

    def unlock(self, resource):
        """
        Unlock resource
        :param resource: resource object to be release. Should contains at least `id` -property.
        :return: None
        """
        logger.info(f'{datetime.now()} resource unlocked: {json.dumps(resource)}')
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
@click.option('--hostname', default=socket.gethostname(), help='Hostname')
@click.option('--resources_list_file', default=None, help='Resources list file. Required.')
@click.option('--lock_folder', default='.', help='Lock folder')
@click.option('--doc', help='generate documentation. E.g. doc.html or list')
@click.option('--log', help='Log filename')
# pylint:disable=too-many-arguments
def main(port, host, hostname, resources_list_file, lock_folder, doc, log):
    """ main function for remote plugin """
    if doc:
        sys.exit(generate_doc(doc))
    setup_logger(log)
    remote = RemoteLockable(hostname=hostname, resource_list_file=resources_list_file, lock_folder=lock_folder)
    RobotRemoteServer(remote, port=port, host=host, allow_remote_stop=False)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
