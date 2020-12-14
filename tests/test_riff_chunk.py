# Copyright (C) 2020 by Landmark Acoustics LLC
r"""Test the RiffChunk object"""

import pytest

import struct

from ariffonriff import RiffChunk


@pytest.fixture
def some_bytes():
    return b'314159 is pi'


id_options = [
    ('foo', b'foo '),
    ('wave', b'wave'),
    ('Gewurztraminer', b'Gewu'),
    ('%^#^@', b'%^#^'),
]

@pytest.mark.parametrize('identifier, should_be', id_options)
def test_riff_chunk_identifiers(identifier, should_be, some_bytes):
    chunk = RiffChunk(identifier, some_bytes)
    assert chunk.id_code == should_be


def test_riff_chunk_raises_on_uft8(some_bytes):

    with pytest.raises(UnicodeEncodeError):
        RiffChunk(u'€€€€', some_bytes)


contents_options = [
    ([3.14159, 2.71828, -1.41421], '3f'),
    ([r'gfedcba'.encode('ascii')], '7s'),
    ([u'"€" is U+20AC.'.encode('utf-8')], '16s'),
]

@pytest.mark.parametrize('data, format_code', contents_options)
def test_riff_chunk_on_data(data, format_code):
    if format_code[0] in ['@', '=', '<', '>', '!']:
        format_code = '<' + format_code[1:]

    contents = struct.pack(format_code,
                           *data)

    chunk = RiffChunk('demo',
                      contents)
    assert chunk.size == len(contents)
    assert chunk.total_size == 8 + chunk.size
    assert chunk.contents(format_code) == struct.unpack(format_code,
                                                        contents)
    assert chunk.to_bytes() == struct.pack('<4sI',
                                           b'demo',
                                           len(contents)) + contents
