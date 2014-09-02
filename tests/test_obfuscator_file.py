#!/usr/bin/env python2.7
__author__ = "Timothy McFadden"
__date__ = "08/28/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.01"
"""
This is the unit test for obfuscator.file.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
import obfuscator.file


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (fh, Test.testfile_path) = tempfile.mkstemp()
        os.close(fh)

    @classmethod
    def tearDownClass(cls):
        try:
            os.unlink(Test.testfile_path)
        except:
            print "WARNING: couldn't delete [%s]" % Test.testfile_path

    def test_01_write_string(self):
        data = map(ord, "testing")
        key = obfuscator.file.write(data, Test.testfile_path, key=123, minimum_length=32)
        self.assertEqual(32, os.path.getsize(Test.testfile_path))
        self.assertGreater(key, 0)

    def test_02_read_string(self):
        data = obfuscator.file.read(Test.testfile_path, key=123)
        read_string = ''.join(map(chr, data))
        self.assertEqual("testing", read_string)
        self.assertEqual(chr(data[0]), "t")
        self.assertEqual(chr(data[-1]), "g")

    def test_03_read_string_wrong_key(self):
        data = obfuscator.file.read(Test.testfile_path)
        read_string = ''.join(map(chr, data))
        self.assertNotEqual("testing", read_string)
        self.assertNotEqual(chr(data[0]), "t")
        self.assertNotEqual(chr(data[-1]), "g")

    def test_04_write_bytes(self):
        data = [1, 2, 3, 4]
        key = obfuscator.file.write(data, Test.testfile_path, minimum_length=0)
        self.assertEqual(len(data) + obfuscator.file.FileHeader.size, os.path.getsize(Test.testfile_path))
        self.assertGreater(key, 0)

    def test_05_read_bytes(self):
        data = obfuscator.file.read(Test.testfile_path)
        self.assertEqual([1, 2, 3, 4], data)

    def test_06_write_rot13_string(self):
        data = map(ord, "testing")
        obfuscator.file.write(data, Test.testfile_path, minimum_length=0)
        self.assertEqual(len(data) + obfuscator.file.FileHeader.size, os.path.getsize(Test.testfile_path))

    def test_07_read_rot13_string(self):
        data = obfuscator.file.read(Test.testfile_path)
        read_string = ''.join(map(chr, data))
        self.assertEqual("testing", read_string)


if __name__ == '__main__':
    unittest.main()
