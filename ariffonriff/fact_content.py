# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The content of the fact chunk of a WAV file."""

from ariffonriff.riff_content import RiffContent


class FactContent(RiffContent):
    r"""Extra information about the format of non-PCM WAV files.

    Parameters
    ----------
    sample_count : int
        The number of frames or blocks in the file's data.
    channel_count : int, optional
        The number of channels.

    """

    chunk_id = 'fact'
    pack_fmt = 'I'

    def __init__(self, sample_count: int, channel_count: int=1):
        self._length = sample_count
        self._channels = channel_count

    def content_tuple(self) -> tuple:
        r"""See `RiffContent`"""

        return (self._length * self._channels, )
