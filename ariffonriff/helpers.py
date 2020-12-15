# Copyright (C) 2020 by Landmark Acoustics LLC
r"""Functions that are useful in making RIFF files."""

from math import ceil


def bits_to_bytes(bit_rate: int) -> int:
    r"""Divide by 8 and round up to find the num. of bytes in `bit_rate`.

    Parameters
    ----------
    bit_rate : int
        The bit rate to convert to a byte rate

    Returns
    -------
    int : the number of bytes needed to hold `bit_rate` bits.

    See Also
    --------
    math.round_up : the function that does the rounding.

    """

    return ceil(bit_rate * 0.125)
