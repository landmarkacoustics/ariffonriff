# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The actual audio data content for a WAV file."""

from ariffonriff.riff_content import RiffContent


class WaveDataContent(RiffContent):
    r"""Wave formatted data consists of interleaved channels.

    Parameters
    ----------
    sample_count : int
        The number frames or blocks in one channel. Possibly ignored.
    channel_count : int
        The number of channels. Possibly ignored.
    bit_rate : int
        The number of bytes in each sample. Possibly ignored.
    sample_format : str
        A 1-character format symbol for the sample packing. Default is 'I'.

    """

    chunk_id = 'data'

    def __init__(self,
                 sample_count: int,
                 channel_count: int):
        self._length = sample_count
        self._channels = channel_count

    def packing_format(self) -> str:
        r"""See `RiffContent`"""
        return f'<{self._length * self._channels}{self.pack_fmt}'
