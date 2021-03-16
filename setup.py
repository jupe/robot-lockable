#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2020 by Jussi Vatjus-Anttila
:license: MIT, see LICENSE for more details.
"""
from setuptools import setup, find_packages


CLASSIFIERS = """
Development Status :: 3 - Alpha
Topic :: Software Development :: Testing
Operating System :: OS Independent
License :: OSI Approved :: Apache Software License
Operating System :: POSIX
Operating System :: Microsoft :: Windows
Operating System :: MacOS :: MacOS X
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
""".strip().splitlines()

setup(
    name='robot-lockable',
    use_scm_version=True,
    packages=find_packages(exclude=['tests']),  # Required
    url='https://github.com/jupe/robot-lockable',
    license='MIT',
    author='Jussi Vatjus-Anttila',
    author_email='jussiva@gmail.com',
    description='Robot Framework plugin for lockable resources',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=CLASSIFIERS,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "robotframework",
        "lockable==0.3.1",
        "click",
        "retry",
        "robotremoteserver",
        "asyncio"
    ],
    entry_points={
        'console_scripts': [
            'robot_lockable = RobotLockable.Remote:main'
        ]
    },
    extras_require={  # Optional
        'dev': ['coverage', 'coveralls', 'mock', 'pylint', 'nose', 'pyinstaller']
    },
    keywords="robot-framework lockable framework resource",
    python_requires=">=3.6",
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jupe/robot-lockable',
        'Source': 'https://github.com/jupe/robot-lockable/',
    }
)
