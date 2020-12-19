# Copyright (C) 2020 by Landmark Acoustics LLC
r"""screw this object-oriented crap."""

from io import IOBase, SEEK_SET
import struct


def extract_values(bytes_object: bytes,
                   format_string: str,
                   start: int=0) -> tuple:
    r"""Unpack values from a bytes-like object and output position info.

    Parameters
    ----------
    bytes_object : bytes
        The data, in a `bytes` object
    format_string : str
        A string of formats that `struct.unpack` will use to read from the data
    start : int, optional
        The index to start at inside the bytes object.

    Returns
    -------
    values : tuple
        the values asked for by the format string
    start : int
        the starting position of the read
    finish : int
        the final position of the read

    See Also
    --------
    struct.unpack : extracts the values
    struct.calcsize : figures out the length to extract from `format_string`

    """

    finish = start + struct.calcsize(format_string)
    values = struct.unpack(format_string,
                           bytes_object[start:finish])

    if len(values) == 1:
        values = values[0]

    return (
        finish,
        values
    )


def format_stuff_as_bytes(stream: IOBase):
    r"""Extract the boilerplate format header from WAV file

    Parameters
    ----------
    stream : io.BufferedIOBase
        A seekable binary file-like-object

    Returns
    -------
    riff_string : str
        Should be 'RIFF'
    file_size : int
        Should be the number of bytes in the file minus 8
    wave_string : str
        Should be 'WAVE'
    fmt__string : str
        Should be 'fmt '. NOTE THE SPACE
    chunk_size : int
        The size of the format chunk
    format_code : int
        '1' if the data are ints, and '3' if they are floats
    channel_count : int
        The number of channels in the file
    sample_rate : int
        The sample rate of the file
    bytes_per_second : int
        Should be `sample_rate * bytes_per_frame`
    bytes_per_frame : int
        Should be `channel_count * bits_per_sample // 8`
    bits_per_sample : int
        The number of bits in each sample
    extra_info : bytes
        The extra information content, if the format chunk has more data
    next_block_name : str
        The next block name
    next_block_data : bytes
        The next block's contents, unless the next block is of type 'data'.

    """

    if stream.seekable():
        stream.seek(0, SEEK_SET)

    header = stream.peek()

    pos, early_data = extract_values(header,
                                     '<4sI4s4sI')

    pos, format_data = extract_values(header,
                                      '<HHIIHH',
                                      pos)

    size_of_extra_info = 0

    if early_data[-1] > 16:
        pos, size_of_extra_info = extract_values(header,
                                                 '<H',
                                                 pos)

    extra_info = b''
    if size_of_extra_info:
        pos, extra_info = extract_values(header,
                                         f'<{size_of_extra_info}s',
                                         pos)

    pos, (next_block_name, _) = extract_values(header,
                                               '<4sI',
                                               pos)

    next_block_data = b''
    if next_block_name == b'fact':
        pos, next_block_data = extract_values(header,
                                              '<I',
                                              pos)

    return early_data + format_data + (
        extra_info,
        next_block_name,
        next_block_data
    )
