#!/usr/bin/env python
"""
This script is used to create the release package.
"""
# Imports ######################################################################
from __future__ import print_function
import os
import sys
import shutil
import argparse
import subprocess

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "09/02/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01"

# Globals ######################################################################
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LIB_DIR = os.path.realpath(os.path.join(THIS_DIR, '..', 'lib'))


def remove_directory(top, remove_top=True):
    '''
    Removes all files and directories, bottom-up.

    @type top: str
    @param top: The top-level directory you want removed
    @type remove_top: bool
    @param remove_top: Whether or not to remove the top directory
    '''
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    if remove_top:
        os.rmdir(top)


if __name__ == '__main__':
    release_dir = os.path.realpath(os.path.join(LIB_DIR, '..', 'release'))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--destdir", help="directory to put the generated zip file", type=str,
        default=release_dir)
    args = parser.parse_args()

    # Read the version from our project
    __version__ = None
    with open(os.path.join(LIB_DIR, 'obfuscator', '__init__.py'), 'rb') as f:
        exec(f.read())

    try:
        subprocess.check_output([sys.executable, 'setup.py', 'sdist', '--formats=gztar'], stderr=subprocess.STDOUT, cwd=LIB_DIR)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise

    # move gztar
    gz_filename, = [x for x in os.listdir(os.path.join(LIB_DIR, 'dist')) if '.tar.gz' in x]
    source = os.path.join(LIB_DIR, 'dist', gz_filename)

    if args.destdir:
        dest = os.path.join(args.destdir, gz_filename)
    else:
        dest = os.path.join(THIS_DIR, gz_filename)
    shutil.move(source, dest)

    # remove left over dirs
    for directory in ['obfuscator.egg-info', 'dist', 'build', 'obfuscator-%s' % __version__]:
        path = os.path.join(LIB_DIR, directory)
        if os.path.exists(path):
            remove_directory(path)
