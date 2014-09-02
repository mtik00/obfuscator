#!/usr/bin/env python
'''obfuscator package setup script.'''
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print >>sys.stderr, "ERROR: This package requires setuptools in order to install."
    sys.exit(1)

package_data = []

## List contains required packages which needs to be installed during svt_http installation
install_requires = []

# Read the version from our project
__version__ = None
with open('obfuscator/__init__.py') as f:
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
    )
