# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The actual audio data content for a WAV file."""

from typing import (
    Iterable,
    List,
    )

from ariffonriff.helpers import bits_to_bytes
from ariffonriff.riff_content import RiffContent


class WaveDataContent(RiffContent):
    r"""Wave formatted data consists of interleaved channels.

    Parameters
    ----------
    channels : Iterable, optional
        an iterable of channels to interleave. Overrides the other arguments.
    sample_count : int, optional
        The number frames or blocks in one channel. Possibly ignored.
    channel_count : int, optional
        The number of channels. Possibly ignored.
    bit_rate : int, optional
        The number of bytes in each sample. Possibly ignored.

    """

    chunk_id = 'data'

    def __init__(self, channels: Iterable[List]=None,
                 sample_count: int=None,
                 channel_count: int=None,
                 bit_rate: int=None):

        if channels is not None:
            self._length = min([len(x) for x in channels])
            self._channels = len(channels)
            self._bytes = 1 # need to introspect the iterable's items.
        else:
            self._length = sample_count
            self._channels = channel_count
            self._bytes = bits_to_bytes(bit_rate)

        if self.total_length is None:
            raise ValueError("Incomplete information for Initialization")

    def total_length(self) -> int:
        r"""The number of bytes in the data chunk's content data."""

        return self._length * self._channels * self._bytes

    def packing_format(self) -> str:
        r"""See `RiffContent`"""

        fmt = self.pack_fmt
        if self._add_extension_content():
            fmt += 'H'

        return fmt

