#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from six import string_types, PY3
from logging import info, debug
import time

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


def ensure_list(l):
    """Allow a single string or integer to be treated like a one-element list"""
    if isinstance(l,string_types) or isinstance(l,int):
        l = [l]
    return l

def need_rerun(inputs, outputs):
    """Examine inputs and outputs and return whether a command should be rerun.

    If one of the outputs does not exist, or if the modification date of the
    newest input is newer than the oldest output, return True; else False. The
    idea is to allow make-like behaviour.

    Parameters
    ----------
    inputs : string or list of strings
        A list of filenames that are inputs
    outputs : string or list of strings
        A list of filenames that are outputs

    Returns
    -------
    result : bool
        True if an input is newer.
    """
    inputs = ensure_list(inputs)
    outputs = ensure_list(outputs)

    if len(outputs)==0:
        raise ValueError("No outputs specified")

    io = inputs
    inputs = []
    for i in io:
        if i.startswith("@"):
            for l in open(i[1:]).readlines():
                inputs.append(l.strip())
        else:
            inputs.append(i)

    oldest_out = np.inf
    oldest_out_name = None

    for o in outputs:
        if not os.path.exists(o):
            info("Output %s missing" % o)
            return True
        ot = os.path.getmtime(o)
        if ot<oldest_out:
            oldest_out = ot
            oldest_out_name = o

    for i in inputs:
        if os.path.getmtime(i) > oldest_out:
            info("Input %s newer than %s" % (i,oldest_out_name))
            debug("%s > %s" %
                      (time.ctime(os.path.getmtime(i)),
                        time.ctime(os.path.getmtime(oldest_out_name))))
            return True

    return False

def write_file_if_changed(fname, s):
    """Write the string s to the file fname but only if it's different

    If the file `fname` exists, read it and compare its contents to the
    string `s`; if they differ, write `s` to replace the contents of `fname`.
    This ensures that modification dates don't get updated unnecessarily.
    """

    if PY3 and isinstance(s,str):
        rmode = "rt"
        wmode = "wt"
    else:
        rmode = "rb"
        wmode = "wb"
    if not os.path.exists(fname) or open(fname,rmode).read() != s:
        with open(fname, wmode) as f:
            f.write(s)
