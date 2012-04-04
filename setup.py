#!/usr/bin/env python
from distutils.core import setup
from foox.version import get_version

setup(
    name='Foox',
    version=get_version(),
    description='Creates species counterpoint with a genetic algorithm.',
    long_description=open('README.rst').read(),
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='http://packages.python.org/foox',
    packages=['foox'],
    scripts=['bin/foox'],
    license='MIT'
)
