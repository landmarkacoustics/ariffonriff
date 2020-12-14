# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The basic component of a RIFF file is a chunk

    https://en.wikipedia.org/wiki/Resource_Interchange_File_Format

"""

import struct
from typing import Tuple


class RiffChunk:
    r"""A three-part piece of data that will be read from or written to a file.

    RIFF chunks contain three components:
    1. a four-btye ASCII identifier string
    1. an unsigned, little-endian, 32-bit integer giving the size of the
       contents, in bytes.
    1. the contents of the chunk.

    Parameters
    ----------
    identifier : str
        The code that identifies this type of chunk.
    contents : bytes
        A piece of data that has been processed by `struct.pack`.

    See Also
    --------
    struct : for packing and unpacking abilities

    Examples
    --------
    >>> import struct
    >>> from ariffonriff import RiffChunk
    >>> channels = 1
    >>> bit_rate = 16
    >>> sample_rate = 44100
    >>> format_code = '<HHI'
    >>> databytes = struct.pack('<HHI',
    ...                         channels,
    ...                         bit_rate,
    ...                         sample_rate)
    ...
    >>> chunk = RiffChunk('code',
    ...                   struct.pack(format_code,
    ...                               databytes))
    ...
    >>> chunk.id_code
    b'code'
    >>> chunk.size
    8
    >>> chunk.total_size
    16
    >>> chunk.contents(format_code)
    (1, 16, 44100)
    >>> chunk.to_bytes
    b'code\x10\x00\x00\x00\x01\x00\x10\x00D\xac\x00\x00'

    """

    def __init__(self, identifier, contents):
        self._id = RiffChunk.constrain_id(identifier)
        self._data = contents

    @staticmethod
    def constrain_id(identifier: str) -> bytes:
        r"""RIFF identifier fields must be 4-byte ASCII strings.

        Parameters
        ----------
        identifier : str
            A python string that wil be encoded and, maybe, padded or truncated

        Returns
        -------
        bytes : the first 4 characters of `identifier`, rendered as ASCII bytes

        See Also
        --------
        str.encode : constrains the bytes to be ASCII
        bytes.ljust : pads the bytes with `' '`, if necessary

        Examples
        --------
        >>> RiffChunk.constrain_id('foo')
        b'foo '
        >>> RiffChunk.constrain_id('!#$^@#$^#^!$#')
        b'!#$^'
        >>> RiffChunk.constrain_id('"€" is U+20AC.')
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        UnicodeEncodeError: 'ascii' codec can't encode character '\u20ac' in \
        position 1: ordinal not in range(128)

        """

        result = identifier.encode('ascii')
        if len(result) < 4:
            return result.ljust(4, b' ')

        return result[:4]

    @property
    def id_code(self) -> bytes:
        r"""The identifying code for the RIFF chunk, a 4-btye ASCII string."""

        return self._id

    @property
    def size(self) -> int:
        r"""The number of bytes in the chunk's contents."""
        return len(self._data)

    @property
    def total_size(self) -> int:
        r"""The number of bytes taken up by the entire chunk."""
        return 8 + self.size

    def contents(self, format_code: str) -> Tuple:
        r"""Just the contents part of the chunk, as a tuple.

        Parameters
        ----------
        format_code : str
            `struct.unpack` will use the code to extract the chunk's contents.

        See Also
        --------
        struct.unpack

        """

        return struct.unpack(format_code,
                             self._data)

    def to_bytes(self) -> bytes:
        r"""The entire chunk as a `bytes` object"""
        return struct.pack('<4sI', self.id_code, self.size) + self._data
