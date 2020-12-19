# Copyright (C) 2020 by Landmark Acoustics LLC
r"""__init__ files shouldn't need @@$%@% docstrings!!"""

from ariffonriff.wave_header import WaveHeader
from ariffonriff.riff_chunk import RiffChunk
from ariffonriff.wave_format_data import WaveFormatData
from ariffonriff.write_wave_stream import WriteWaveStream


__all__ = [
    'WaveHeader',
    'RiffChunk',
    'WaveFormatData',
    'WriteWaveStream',
]
