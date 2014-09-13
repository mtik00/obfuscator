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

package_data = []

## List contains required packages which needs to be installed during obfuscator installation
install_requires = []

# Read the version from our project
__version__ = None
version_file = os.path.join(os.path.dirname(__file__), 'obfuscator', '__init__.py')
with open(version_file) as f:
    exec(f.read())

if __name__ == '__main__':
    setup(
        name="obfuscator",
        version=__version__,
        description="Data obfuscator package",
        author="Timothy McFadden",
        install_requires=install_requires,
        packages=find_packages(),
        package_data={"obfuscator": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="tests",
    )
