""" Lockable plugin for pytest """
import socket
import tempfile
from RobotLockable import __version__
from RobotLockable.Lockable import Lockable


class ResourceNotFound(Exception):
    """ Exception raised when resource not found """


class RobotLockable:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, hostname=socket.gethostname(),
                 resource_list_file="resource.json",
                 lock_folder=tempfile.gettempdir()):
        self._lockable = Lockable(hostname=hostname,
                                  resource_list_file=resource_list_file,
                                  lock_folder=lock_folder)

    def lock(self, requirements, timeout_s = 10):
        return self._lockable.lock(requirements, timeout_s)

    def unlock(self, resource):
        print('resource:', resource)
        self._lockable.unlock(resource)
