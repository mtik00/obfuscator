#!/usr/bin/env python
"""
This module contains a file-level interface for the XOR obfuscation methods.
"""
__author__ = "Timothy McFadden"
__date__ = "08/28/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "1.0.4"
# Imports ######################################################################
import sys
import struct
import random
from . import _get_encoder_type, _get_decoder

if sys.version_info.major < 3:
    def next(iterator):
        return getattr(iterator, "next")()
elif sys.version_info.major > 2:
    xrange = range


class ObfuscatedFile(object):
    """
    :param str filename: The path of the file you want to read/write.

    This class represents an obfuscated data file.  You can use this to store
    some-what sensitive information inside a file.  The documentation for some of
    the functions is purposely light.

    Example #1 - Storing a string::

        >>> from obfuscator.file import ObfuscatedFile
        >>> of = ObfuscatedFile('data.bin')
        >>> bytes = map(ord, "my string")
        >>> of.write(bytes)  # data.bin is 32 bytes long
        86  # The random key used for encoding; stored in the file
        >>> read_bytes = of.read()
        >>> read_bytes
        [109L, 121L, 32L, 115L, 116L, 114L, 105L, 110L, 103L]
        >>> ''.join(map(chr, read_bytes))
        'my string'

    Example #2 - Storing a string with known key::

        >>> from obfuscator.file import ObfuscatedFile
        >>> of = ObfuscatedFile('data.bin')
        >>> bytes = map(ord, "my string")
        >>> my_key = 0xCF
        >>> of.write(bytes, my_key)  # data.bin is 32 bytes long
        207
        >>> read_bytes = of.read()  # Notice how we didn't use a key
        >>> ''.join(map(chr, read_bytes))
        ',8a253(/&'
        >>> # The string is wrong because the key is not stored in the file
        >>> read_bytes = of.read(key=my_key)
        >>> ''.join(map(chr, read_bytes))
        'my string'
        >>>

    """

    size = 5  # Number of bytes in the header

    def __init__(self, filename):
        """
        :param str filename: The path of the file you want to read/write.
        """
        self.__CONST_NUM = 0x8343353C
        self.__CONST_NUMS = [0x00, 0x9C, 0x38, 0x34, 0x42, 0x4F, 0x39]
        self.filename = filename

    def __encode(self, var1, var2, var3, var4=None):
        """Convert the variables into 2 32-bit integers."""
        s = var4 if var4 is not None else random.randint(1, 6)

        bytes = [0, 0, 0, 0, 0]
        r = (random.randint(0, 1) for _ in xrange(1, 64))
        bytes[0] = (var1 & 0xC0) | next(r) << 5 | (var2 & 0xC0) >> 3 | next(r) << 2 | (var2 & 0x30) >> 4
        bytes[1] = (var1 & 0x30) << 2 | next(r) << 5 | (var2 & 0x0F) << 1 | next(r)
        bytes[2] = (var1 & 0x08) << 4 | next(r) << 6 | (var1 & 0x07) << 3 | next(r) << 2 | next(r) << 1 | next(r)
        bytes[3] = next(r) << 7 | (var3 & 0x04) << 4 | next(r) << 5 | (var3 & 0x03) << 3 | next(r) << 2 | next(r) << 1 | next(r)
        bytes[4] = next(r) << 7 | next(r) << 6 | (s & 4) << 3 | next(r) | (s & 3) << 2 | next(r) << 1 | next(r)

        return (
            (bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]) ^ self.__CONST_NUM,
            (bytes[4] ^ self.__CONST_NUM) & 0xFF)

    def __decode(self, numbers):
        """Convert 2 32-bit integers into 4 variables."""
        number1, number2 = numbers
        number1 ^= self.__CONST_NUM
        number2 ^= self.__CONST_NUM
        var1 = var2 = var3 = var4 = 0
        bytes = [
            (number1 & 0xFF000000) >> 24,
            (number1 & 0x00FF0000) >> 16,
            (number1 & 0x0000FF00) >> 8,
            number1 & 0x000000FF,
            number2 & 0x000000FF]

        var1 = (bytes[0] & 0xC0) | (bytes[1] & 0xC0) >> 2 | (bytes[2] & 0x80) >> 4 | (bytes[2] & 0x38) >> 3
        var2 = (bytes[0] & 0x18) << 3 | (bytes[0] & 0x03) << 4 | (bytes[1] & 0x1E) >> 1
        var3 = (bytes[3] & 0x40) >> 4 | (bytes[3] & 0x18) >> 3
        var4 = (bytes[4] & 0x20) >> 3 | (bytes[4] & 0x0C) >> 2

        return (var1, var2, var3, var4)

    def _encode_to_numbers(self, var1, data):
        from . import obfuscate
        var1 = var1 if var1 is not None else 0
        var2 = len(data)
        var3 = _get_encoder_type(obfuscate)
        return self.__encode(var1, var2, var3)

    def _pack_header(self, numbers):
        """Create the bytes of the header for the file."""
        return struct.pack("!1I1B", *numbers)

    def _unpack_header(self, barray, key=None):
        """Decode the file header."""
        numbers = (barray[0] << 24 | barray[1] << 16 | barray[2] << 8 | barray[3], barray[4])
        var1, var2, var3, var4 = self.__decode(numbers)
        return (key if key else var1, var2, var3, var4)

    def read(self, key=None):
        """This function reads a file written by `write`, and returns the
        deobfuscated data.

        :param int key: The key used during `write()`.  NOTE: If you passed in a
            key during `write()`, you *must* use the same key here; the key will not
            be stored in the file.  If you let the algorithm choose the key, it is
            stored in the file, and will be used during `read()`.
        """
        with open(self.filename, 'rb') as fh:
            ba = bytearray(fh.read())

        (var1, var2, var3, var4) = self._unpack_header(ba, key=key)
        decoder = _get_decoder(var3)
        ba_data = ba[self.size:self.size + var2]
        data = [x ^ self.__CONST_NUMS[var4] for x in ba_data]
        bytes = decoder(var1, data)

        return bytes

    def write(self, data, key=None, minimum_length=32):
        """Write the data to a file.

        :param iterable data: The data you want to encode; the length of data must
            be less than 0xFF (header size limitation)
        :param int key: The key used during encoding
        :param int minimum_length: The minimum number of bytes to write.  If the
            encoding operation produces fewer bytes that this, random bytes are
            appended to the end of the result so len(bytes) == minimum_length.
        """
        if len(data) > 0xFF:
            raise ValueError("Cannot encode more than 0xFF bytes")

        from . import obfuscate
        _key, bytes = obfuscate(data, key=key, minimum_length=minimum_length - self.size)

        # Don't store the key in the file if the user passes it in
        # (they'll need to remember it).
        _write_key = _key if key is None else random.randint(1, 255)

        numbers = self._encode_to_numbers(_write_key, data)
        _, _, _, var4 = self.__decode(numbers)
        bytes = [x ^ self.__CONST_NUMS[var4] for x in bytes]
        with open(self.filename, 'wb') as fh:
            fh.write(self._pack_header(numbers))
            fh.write(struct.pack('%iB' % len(bytes), *bytes))

        return _key

if __name__ == '__main__':
    if "decode-str" in sys.argv:
        path, key = sys.argv[2:4]
        ofile = ObfuscatedFile(path)
        bytes = ofile.read(int(key))
        print "".join([chr(x) for x in bytes])
    elif "encode-str" in sys.argv:
        path, key, string = sys.argv[2:5]
        ofile = ObfuscatedFile(path)
        bytes = map(ord, string)
        print bytes
        ofile.write(bytes, int(key))
    else:
        print("Usage:")
        print("\tpython -m obfuscator.file encode-str <path-to-file> <key> \"string to encode\"")
        print("\tpython -m obfuscator.file decode-str <path-to-file> <key>")
