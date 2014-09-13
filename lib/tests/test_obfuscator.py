#!/usr/bin/env python
__author__ = "Timothy McFadden"
__date__ = "08/28/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01"
"""
This is the unit test for obfuscator.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
import obfuscator


class Test(unittest.TestCase):

    def test_obfuscate_xor_string(self):
        data = "testing"
        key, bytes = obfuscator.obfuscate_xor(map(ord, data), minimum_length=40)
        self.assertGreater(key, 0)
        self.assertEqual(len(bytes), 40)

        key, bytes = obfuscator.obfuscate_xor(map(ord, data), key=0x0F, minimum_length=0)
        self.assertEqual(key, 0x0F)
        self.assertEqual(len(bytes), len(data))

        self.assertEqual(ord("t") ^ 0x0F, bytes[0])
        self.assertEqual(ord("g") ^ 0x0F, bytes[-1])

    def test_obfuscate_xor_bytes(self):
        data = [0x01, 0x06, 0xA1]
        key, bytes = obfuscator.obfuscate_xor(data, minimum_length=40)
        self.assertGreater(key, 0)
        self.assertEqual(len(bytes), 40)

        key, bytes = obfuscator.obfuscate_xor(data, key=0x0F, minimum_length=0)
        self.assertEqual(key, 0x0F)
        self.assertEqual(len(bytes), len(data))

        self.assertEqual(0x01 ^ 0x0F, bytes[0])
        self.assertEqual(0xA1 ^ 0x0F, bytes[-1])

    def test_deobfuscate_xor(self):
        key, bytes = 15, [123, 106, 124, 123, 102, 97, 104]  # encoded "testing"

        new_bytes = obfuscator.deobfuscate_xor(key, bytes)
        self.assertEqual("t", chr(new_bytes[0]))
        self.assertEqual("g", chr(new_bytes[-1]))

    def test_obfuscate_offset_string(self):
        data = "testing"
        key, bytes = obfuscator.obfuscate_offset(map(ord, data), minimum_length=40)
        self.assertGreaterEqual(key, 0)
        self.assertEqual(len(bytes), 40)

        key, bytes = obfuscator.obfuscate_offset(map(ord, data), key=0x0F, minimum_length=0)
        self.assertEqual(key, 0x0F)
        self.assertEqual(len(bytes), len(data))

        self.assertEqual(ord("t") + key, bytes[0])
        self.assertEqual(ord("g") + key, bytes[-1])

    def test_obfuscate_offset_bytes(self):
        data = [0x01, 0x06, 0xA1]
        key, bytes = obfuscator.obfuscate_offset(data, minimum_length=40)
        self.assertGreater(key, 0)
        self.assertEqual(len(bytes), 40)

        key, bytes = obfuscator.obfuscate_offset(data, key=0x0F, minimum_length=0)
        self.assertEqual(key, 0x0F)
        self.assertEqual(len(bytes), len(data))

        self.assertEqual(0x01 + 0x0F, bytes[0])
        self.assertEqual(0xA1 + 0x0F, bytes[-1])

    def test_deobfuscate_offset(self):
        key, bytes = 15, [131, 116, 130, 131, 120, 125, 118]  # encoded "testing"

        new_bytes = obfuscator.deobfuscate_offset(key, bytes)
        self.assertEqual("t", chr(new_bytes[0]))
        self.assertEqual("g", chr(new_bytes[-1]))

    def test_get_decoder(self):
        self.assertIs(obfuscator._get_decoder(1), obfuscator.deobfuscate_xor)
        self.assertIs(obfuscator._get_decoder(2), obfuscator.deobfuscate_offset)

    def test_get_encoder_type(self):
        self.assertEqual(obfuscator._get_encoder_type(obfuscator.obfuscate_xor), 1)
        self.assertEqual(obfuscator._get_encoder_type(obfuscator.obfuscate_offset), 2)

    def test_encode_operation(self):
        import operator
        key, orig_bytes = 10, [1, 2, 3, 4]

        for combinator in [operator.xor, operator.add, operator.sub, operator.mul]:
            bytes = obfuscator._encode_operation(orig_bytes, 10, combinator=combinator)
            self.assertEqual(bytes[1], combinator(2, 10))

    def test_decode_operation(self):
        import operator
        key, orig_bytes = 10, [1, 2, 3, 4]

        for combinator in [operator.xor, operator.add, operator.sub, operator.mul]:
            bytes = obfuscator._decode_operation(orig_bytes, 10, combinator=combinator)
            self.assertEqual(bytes[1], combinator(2, 10))

    def test_rot13_encode(self):
        original = map(ord, "test")
        encoded = map(ord, "grfg")

        self.assertEqual((None, encoded), obfuscator.rot13(original, minimum_length=0))
        self.assertEqual((None, encoded), obfuscator.obfuscate_rot13(original, minimum_length=0))

    def test_rot13_decode(self):
        original = map(ord, "test")
        encoded = map(ord, "grfg")

        self.assertEqual((None, original), obfuscator.rot13(encoded, minimum_length=0))
        self.assertEqual(original, obfuscator.deobfuscate_rot13(None, encoded))


if __name__ == '__main__':
    unittest.main()
