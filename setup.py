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
    packages=['foox', 'foox/species'],
    scripts=['bin/foox', 'bin/wordolution'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Artistic Software',
        'Topic :: Education',
        'Topic :: Internet',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
