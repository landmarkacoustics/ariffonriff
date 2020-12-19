# Copyright (C) 2020 by Landmark Acoustics LLC
r"""test modules shouldn't need docstrings"""

import struct

import pytest

from ariffonriff import WaveFormatData

pcm16_stereo = WaveFormatData(44100,
                              2,
                              16)
r"""CD-quality stereo sound with 16-bit integer values."""


float32_mono = WaveFormatData(44100,
                              1,
                              32)
r"""32-bit IEEE float mono audio"""


@pytest.mark.parametrize("format_object,"
                         "sample_rate,"
                         "channel_count,"
                         "byte_rate,"
                         "code,",
                         zip([pcm16_stereo, float32_mono],
                             [44100, 44100],
                             [2, 1],
                             [2, 4],
                             [1, 3]))
def test_properties(format_object,
                    sample_rate,
                    channel_count,
                    byte_rate,
                    code):
    r"""Trivial access to internals"""
    bit_rate = 8*byte_rate
    bytes_per_frame = byte_rate * channel_count
    needs_fact_chunk = code != 0x0001

    assert format_object.sample_rate == sample_rate
    assert format_object.channel_count == channel_count
    assert format_object.bit_rate == bit_rate
    assert format_object.byte_rate == byte_rate
    assert format_object.bytes_per_frame == bytes_per_frame
    assert format_object.code == code
    assert format_object.needs_fact_chunk == needs_fact_chunk


@pytest.mark.parametrize("format_object, pack_format, pack_args",
                         zip([pcm16_stereo, float32_mono],
                             ["<IHHIIHH", "<IHHIIHHH"],
                             [(16, 1, 2, 44100, 44100 * 2 * 2, 2 * 2, 16),
                              (18, 3, 1, 44100, 44100 * 1 * 4, 1 * 4, 32, 0)]))
def test_format_chunk(format_object, pack_format, pack_args):
    r"""Check the realized binary representation of the format."""
    should_be = b'fmt ' + struct.pack(pack_format, *pack_args)
    assert format_object.as_wave_format_chunk() == should_be
