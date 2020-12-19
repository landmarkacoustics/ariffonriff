# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The minimal version that I need just needs to write wave files."""

import struct

import numpy as np

from ariffonriff.helpers import bits_to_bytes
from ariffonriff.types import wave_data_types_by_bit

class WaveFormatData:
    r"""The minimum information needed to describe a WAVE file

    There are some defintions that I use consistently across this class. A
    single value that represents one piece of amplitude information is a
    'sample.' A collection of samples from one instant, one sample per channel,
    is a 'frame.' A collection of samples from many frames, all corresponding
    to the same source, is a 'channel.' The number of bits that it takes to
    represent a sample is the 'bit rate.' The manner in which sample values are
    represented is a 'format.' Formats might include 16-bit PCM integers or
    32-bit floating point values.

    Parameters
    ----------
    sample_rate : np.uint32
        The number of frames per second
    channels : np.uint16
        The number of channels
    bit_rate : np.uint16
        The size, in bits, of a single sample value.

    """

    def __init__(self,
                 sample_rate: np.uint32,
                 channels: np.uint16,
                 bit_rate: np.uint16):

        self._sample_rate = sample_rate
        self._n_channels = channels
        self._bits_per_sample = bit_rate
        self._bytes_per_sample = bits_to_bytes(bit_rate)
        self._code = wave_format_code(bit_rate, channels)
        self._data_type = wave_data_types_by_bit[bit_rate]

    @property
    def sample_rate(self) -> np.uint32:
        r"""The number of frames per second in the file's data."""
        return self._sample_rate

    @property
    def channel_count(self) -> np.uint16:
        r"""The number of channels in the file's data."""
        return self._n_channels

    @property
    def bit_rate(self) -> np.uint16:
        r"""The number of bits per sample in the file's data."""
        return self._bits_per_sample

    @property
    def byte_rate(self) -> np.uint16:
        r"""The number of bytes per sample in the file's data."""
        return self._bytes_per_sample

    @property
    def bytes_per_frame(self) -> np.uint16:
        r"""The number of bytes in each frame of data."""
        return self.byte_rate * self.channel_count

    @property
    def code(self) -> np.uint16:
        r"""The code for the data as defined by the WAVE standard."""
        return self._code

    @property
    def needs_fact_chunk(self) -> bool:
        r"""`True` if `code != 1`"""
        return self._code != 1

    @property
    def data_type(self) -> np.dtype:
        r"""The numpy type corresponding to how the file's data are stored."""
        return self._data_type.dtype

    def as_wave_format_chunk(self) -> bytes:
        r"""Output the contents as a format chunk for WAVE."""
        if self.needs_fact_chunk:
            return self.as_other_format_chunk()

        return self.as_int_format_chunk()

    def as_int_format_chunk(self):
        r"""the basic format chunk"""

        return struct.pack('<4sIHHIIHH',
                           b'fmt ',
                           16,
                           self._code,
                           self.channel_count,
                           self.sample_rate,
                           self.sample_rate * self.bytes_per_frame,
                           self.bytes_per_frame,
                           self.bit_rate)

    def as_other_format_chunk(self):
        r"""a format chunk for data that is not PCM integers."""

        chunk = self.as_int_format_chunk()
        return \
            chunk[:4] + \
            struct.pack('<I', 18) + \
            chunk[8:] + \
            struct.pack('<H', 0)

    def __repr__(self):
        return '<WaveFormatData: ' + \
            f'Hz={self.sample_rate} ' + \
            f'bits={self.bit_rate} ' + \
            f'channels={self.channel_count}>'

def wave_format_code(bits_per_sample: int, channels: int) -> int:
    r"""The format code for the WAVE chunk, based on its bitrate and channels

    Parameters
    ----------
    bits_per_sample : int
        The number of bits per sample
    channels : int
        The number of channels in the sample

    Returns
    -------
    int : 1, 3, or 65534

    Examples
    --------
    >>> hex(wave_format_code(8, 1))
    '0x1'
    >>> hex(wave_format_code(32, 2))
    '0x3'
    >>> hex(wave_format_code(16, 10))
    '0xfffe'
    >>> hex(wave_format_code(42, 1))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: the bit rate must be a multiple of 8

    """

    if bits_per_sample % 8:
        raise ValueError("the bit rate must be a multiple of 8")

    if channels < 3:
        if bits_per_sample < 17:
            return 0x0001

        return 0x0003

    return 0xfffe
