""" Lockable plugin for robot-framework """
import random
import json
import socket
import os
import sys
import functools
from uuid import uuid1
from time import sleep
from contextlib import contextmanager
import tempfile
from pydash import filter_, merge, count_by
from func_timeout import func_timeout, FunctionTimedOut
from filelock import Timeout, FileLock
from dataclasses import dataclass


@dataclass
class Reservation:
    """
    Reservation dataclass
    """
    requirements: dict
    resource_info: dict
    release: callable
    alloc_id: str = str(uuid1())

    @property
    def id(self):
        """ resource id getter """
        return self.resource_info['id']


class ResourceNotFound(Exception):
    """ Exception raised when resource not found """

    @staticmethod
    def invariant(true, message):
        """ Raise ResourceNotFound if not true with given message"""
        if not true:
            raise ResourceNotFound(message)


class Lockable:
    """
    Base class for Lockable. It handle low-level functionality.
    """
    def __init__(self, hostname=socket.gethostname(),
                 resource_list_file="resources.json",
                 lock_folder=tempfile.gettempdir()):
        self._resources = dict()
        self._hostname = hostname
        self._resource_list = self.read_resources_list(resource_list_file)
        self._lock_folder = lock_folder

    @staticmethod
    def read_resources_list(filename):
        """ Read resources json file """
        with open(filename) as json_file:
            try:
                data = json.load(json_file)
                assert isinstance(data, list), 'data is not an list'
            except (json.decoder.JSONDecodeError, AssertionError) as error:
                raise ValueError(f'invalid resources json file: {error}')
            Lockable.validate_json(data)
        return data

    @staticmethod
    def validate_json(data):
        counts = count_by(data, lambda obj: obj.get('id'))
        no_ids = filter_(counts.keys(), lambda key: key is None)
        if no_ids:
            raise AssertionError('Invalid json, id property is missing')

        duplicates = filter_(counts.keys(), lambda key: counts[key] > 1)
        if duplicates:
            print(duplicates)
            raise AssertionError(f"Invalid json, duplicate ids in {duplicates}")

    @staticmethod
    def parse_requirements(requirements_str):
        """ Parse requirements """
        if isinstance(requirements_str, dict):
            return requirements_str
        if not requirements_str:
            return dict()
        try:
            return json.loads(requirements_str)
        except json.decoder.JSONDecodeError:
            parts = requirements_str.split('&')
            if len(parts) == 0:
                raise ValueError('no requirements given')
            requirements = dict()
            for part in parts:
                try:
                    part.index("=")
                except ValueError:
                    continue
                key, value = part.split('=')
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                requirements[key] = value
            return requirements

    def _try_lock(self, candidate):
        """ Function that tries to lock given candidate resource """
        resource_id = candidate.get("id")
        try:
            lock_file = os.path.join(self._lock_folder, f"{resource_id}.lock")
            print(f"Use lock file: {lock_file}")
            _lockable = FileLock(lock_file)
            _lockable.acquire(timeout=0)
            print(f'Allocated resource: {resource_id}')

            def release():
                nonlocal _lockable
                print(f'Release resource: {resource_id}')
                _lockable.release()
                try:
                    os.remove(lock_file)
                except OSError as error:
                    print(error, file=sys.stderr)

            return candidate, release
        except Timeout:
            raise AssertionError('not success')

    def _lock_some(self, candidates, timeout_s, retry_interval):
        """ Contextmanager that lock some candidate that is free and release it finally """
        print(f'Total match local resources: {len(candidates)}, timeout: {timeout_s}')
        try:
            def doit(candidates_inner):
                while True:
                    for candidate in candidates_inner:
                        try:
                            return self._try_lock(candidate)
                        except AssertionError:
                            pass
                    print('trying to lock after short period')
                    sleep(retry_interval)

            resource, release = func_timeout(timeout_s, doit, args=(candidates,))
            print(f'resource {resource["id"]} allocated ({json.dumps(resource)})')
            return resource, release
        except FunctionTimedOut:
            raise TimeoutError(f'Allocation timeout ({timeout_s}s)')

    def _lock(self, requirements: dict, timeout_s: int, retry_interval=1):
        """ Lock resource """
        local_resources = filter_(self._resource_list, requirements)
        random.shuffle(local_resources)
        ResourceNotFound.invariant(local_resources, "Suitable resource not available")
        resource, release = self._lock_some(local_resources, timeout_s, retry_interval)
        reservation = Reservation(requirements=requirements,
                                  resource_info=resource,
                                  release=release)
        return reservation

    @staticmethod
    def _get_requirements(requirements, hostname):
        """ Generate requirements"""
        print(f'hostname: {hostname}')
        return merge(dict(hostname=hostname, online=True), requirements)

    def lock(self, requirements, timeout_s=1000, alloc_time_s=10):
        requirements = self.parse_requirements(requirements)
        predicate = self._get_requirements(requirements, self._hostname)
        print(f"Use lock folder: {self._lock_folder}")
        print(f"Requirements: {json.dumps(predicate)}")
        print(f"Resource list: {json.dumps(self._resource_list)}")
        reservation = self._lock(predicate, timeout_s)
        self._resources[reservation.id] = reservation
        return reservation

    def unlock(self, resource):
        print('resource:', resource)
        resource_id = resource['id']
        ResourceNotFound.invariant(resource_id in self._resources.keys(), 'resource not locked')
        reservation = self._resources[resource_id]
        del self._resources[resource_id]
        reservation.release()
        '''task = reservation.task
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("main(): cancel_me is cancelled now")
        '''

    @staticmethod
    @contextmanager
    def auto_unlock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            reservation = func(*args, **kwds)
            yield reservation
            reservation.release()
        return wrapper
