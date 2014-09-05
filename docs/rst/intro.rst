Introduction
============

Obfuscator is a Python package used to obfuscate a set of data (e.g. bytes).  It
provides **no** encryption!  It's strictly a "security through obscurity" tool,
with limited usefulness.  You have been warned!

The project is hosted on GitHub at https://github.com/mtik00/obfuscator

Install
=======
Download the `latest release tarball <https://github.com/mtik00/obfuscator/releases/latest>`_ and install with `pip install <package>`.

Usage
=====
See the unit tests for more in-depth examples.  Here are the basics:

.. code:: python

    import obfuscator
    original_bytes = map(ord, "testing")
    _key, obfuscated_bytes = obfuscator.obfuscate_xor(original_bytes, key=0x66)
    deobfuscated_bytes = obfuscator.deobfuscate_xor(key=0x66, data=obfuscated_bytes)
    assert original_bytes == deobfuscated_bytes
