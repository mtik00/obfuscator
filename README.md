[![travis ci build state](https://travis-ci.org/mtik00/obfuscator.svg?branch=master)](https://travis-ci.org/mtik00/obfuscator)

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

ofile = obfuscator.file.ObfuscatedFile("test.bin")
data = map(ord, "testing")
ofile.write(data, key=123, minimum_length=32)
self.assertEqual(32, os.path.getsize("test.bin"))
```