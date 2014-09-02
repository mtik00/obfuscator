#!/usr/bin/env python2.7
# -*- coding: iso-8859-15 -*-
__author__ = "Timothy McFadden"
__date__ = "08/27/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01.0"
"""
This module contains a simple mechanism for obfuscating a set of data.  Consider
this "security through obscurity".  This module contains no encryption mechanisms!

Example
=======

"""
# Imports ######################################################################
import random
import operator


# Globals ######################################################################
DEFAULT_ENCODER = 1


def _get_decoder(encode_method_type):
    """Convert the method type to the deobfuscation function.

    :param int encode_method_type: The type encoder used (see _get_encoder_type)
    """
    return FUNC_MAP[encode_method_type][1]


def _get_encoder_type(encoder=None):
    """Convert the encoder into an int that can be used for _get_decoder.

    :param encoder: The encoder used to obfuscate the data
    """
    return FUNC_MAP[encoder] if (encoder in FUNC_MAP) else FUNC_MAP[obfuscate_xor]


def _encode_operation(data, key, combinator=operator.xor, minimum_length=0):
    """This function encodes the iterable `data` with the key, and combinator.
    The formula used is `[combinator(x, key) for x in data]`.

    Example
    =======
        >>> bytes = map(ord, "test")
        >>> _encode_operation(bytes, 10, minimum_length=10)
        [126, 111, 121, 126, 187, 140, 174, 172, 128, 42]
        >>>

    :param iterable data: The data you want to encode
    :param int key: The key used during encoding
    :param code combinator: The function used to combine each item of the
        iterable (after possible conversion) and the key
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    bytes = [combinator(x, key) for x in data]
    bytes += [random.randint(0, 255) for x in xrange(minimum_length - len(bytes))]
    return bytes


def _decode_operation(data, key, combinator=operator.xor):
    """This function decodes the iterable `data` with the key and combinator.
    The formula used is `[combinator(x, key) for x in data]`.

    Be sure to use the "opposite" of the operator used to encode.  E.g. encode
    with operator.add, decode with operator.sub.

    Example
    =======
        >>> data = [126, 111, 121, 126]
        >>> decoded = _decode_operation(data, 10)
        >>> decoded
        [116, 101, 115, 116]
        >>> ''.join(map(chr, decoded))
        'test'
        >>>

    :param iterable data: The data you want to decode
    :param int key: The key used during decoding
    :param code combinator: The function used to combine each item of the
        iterable (after possible conversion) and the key
    """
    bytes = [combinator(x, key) for x in data]

    return bytes


def obfuscate(data, key=None, minimum_length=32, encoder=DEFAULT_ENCODER):
    """This function obfuscates the data using the default operation.
    """
    return FUNC_MAP[encoder][0](data, key, minimum_length)


def deobfuscate(key, data, encoder=DEFAULT_ENCODER):
    """This function obfuscates the data using the default operation.
    """
    return FUNC_MAP[encoder][1](key, data)


def obfuscate_xor(data, key=None, minimum_length=32):
    """This function obfuscates the data using an byte-wise XOR operation.

    The formula used is: [x ^ key for x in data]

    :param iterable data: The data you want to obfuscate
    :param int key: The key used for the XOR operation.  By default, the key
        will be a random integer between 1 and 255.
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    key = key if key else random.randint(1, 255)
    bytes = _encode_operation(data, key, combinator=operator.xor, minimum_length=minimum_length)
    return (key, bytes)


def deobfuscate_xor(key, data):
    """This function deobfuscates the data using an byte-wise XOR operation.

    The formula used is: [x ^ key for x in data]

    :param int key: The key used for the XOR operation.
    :param iterable data: The data you want to obfuscate
    """
    return _decode_operation(data, key, combinator=operator.xor)


def obfuscate_offset(data, key=None, minimum_length=32):
    """This function obfuscates the data using an offset operation.

    The formula used is: [x + key for x in data]

    :param iterable data: The data you want to obfuscate
    :param int key: The value used for the offset operation.  By default, the
        value will be a random integer between 40 and 128.
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    key = key if key else random.randint(40, 127)
    bytes = _encode_operation(data, key, combinator=operator.add, minimum_length=minimum_length)
    return (key, bytes)


def deobfuscate_offset(key, data):
    """This function deobfuscates the data using an offset operation.

    The formula used is: [x - key for x in data]

    :param int key: The key used for the offset operation.
    :param iterable data: The data you want to obfuscate
    """
    return _decode_operation(data, key, combinator=operator.sub)


def obfuscate_rot13(data, key=None, minimum_length=32):
    """This function performs a ROT13 encode on the data.  `data` needs
    to be an iterable that contains a representation of str types.  This can be
    either a string of type `str`, or a list of bytes from something like `ord`.

    :param iterable data: The data you want to obfuscate
    :param int key: This value is ignored; it only exists to conform to the other
        methods.
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    return rot13(data, minimum_length)


def deobfuscate_rot13(key, data):
    """This function performs a ROT13 decode of the data.  `data` needs
    to be an iterable that contains a representation of str types.  This can be
    either a string of type `str`, or a list of bytes from something like `ord`.

    :param int key: This value is ignored; it only exists to conform to the other
        methods.
    :param iterable data: The data you want to deobfuscate
    """
    _, bytes = rot13(data, minimum_length=0)
    return bytes


def rot13(data, minimum_length=32):
    """This function performs a ROT13 encode/decode on the data.  `data` needs
    to be an iterable that contains a representation of str types.  This can be
    either a string of type `str`, or a list of bytes from something like `ord`.

    :param iterable data: The data you want to obfuscate
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    import string

    if type(data) is str:
        data = map(ord, data)

    rot13 = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

    def op(x, key):
        return ord(string.translate(chr(x), rot13))

    return (None, _encode_operation(data, 0, combinator=op, minimum_length=minimum_length))


# Setup defaults and maps ######################################################

# Map the encode / decode functions so we can store them in the binary file and
# read them back.  This allows us to read an obfuscated file without knowing the
# obfuscation method used to write the file.
FUNC_MAP = {
    0: [obfuscate, deobfuscate],
    1: [obfuscate_xor, deobfuscate_xor],
    2: [obfuscate_offset, deobfuscate_offset],
    3: [obfuscate_rot13, deobfuscate_rot13],
    obfuscate: 0,
    obfuscate_xor: 1,
    obfuscate_offset: 2,
    obfuscate_rot13: 3
}
