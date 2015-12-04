#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from pip.download import PipSession

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt', session=PipSession())]


setup(
    name='django-helpers',
    version='0.0.3',
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
