""" robot-lockable """
from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "unknown"

__pypi_url__ = "https://pypi.python.org/pypi/robot-lockable"
__robot_info__ = get_distribution("robotframework")

from RobotLockable.RobotLockable import RobotLockable  # pylint: disable=wrong-import-position
