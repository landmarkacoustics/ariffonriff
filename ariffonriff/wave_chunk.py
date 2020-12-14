# Copyright (C) 2020 by Landmark Acoustics LLC
r"""Wave chunk class"""

from ariffonriff.chunk import Chunk


class WaveChunk(Chunk):
    r"""Writes the start of a WAVE chunk.

    Parameters
    ----------
    data_size : int
        The size, in bytes, of the file's sound data.

    """

    def __init__(self,
                 data_size):
        super().__init__('RIFF',
                         4 + 24 + 8 + data_size)

    @classmethod
    def format(cls):
        r"""Appends `4s` to the parent class's `format`."""
        return super().format() + '4s'

    def values(self):
        r"""Appends `WAVE` to the parent class's `value`."""
        return super().values() + ('WAVE'.encode('ascii'),)
