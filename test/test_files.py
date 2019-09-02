#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os.path import join
import tempfile
import time
import subprocess
import shutil

import pytest

from aarchiba_tools import ensure_list, need_rerun, write_file_if_changed


@pytest.fixture
def dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def touch(f):
    subprocess.check_call(["touch", f])
    return f


@pytest.fixture(scope="module")
def files():
    dir = tempfile.mkdtemp()
    r = []
    r.append([touch(join(dir, "a%d" % i)) for i in range(3)])
    time.sleep(0.01)
    r.append([touch(join(dir, "b%d" % i)) for i in range(3)])
    time.sleep(1)
    r.append([touch(join(dir, "c%d" % i)) for i in range(3)])
    yield r
    shutil.rmtree(dir)


def test_times_clear(files):
    a, b, c = files
    assert need_rerun(c, a)
    assert not need_rerun(a, c)


def test_non_list(files):
    a, b, c = files
    assert need_rerun(c[0], a)
    assert need_rerun(c[0], a[0])
    assert need_rerun(c, a[0])
    assert not need_rerun(a[0], c)
    assert not need_rerun(a[0], c[0])
    assert not need_rerun(a, c[0])


def test_times_equal(files):
    a, b, c = files
    assert not need_rerun(a[0], a[0])


def test_times_1s(files):
    a, b, c = files
    assert need_rerun(c, b)
    assert not need_rerun(b, c)


@pytest.mark.xfail
def test_times_superclose(files):
    a, b, c = files
    assert need_rerun(a[1], a[0])
    assert not need_rerun(a[0], a[1])


def test_times_close(files):
    a, b, c = files
    assert need_rerun(b, a)
    assert not need_rerun(a, b)


def test_if_newer_string(dir):
    s = "foo\n"
    s2 = "bar\n"
    fn = join(dir, "f")
    with open(fn, "wt") as f:
        f.write(s)
    t = os.path.getmtime(fn)
    time.sleep(0.1)  # might not be enough if OS timestamps are 1s
    write_file_if_changed(fn, s)
    assert os.path.getmtime(fn) == t
    write_file_if_changed(fn, s2)
    assert os.path.getmtime(fn) != t


def test_if_newer_bytestring(dir):
    s = b"foo\n"
    s2 = b"bar\n"
    fn = join(dir, "f")
    with open(fn, "wb") as f:
        f.write(s)
    t = os.path.getmtime(fn)
    time.sleep(0.1)  # might not be enough if OS timestamps are 1s
    write_file_if_changed(fn, s)
    assert os.path.getmtime(fn) == t
    write_file_if_changed(fn, s2)
    assert os.path.getmtime(fn) != t
