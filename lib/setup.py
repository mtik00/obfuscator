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

try:
    import pypandoc
    read_md = lambda f: pypandoc.convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST", file=sys.stderr)
    read_md = lambda f: open(f, 'r').read()


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
        download_url="https://github.com/mtik00/obfuscator/releases/tag/v{}".format(__version__),
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

        long_description=read_md(os.path.join(os.path.dirname(__file__), "..", "README.md"))
    )
