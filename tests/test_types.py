# Copyright (C) 2020 by Landmark Acoustics LLC
r"""this might be a docstring, maybe..."""

import numpy as np

from numpy.testing import assert_almost_equal

from ariffonriff.types import (
    le_byte,
    le_unsigned,
    le_float,
    le_double,
)

def test_8_bit_pcm_type():
    r"""Check the features of one-byte integers"""
    assert le_byte.dtype is np.dtype(np.ubyte)
    assert le_byte.min == 0
    assert le_byte.max == 255


def test_16_bit_pcm_type():
    r"""Check the features of two-byte integers"""
    assert le_unsigned.dtype is np.dtype(np.uint16)
    assert le_unsigned.min == 0
    assert le_unsigned.max == 65535


def test_32_bit_ieee_float_type():
    r"""Check the features of 32-bit floats"""
    assert le_float.dtype is np.dtype(np.float32)
    big_num = np.finfo(np.float32).max
    assert_almost_equal(le_float.min, -big_num)
    assert_almost_equal(le_float.max, big_num)


def test_64_bit_ieee_float_type():
    r"""Check the features of 64-bit floats"""
    assert le_double.dtype is np.dtype(np.float64)
    big_num = np.finfo(np.float64).max
    assert_almost_equal(le_double.min, -big_num)
    assert_almost_equal(le_double.max, big_num)
