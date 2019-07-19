#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


def downsample(a, factor, axis=-1, func=np.mean):
    """Return the original array downsampled along a particular axis.

    Groups the specified axis into blocks of size `factor` and applies
    the provided `func` (by default the mean, but sum, product and
    maxiumum are sensible too) to the axis of blocks.

    Parameters
    ----------
    a : array_like
        The array to be manipulated.
    factor : int
        The factor by which to downsample the array. The relevant axis
        should have a length exactly divisible by factor.
    axis : int, optional
        The axis to apply the operation to.
    func : callable
        The function to apply. Should accept an array as input and an
        axis argument; will be called with a newly-created axis of length
        factor, and it should return a result with this axis removed.

    Returns
    -------
    ad : array type based on type of a
        The axis specified will have been reduced by a factor `factor`
        but will still be part of the shape even if it has length 1.
    """
    a = np.asanyarray(a)
    s = np.shape(a)
    if axis<0:
        axis += len(s)
    if axis<0 or axis>=len(s):
        raise ValueError("Input array has only %d dimensions" % len(s))
    if factor<=0:
        raise ValueError("Cannot downsample array by factor %s" % factor)
    n = s[axis]
    if n%factor != 0:
        raise ValueError("Axis length %d not divisible by factor %d"
                             % (n,factor))
    ns = s[:axis]+(n//factor,factor)+s[axis+1:]
    ar = np.reshape(a,ns)
    return func(ar, axis=axis+1)

def logspace_exp(start, stop, num=50, endpoint=True):
    """Return logarithmically spaced values between the endpoints.

    Parameters
    ----------
    start : float
        Start value. Should be nonzero.
    stop : float
        Stop value. Should be nonzero and have the same sign as start.
    num : int, optional
        Number of points to generate.
    endpoint : bool, optional
        Whether to include the endpoint.

    Returns
    -------
    samples : ndarray
        There are `num` samples in the closed or open (depending on
        `endpoint`) interval between `start` and `stop`. Their logarithms
        are spaced equally between the logarithms of `start` and `stop`.

    Results will always be of dtype float.
    """
    if start==0 or stop==0:
        raise ValueError("start and stop values must be nonzero")
    if start<0:
        s = -1
        start = -start
        stop = -stop
    else:
        s = 1
    if stop<0:
        raise ValueError("start and stop values must have the same sign")

    return s*np.exp(np.linspace(np.log(start), np.log(stop),
                            num=num, endpoint=endpoint, dtype=float))
