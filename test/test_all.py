#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy.testing import assert_, assert_equal, assert_almost_equal, assert_raises

from aarchiba_tools import downsample, logspace_exp


def test_downsample_1d():
    assert_almost_equal(downsample([1, 2, 3, 4], 2), [1.5, 3.5])
    assert_almost_equal(downsample([1, 2, 3, 4], 4), [2.5])
    assert_almost_equal(downsample([1, 2, 3, 4], 1), [1, 2, 3, 4])


def test_downsample_raises():
    assert_raises(ValueError, downsample, [1, 2, 3, 4], 3)
    assert_raises(ValueError, downsample, [1, 2, 3, 4], 0)
    assert_raises(ValueError, downsample, [1, 2, 3, 4], -1)

    assert_raises(ValueError, downsample, np.zeros((2, 3)), 1, axis=2)
    assert_raises(ValueError, downsample, np.zeros((2, 3)), 1, axis=-3)


def test_downsample_negative_axes():
    a = np.random.randn(6, 35, 11 * 13)
    assert_almost_equal(downsample(a, 11, axis=2), downsample(a, 11, axis=-1))
    assert_almost_equal(downsample(a, 3, axis=0), downsample(a, 3, axis=-3))


def test_downsample_shape():
    a = np.random.randn(6, 6, 6)
    assert_equal(downsample(a, 3, axis=0).shape, (2, 6, 6))
    assert_equal(downsample(a, 3, axis=1).shape, (6, 2, 6))
    assert_equal(downsample(a, 3, axis=2).shape, (6, 6, 2))
    assert_equal(downsample(a, 3, axis=-3).shape, (2, 6, 6))
    assert_equal(downsample(a, 3, axis=-2).shape, (6, 2, 6))
    assert_equal(downsample(a, 3, axis=-1).shape, (6, 6, 2))


def test_downsample_dimensions():
    a = np.random.randn(6, 6, 6)
    assert_almost_equal(downsample(a, 6, axis=0), a.mean(axis=0)[None, :, :])
    assert_almost_equal(downsample(a, 6, axis=1), a.mean(axis=1)[:, None, :])
    assert_almost_equal(downsample(a, 6, axis=2), a.mean(axis=2)[:, :, None])


def test_logspace_exp_basic():
    assert_almost_equal(logspace_exp(1, 1000, 4), [1, 10, 100, 1000])
