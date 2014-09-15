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
        url="https://github.com/mtik00/obfuscator",
        install_requires=[],
        packages=find_packages(),
        package_data={"obfuscator": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="tests",

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'License :: OSI Approved :: MIT License',
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

        long_description="""\
Introduction
============

Obfuscator is a Python package used to obfuscate a set of data (e.g. bytes).  It
provides **no** encryption!  It's strictly a "security through obscurity" tool,
with limited usefulness.  You have been warned!

Documentation
=============

Documentation is hosted on readthedocs: [obfuscator.readthedocs.org](http://obfuscator.readthedocs.org/en/latest/)

Install
=======
Download the tarball and install with `pip install <package>`.

Usage
=====
See the unit tests for more in-depth examples.  Here are the basics:

```python
import obfuscator
original_bytes = map(ord, "testing")
_key, obfuscated_bytes = obfuscator.obfuscate_xor(original_bytes, key=0x66)
deobfuscated_bytes = obfuscator.deobfuscate_xor(key=0x66, data=obfuscated_bytes)
assert original_bytes == deobfuscated_bytes
```
"""
    )
