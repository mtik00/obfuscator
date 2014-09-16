#!/usr/bin/env python
'''obfuscator package setup script.'''
from __future__ import print_function
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)


THIS_DIR = os.path.abspath(os.path.dirname(__file__))

# Read the version from our project
__version__ = None
version_file = os.path.join(THIS_DIR, 'obfuscator', '__init__.py')
with open(version_file) as f:
    exec(f.read())


if __name__ == '__main__':
    setup(
        name="obfuscator",
        version=__version__,
        description="Data obfuscator package",
        author="Timothy McFadden",
        url="https://github.com/mtik00/obfuscator",
        download_url="https://github.com/mtik00/obfuscator/releases/download/v{0}/obfuscator-{0}.tar.gz".format(__version__),
        install_requires=[],
        packages=find_packages(),
        package_data={"obfuscator": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="tests",

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Security'
        ],

        long_description=open(os.path.join(THIS_DIR, "README.rst"), 'r').read()
    )
