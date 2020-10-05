"""
Locking keywords for robot-framework for local usage
"""
import socket
import tempfile
from lockable import Lockable
from RobotLockable import __version__


class RobotLockable:
    """ RobotFramework Lockable plugin """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, hostname=socket.gethostname(),
                 resource_list_file="resource.json",
                 lock_folder=tempfile.gettempdir()):
        """
        Constructor for RobotLockable local keywords
        :param hostname: optional hostname
        :param resource_list_file: optional resources file
        :param lock_folder: optional lock folder
        """
        self._lockable = Lockable(hostname=hostname,
                                  resource_list_file=resource_list_file,
                                  lock_folder=lock_folder)

    def lock(self, requirements, timeout_s=0):
        """
        Lock resource keyword
        Usage example:
        ```
        # lock DUT type of resource and fail if can't during 1 second
        lock    type=dut    1
        ```
        :param requirements: resource requirements
        :param timeout_s: timeout for allocation
        :return: Resource object
        """
        return self._lockable.lock(requirements, timeout_s).resource_info

    def unlock(self, resource):
        """
        Unlock resource
        :param resource: resource object. Should contains at least 'id' -property
        :return: None
        """
        print('resource:', resource)
        self._lockable.unlock(resource)
