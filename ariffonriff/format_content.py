# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The content of the format chunk of a WAV file."""

import struct

from ariffonriff.helpers import bits_to_bytes
from ariffonriff.riff_content import RiffContent


class FormatContent(RiffContent):
    r"""Describes the format in which the data of a WAV file is stored.

    Parameters
    ----------
    format_code : int
        There are five pre-defined format codes (see notes). Two bytes.
    sample_rate : int
        The number of blocks per second. Four bytes.
    bit_rate : int
        The number of bits per sample. Two bytes.
    channel_count : int
        The number of interleaved samples per block. Two bytes.

    Notes
    -----
    The different possible values for `format_code` follow below. If the data
    are encoded as anything other than PCM then there will be some extra
    information in the format chunk. Right now, the only formats that this
    class supports are 1 and 3.

    - 0x0001 : Pulse Code Modulated (PCM)
    - 0x0003 : floating-point (IEEE float)
    - 0x0006 : 8-bit A-law
    - 0x0007 : 8-bit μ-law
    - 0xFFFE : another format detailed in `sub_format`

    """

    chunk_id = 'fmt '
    pack_fmt = 'HHIIHH'

    def __init__(self, format_code, channel_count, sample_rate, bit_rate):

        if format_code not in [1, 3]:
            raise ValueError('the format code must be either 0x0001 or 0x0003')

        self._code = format_code
        self._channels = channel_count
        self._Hz = sample_rate
        self._bits = bit_rate
        self._byte_rate = bits_to_bytes(bit_rate)

    def packing_format(self) -> str:
        r"""See `RiffContent`"""

        fmt = self.pack_fmt
        if self._add_extension_content():
            fmt += 'H'

        return fmt

    def content_tuple(self) -> tuple:
        r"""See `RiffContent`"""

        tpl = (
            self._code,
            self._channels,
            self._Hz,
            self._Hz * self._byte_rate * self._channels,
            self._byte_rate * self._channels,
            self._bits
        )

        if self._add_extension_content():
            tpl += (0)

        return tpl

    def _add_extension_content(self):
        return self._code != 1

    @classmethod
    def from_bytes(cls, contents: bytes) -> object:
        r"""Extract format data from a little-endian bytes object

        Parameters
        ----------
        contents : bytes
            This should be in the expected format

        Returns
        -------
        FormatContent : a new FormatContent object

        """

        (
            code,
            channels,
            hertz,
            bytes_per_second,
            block_size,
            bit_rate
        ) = struct.unpack('<HHIIHH',
                          contents[:16])

        byte_rate = bits_to_bytes(bit_rate)

        if bytes_per_second != channels * hertz * byte_rate:
            raise ValueError(
                f'The bytes-per-second value is {bytes_per_second}, ' +
                f'but it should be {channels * hertz * byte_rate}.'
            )
        if block_size != channels * byte_rate:
            raise ValueError(
                f'The block size is {block_size}, ' +
                f'but it should be {channels * byte_rate}.'
            )

        return cls(code, channels, hertz, bit_rate)
