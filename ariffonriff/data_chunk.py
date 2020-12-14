# Copyright (C) 2020 by Landmark Acoustics LLC
r"""also needs to be refactored."""

from ariffonriff.chunk import Chunk


class DataChunk(Chunk):
    r"""Writes the start of a chunk that describes a WAV file's data.

    Parameters
    ----------
    data_size : int
        The size, in bytes, of the file's sound data.

    """

    def __init__(self,
                 data_size):
        super().__init__('data',
                         data_size)
