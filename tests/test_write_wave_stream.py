# Copyright (C) 2020 by Landmark Acoustics LLC
r"""this docstring intentionally left blank."""

from io import SEEK_SET, SEEK_END
import struct

import numpy as np

import pytest

from ariffonriff import (
    WaveFormatData,
    WriteWaveStream
)

from ariffonriff.helpers import short_tone


cd_format = WaveFormatData(
    44100,
    1,
    16)

tone = np.array(pow(2, 16)*(0.5*short_tone(441, 0.1) + 1),
                dtype=np.dtype('<u2'))


def test_writing_a_permanent_file(tmp_path):
    r"""write some audio to the desktop"""

    with open(tmp_path / "foo.wav", "wb") as fh:
        stylus = WriteWaveStream(fh, cd_format)

        stylus.setup()
        header_size = 4 + 8 + 16 + 8
        assert fh.tell() == header_size + 8
        assert len(stylus._size_fields) == 2
        out_amount = fh.write(tone.data)
        assert out_amount == 4410 * 2

        stylus.teardown()
        assert stylus._data_size()[1] == out_amount
        assert stylus._fact_size()[1] == 4410
        assert stylus._riff_size()[1] == header_size + out_amount


def test_context_manager(tmp_path):
    r"""Can the WriteWaveStream object successfully manage a context?"""

    tmp_file = tmp_path / "bar.wav"

    with open(tmp_file, "w+b") as fh:
        with WriteWaveStream(fh, cd_format):
            data_size = fh.write(tone.data)

        fh.seek(4, SEEK_SET)
        riff_size = struct.unpack('<I',
                                  fh.read(4))[0]
        file_size = fh.seek(0, SEEK_END)

    assert file_size == riff_size + 8
    assert data_size == riff_size - 36
