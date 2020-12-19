# Copyright (C) 2020 by Landmark Acoustics LLC
r"""Functions that are useful in making RIFF files."""

from math import ceil

import numpy as np


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


def short_tone(frequency: np.float32,
               duration: np.float32,
               sample_rate: np.uint32=44100,
               amplitude: np.float32=0.8):
    r"""A short digital sine wave with constant frequency and amplitude.

    Parameters
    ----------
    frequency : np.float32
        the frequency of the tone in Hz
    duration: np.float32
        the length of the tone in seconds
    sample_rate : np.uint32, optional
        the number of samples per second
    amplitude : np.float32, optional
        the amplitude of the tone, constrained to (0, 1]

    """

    times = np.linspace(0,
                        duration,
                        int(duration * sample_rate))

    amplitude = min(np.abs(amplitude), 1.0)

    return  amplitude * np.sin(2 * np.pi * frequency * times)
