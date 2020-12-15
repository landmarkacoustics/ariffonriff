# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The content of a RIFF chunk."""

import struct

from ariffonriff import RiffChunk

class RiffContent:
    r"""A base class for information within a RIFF chunk

    Attributes
    ----------
    chunk_id : str
        a four-character ASCII string that identifies the chunk type
    pack_fmt : str
        an ASCII string describing how to pack the content's data into bytes

    """

    chunk_id = '____'
    pack_fmt = '<'

    def chunk_identifier(self) -> str:
        r"""The id string for the type of chunk that the content describes

        Override this in subclasses!

        Returns
        -------
        str : a four-character ASCII string

        """

        return self.chunk_id

    def packing_format(self) -> str:
        r"""The format string for packing the content's data.

        Override this in subclasses!

        Returns
        -------
        str : a series of codes for the values in `self.content`

        See Also
        --------
        struct.pack

        """

        return self.pack_fmt

    def content_tuple(self) -> tuple:
        r"""The data, ordered to match with `packing_format`.

        Override this in subclasses!

        Returns
        -------
        tuple : each item in the content's data.

        """

        return ()

    @classmethod
    def from_bytes(cls, contents: bytes):
        r"""Extract fact data from a little-endian bytes object

        This may not need to be overridden

        Parameters
        ----------
        contents : bytes
            This should be in the expected format

        Returns
        -------
        FactContent : a new FactContent object

        """

        return cls(struct.unpack(cls.packing_format(),
                                 contents))

    def to_bytes(self) -> bytes:
        r"""Encode the information as a little-endian bytes object.

        Returns
        -------
        bytes : the information that a WAV file needs in a 'fmt ' chunk

        """

        return struct.pack(self.packing_format(),
                           *self.content_tuple())

    def as_riff_chunk(self) -> RiffChunk:
        r"""Encode the fact information as a RIFF chunk."""

        return RiffChunk(self.chunk_identifier(),
                         self.to_bytes)
