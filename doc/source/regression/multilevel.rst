.. _reg-multilevel:

.. currentmodule:: pywt

Multilevel DWT, IDWT and SWT
============================

Multilevel DWT decomposition
----------------------------

>>> import pywt
>>> x = [3, 7, 1, 1, -2, 5, 4, 6]
>>> db1 = pywt.Wavelet('db1')
>>> cA3, cD3, cD2, cD1 = pywt.wavedec(x, db1)
>>> print cA3
[ 8.83883476]
>>> print cD3
[-0.35355339]
>>> print cD2
[ 4.  -3.5]
>>> print cD1
[-2.82842712  0.         -4.94974747 -1.41421356]

>>> pywt.dwt_max_level(len(x), db1)
3

>>> cA2, cD2, cD1 = pywt.wavedec(x, db1, mode='cpd', level=2)


Multilevel IDWT reconstruction
------------------------------

>>> coeffs = pywt.wavedec(x, db1)
>>> print pywt.waverec(coeffs, db1)
[ 3.  7.  1.  1. -2.  5.  4.  6.]


Multilevel SWT decomposition
----------------------------

>>> x = [3, 7, 1, 3, -2, 6, 4, 6]
>>> (cA2, cD2), (cA1, cD1) = pywt.swt(x, db1, level=2)
>>> print cA1
[ 7.07106781  5.65685425  2.82842712  0.70710678  2.82842712  7.07106781
  7.07106781  6.36396103]
>>> print cD1
[-2.82842712  4.24264069 -1.41421356  3.53553391 -5.65685425  1.41421356
 -1.41421356  2.12132034]
>>> print cA2
[  7.    4.5   4.    5.5   7.    9.5  10.    8.5]
>>> print cD2
[ 3.   3.5  0.  -4.5 -3.   0.5  0.   0.5]

>>> [(cA2, cD2)] = pywt.swt(cA1, db1, level=1, start_level=1)
>>> print cA2
[  7.    4.5   4.    5.5   7.    9.5  10.    8.5]
>>> print cD2
[ 3.   3.5  0.  -4.5 -3.   0.5  0.   0.5]

>>> coeffs = pywt.swt(x, db1)
>>> len(coeffs)
3
>>> pywt.swt_max_level(len(x))
3
