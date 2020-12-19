# Copyright (C) 2020 by Landmark Acoustics LLC
r"""The minimal version that I need just needs to write wave files."""

import io
import struct
from typing import Callable

from ariffonriff.wave_format_data import WaveFormatData


class WriteWaveStream:
    r"""Put a stream into a WAV file and then update the header's size fields.

    Parameters
    ----------
    output : seekable file-like object
        This is where the data will be written.
    settings : ariffonriff.WaveFormatData
        Information about how the data are encoded.

    """

    def __init__(self,
                 output,
                 settings: WaveFormatData):
        self._target = output
        self._format = settings
        self._size_fields = []
        self._data_start = None
        self._data_length = 0
        self._sample_count = 0

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.teardown()
        return False

    def _register_size_field(self, callback: Callable, length: int=4):
        self._size_fields.append(
            (
                callback,
                self._target.tell()
            )
        )
        self._write(b'\x00' * length)

    def setup(self):
        r"""Write the WAVE header and register size-sensitive fields.

        """

        self._write(b'RIFF')
        self._register_size_field(self._riff_size)

        self._write(b'WAVE')
        self._write(self._format.as_wave_format_chunk())

        if self._format.needs_fact_chunk:
            self._write(struct.pack('<4sI',
                                    b'fact',
                                    4))
            self._register_size_field(self._fact_size)

        self._write(b'data')
        self._register_size_field(self._data_size)
        self._data_start = self._target.tell()

    def teardown(self):
        r"""Calculate the file size and update size-sensitive fields."""

        data_end = self._target.tell()
        self._data_length = data_end - self._data_start
        self._sample_count = self._data_length // self._format.bytes_per_frame

        for callback, offset in self._size_fields:
            self._seek(offset)
            format_string, value = callback()
            self._write(struct.pack(format_string,
                                    value))

        self._seek(data_end)

    def _seek(self, offset):
        return self._target.seek(offset,
                                 io.SEEK_SET)

    def _write(self, data: bytes):
        self._target.write(data)

    def _riff_size(self):
        pos = self._target.tell()
        file_length = self._target.seek(0,
                                        io.SEEK_END)
        self._seek(pos)

        return ('<I', file_length - 8)

    def _fact_size(self):
        return ('<I', self._format.channel_count * self._sample_count)

    def _data_size(self):
        return ('<I', self._data_length)
