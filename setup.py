#!/usr/bin/env python
"""Setup for the columbia micro-service, part of the Quaerere Platform
"""
import os
import re
import sys

from setuptools import setup
from setuptools.command.install import install

PROJECT_NAME = 'quaerere-columbia-common'
INSTALL_REQUIRES = [
    'marshmallow<3,>=2.19.0',
    'quaerere-base-common',
]
SETUP_REQUIRES = [
    'pytest-runner',
    'Sphinx<2,>=1.8.0',
    'sphinx-rtd-theme',
    'setuptools',
]
TESTS_REQUIRES = [
    'pytest>=4.2.0',
    'pytest-cov>=2.6.0',
    'pytest-flake8',
]


def get_version():
    with open('VERSION') as f:
        return f.readline().strip()


PROJECT_RELEASE = get_version()
PROJECT_VERSION = '.'.join(PROJECT_RELEASE.split('.')[:2])


# Taken from https://circleci.com/blog/continuously-deploying-python-\
# packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        release_regex = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')
        if not release_regex.match(PROJECT_RELEASE):
            sys.exit(0)

        tag = os.getenv('CIRCLE_TAG')

        if tag != 'v' + PROJECT_RELEASE:
            info = "Git tag: {0} does not match the version of this " \
                   "app: {1}".format(tag, PROJECT_RELEASE)
            sys.exit(info)


class WriteRequirementsCommand(install):
    """Writes all package requirements into requirements.txt"""
    description = 'creates requirements.txt'

    def run(self):
        header = '# Generated file, do not edit\n'
        all_requirements = INSTALL_REQUIRES + SETUP_REQUIRES + TESTS_REQUIRES
        all_requirements = [I + '\n' for I in all_requirements]
        all_requirements.insert(0, header)
        with open('requirements.txt', 'w') as fh:
            fh.writelines(all_requirements)


setup(name=PROJECT_NAME,
      version=PROJECT_RELEASE,
      test_suite='tests',
      install_requires=INSTALL_REQUIRES,
      setup_requires=SETUP_REQUIRES,
      tests_require=TESTS_REQUIRES,
      entry_points={
          'distutils.commands': [
              'build_sphinx = sphinx.setup_command:BuildDoc']},
      command_options={
          'build_sphinx': {
              'project': ('setup.py', PROJECT_NAME),
              'version': ('setup.py', PROJECT_VERSION),
              'release': ('setup.py', PROJECT_RELEASE),
              'source_dir': ('setup.py', 'docs'), }, },
      cmdclass={
          'mk_reqs': WriteRequirementsCommand,
          'verify': VerifyVersionCommand, }, )
