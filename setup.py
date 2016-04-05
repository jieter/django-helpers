#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup

from helpers import __version__ as VERSION

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a v{} -m 'tagging v{}'".format(VERSION, VERSION))
    os.system('git push && git push --tags')
    sys.exit()

requirements_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
requirements = [str(ir.req) for ir in parse_requirements(requirements_filename, session=PipSession())]

setup(
    name='django-helpers-jieter',
    version=VERSION,
    description="""Some Django helpers I share between my projects""",
    author='Jan Pieter Waagmeester',
    author_email='jieter@jieter.nl',
    url='https://github.com/jieter/django-helpers',
    packages=['helpers'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='django helpers',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
