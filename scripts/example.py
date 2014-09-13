#!/usr/bin/env python
"""
This script is used to demonstrate usage of the obfuscator library.
"""
# Imports ######################################################################
from __future__ import print_function
import os
import sys
import random
import obfuscator

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "09/02/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def rtn_cont():
    raw_input("\nPress return to continue ")


def encode_string():
    while True:
        text = raw_input("Enter some text to encode: ")

        if not text:
            return True

        minimum = raw_input("Select the minimum number of characters: ")

        if minimum.isdigit():
            minimum = int(minimum)
        else:
            minimum = 0

        key = random.randint(1, 60)

        for encoder in [1, 2, 3]:
            print("function:", obfuscator.FUNC_MAP[encoder][0].__name__)
            key, data = obfuscator.obfuscate(map(ord, text), key=key, encoder=encoder, minimum_length=minimum)
            print("    key:", key)
            print("    data:", data)
            print("    data as string:", ''.join(map(chr, data)))

        rtn_cont()


def decode_data():
    # [122, 108, 45, 103, 114, 107, 103]
    while True:
        print("Enter the byte array to decode, in the form of: [102, 98, 122, 114]")
        text = raw_input("bytes: ")
        key = raw_input("Enter the key used to encode the data: ")

        if not text:
            return True

        if key.isdigit():
            key = int(key)
        else:
            key = 0

        bytes = map(int, text.strip("[]").replace(" ", "").split(","))

        for encoder in [1, 2, 3]:
            print("function:", obfuscator.FUNC_MAP[encoder][1].__name__)
            data = obfuscator.deobfuscate(key, bytes, encoder=encoder)
            print("    key:", key)
            print("    data:", data)
            print("    data as string:", ''.join(map(chr, data)))

        rtn_cont()


def menu():
    clear()

    print("=" * 25)
    print("Obfuscator CLI (" + obfuscator.__version__ + ")")
    print("=" * 25)

    keylist = function_dict.keys()
    keylist.sort()
    for key in keylist:
        print("%2s: %s" % (key, function_dict[key]['text']))

    print("")
    selection = raw_input("Please select a menu item, or 0 to exit: ")

    if len(selection) == 0:
        return True
    elif int(selection) == 0:
        sys.exit()

    return function_dict[int(selection)]['sub']()


function_dict = {
    1: {'sub': encode_string, 'text': "Encode string"},
    2: {'sub': decode_data, 'text': "Decode data"},
}

if __name__ == '__main__':
    while menu():
        pass
