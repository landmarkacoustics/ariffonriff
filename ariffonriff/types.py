# Copyright (C) 2020 by Landmark Acoustics LLC
r"""Some type declarations for consistency."""

from numpy import (
    dtype,
    finfo,
    iinfo
)

le_byte = iinfo(dtype('<u1'))
r"""One-byte unsigned integers, like for 8-bit PCM audio"""

le_unsigned = iinfo(dtype('<u2'))
r"""Two-byte unsigned integers, like for 16-bit PCM audio"""

le_float = finfo(dtype('<f'))
r"""Four-byte floating-point numbers, like for 32-bit float audio"""

le_double = finfo(dtype('<d'))
r"""Eight-byte floating-point numbers, like for 64-bit float audio"""

wave_data_types_by_bit = {
    8 : le_byte,
    16 : le_unsigned,
    32 : le_float,
    64 : le_double,
}
r"""Map the bits per sample to info about the corresponding numpy scalar"""
