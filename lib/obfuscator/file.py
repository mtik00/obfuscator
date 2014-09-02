#!/usr/bin/env python2.7
__author__ = "Timothy McFadden"
__date__ = "08/28/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01"
"""
This module contains a file-level interface for the obfuscation methods.
"""
# Imports ######################################################################
import struct
import random
from . import _get_encoder_type, _get_decoder


class FileHeader(object):
    """The standard header for all obfuscated binary files."""

    size = 4

    def __init__(self):
        self.__CONST_NUM = 0x8343353C

    def __encode(self, var1, var2, var3):
        """Convert the variables into a 32-bit integer."""
        r = (random.randint(0, 1) for _ in xrange(1, 64))

        bytes = [0, 0, 0, 0]
        bytes[0] = (var1 & 0xC0) | r.next() << 5 | (var2 & 0xC0) >> 3 | r.next() << 2 | (var2 & 0x30) >> 4
        bytes[1] = (var1 & 0x30) << 2 | r.next() << 5 | (var2 & 0x0F) << 1 | r.next()
        bytes[2] = (var1 & 0x08) << 4 | r.next() << 6 | (var1 & 0x07) << 3 | r.next() << 2 | r.next() << 1 | r.next()
        bytes[3] = r.next() << 7 | (var3 & 0x04) << 4 | r.next() << 5 | (var3 & 0x03) << 3 | r.next() << 2 | r.next() << 1 | r.next()

        return (bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]) ^ self.__CONST_NUM

    def __decode(self, number):
        """Decode a 32-bit integer into 3 variables."""
        number ^= self.__CONST_NUM
        var1 = var2 = var3 = 0
        bytes = [(number & 0xFF000000) >> 24, (number & 0x00FF0000) >> 16, (number & 0x0000FF00) >> 8, number & 0x000000FF]
        var1 = (bytes[0] & 0xC0) | (bytes[1] & 0xC0) >> 2 | (bytes[2] & 0x80) >> 4 | (bytes[2] & 0x38) >> 3
        var2 = (bytes[0] & 0x18) << 3 | (bytes[0] & 0x03) << 4 | (bytes[1] & 0x1E) >> 1
        var3 = (bytes[3] & 0x40) >> 4 | (bytes[3] & 0x18) >> 3

        return (var1, var2, var3)

    def pack(self, key, data):
        """Create the bytes of the header for the file."""
        from . import obfuscate
        key = key if key is not None else 0
        length = len(data)
        otype = _get_encoder_type(obfuscate)
        number = self.__encode(key, length, otype)
        return struct.pack("!1I", number)

    def unpack(self, barray, key=None):
        """Decode the file header."""
        number = barray[0] << 24 | barray[1] << 16 | barray[2] << 8 | barray[3]
        var1, var2, var3 = self.__decode(number)
        return (key if key else var1, var2, var3)


def write(data, filename, key=None, minimum_length=32):
    """Write the data to a file.

    :param iterable data: The data you want to encode; the length of data must
        be less than 0xFF (header size limitation)
    :param str filename: The path of the file you want to write
    :param int key: The key used during encoding
    :param int minimum_length: The minimum number of bytes to return.  If the
        encoding operation produces fewer bytes that this, random bytes are
        appended to the end of the result so len(bytes) == minimum_length.
    """
    if len(data) > 0xFF:
        raise ValueError("Cannot encode more than 0xFF bytes")

    from . import obfuscate
    _key, bytes = obfuscate(data, key=key, minimum_length=minimum_length - FileHeader.size)

    # Don't store the key in the file if the user passes it in
    # (they'll need to remember it).
    _write_key = _key if key is None else random.randint(0, 256)

    with open(filename, 'wb') as fh:
        fh.write(FileHeader().pack(_write_key, data))
        fh.write(struct.pack('%iB' % len(bytes), *bytes))

    return _key


def read(filename, key=None):
    """This function reads a file written by `write`, and returns the
    deobfuscated data.  This function is not compatible with any other file!

    :param str filename: The name of the file you wish to store the data in
    :param int key: The key used during `write()`.  NOTE: If you passed in a
        key during `write()`, you *must* use the same key here; the key will not
        be stored in the file.  If you let the algorithm choose the key, it is
        stored in the file, and will be used during `read()`.
    """
    with open(filename, 'rb') as fh:
        ba = bytearray(fh.read())

    header = FileHeader()
    (var1, var2, var3) = header.unpack(ba, key=key)
    decoder = _get_decoder(var3)
    ba_data = ba[FileHeader.size:FileHeader.size + var2]
    data = [x for x in ba_data]
    bytes = decoder(var1, data)

    return bytes
