#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

from helpers import __version__ as VERSION

package_name = 'django-helpers-jieter'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('twine upload -r pypi dist/%s-%s.tar.gz' % (package_name, VERSION))
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a v{} -m 'tagging v{}'".format(VERSION, VERSION))
    os.system('git push && git push --tags')
    sys.exit()

setup(
    name=package_name,
    version=VERSION,
    description="""Some Django helpers I share between my projects""",
    author='Jan Pieter Waagmeester',
    author_email='jieter@jieter.nl',
    url='https://github.com/jieter/django-helpers',
    packages=['helpers'],
    include_package_data=True,
    install_requires=[
        'django-braces',
        'django-envelope',
        'isoweek',
        'python-dateutil',
        'pytz'
    ],
    license='MIT',
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
