#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

from itertools import product
from functools import reduce
import operator
import numpy as np
from numpy.testing import (run_module_suite, assert_allclose, assert_,
                           assert_raises)

import pywt


def test_traversing_tree_nd():
    x = np.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, dtype=np.float64)
    wp = pywt.WaveletPacketND(data=x, wavelet='db1', mode='symmetric')

    assert_(np.all(wp.data == x))
    assert_(wp.path == '')
    assert_(wp.level == 0)
    assert_(wp.maxlevel == 3)

    assert_allclose(wp['aa'].data, np.array([[3., 7., 11., 15.]] * 4),
                    rtol=1e-12)
    assert_allclose(wp['da'].data, np.zeros((4, 4)), rtol=1e-12, atol=1e-14)
    assert_allclose(wp['ad'].data, -np.ones((4, 4)), rtol=1e-12, atol=1e-14)
    assert_allclose(wp['dd'].data, np.zeros((4, 4)), rtol=1e-12, atol=1e-14)

    assert_allclose(wp['aa'*2].data, np.array([[10., 26.]] * 2), rtol=1e-12)

    assert_(wp['aa']['aa'].data is wp['aa'*2].data)
    assert_allclose(wp['aa'*3].data, np.array([[36.]]), rtol=1e-12)

    assert_raises(IndexError, lambda: wp['aa'*(wp.maxlevel+1)])
    assert_raises(ValueError, lambda: wp['f'])


def test_accessing_node_atributes_nd():
    x = np.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, dtype=np.float64)
    wp = pywt.WaveletPacketND(data=x, wavelet='db1', mode='symmetric')

    assert_allclose(wp['aa'+'ad'].data, np.zeros((2, 2)) - 4, rtol=1e-12)
    assert_(wp['aa'+'ad'].path == 'aa'+'ad')
    assert_(wp['aa'+'ad'].node_name == 'ad')
    assert_(wp['aa'+'ad'].parent.path == 'aa')

    assert_allclose(wp['aa'+'ad'].parent.data,
                    np.array([[3., 7., 11., 15.]] * 4), rtol=1e-12)
    assert_(wp['aa'+'ad'].level == 2)
    assert_(wp['aa'+'ad'].maxlevel == 3)
    assert_(wp['aa'+'ad'].mode == 'symmetric')


def test_collecting_nodes_nd():
    x = np.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, dtype=np.float64)
    wp = pywt.WaveletPacketND(data=x, wavelet='db1', mode='symmetric')

    assert_(len(wp.get_level(0)) == 1)
    assert_(wp.get_level(0)[0].path == '')

    # First level
    assert_(len(wp.get_level(1)) == 4)
    assert_(
        [node.path for node in wp.get_level(1)] == ['aa', 'ad', 'da', 'dd'])

    # Second and third levels
    for lev in [2, 3]:
        assert_(len(wp.get_level(lev)) == (2**x.ndim)**lev)
        paths = [node.path for node in wp.get_level(lev)]
        expected_paths = [
            reduce(operator.add, p) for
            p in sorted(product(['aa', 'ad', 'da', 'dd'], repeat=lev))]
        assert_(paths == expected_paths)


def test_data_reconstruction_delete_nodes_nd():
    x = np.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, dtype=np.float64)
    wp = pywt.WaveletPacketND(data=x, wavelet='db1', mode='symmetric')

    new_wp = pywt.WaveletPacketND(data=None, wavelet='db1', mode='symmetric',
                                  ndim=x.ndim)
    new_wp['ad'+'da'] = wp['ad'+'da'].data
    new_wp['ad'*2] = wp['ad'+'da'].data
    new_wp['ad'+'dd'] = np.zeros((2, 2), dtype=np.float64)
    new_wp['aa'] = [[3.0, 7.0, 11.0, 15.0]] * 4
    new_wp['dd'] = np.zeros((4, 4), dtype=np.float64)
    new_wp['da'] = wp['da']       # all zeros

    assert_allclose(new_wp.reconstruct(update=False),
                    np.array([[1.5, 1.5, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5]] * 8),
                    rtol=1e-12)

    new_wp['ad'+'aa'] = wp['ad'+'aa'].data
    assert_allclose(new_wp.reconstruct(update=False), x, rtol=1e-12)

    del(new_wp['ad'+'aa'])
    # TypeError on accessing deleted node
    assert_raises(TypeError, lambda: new_wp['ad'+'aa'])

    new_wp['ad'+'aa'] = wp['ad'+'aa'].data
    assert_(new_wp.data is None)

    assert_allclose(new_wp.reconstruct(update=True), x, rtol=1e-12)
    assert_allclose(new_wp.data, x, rtol=1e-12)

    # TODO: decompose=True


if __name__ == '__main__':
    run_module_suite()
