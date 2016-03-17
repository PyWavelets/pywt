#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

from numpy.testing import (run_module_suite, assert_almost_equal,
                           assert_allclose)
import numpy as np
import pywt


def ref_gaus(LB,UB,N,num):
    X = np.linspace(LB,UB,N)
    F0 = (2./np.pi)**(1./4.)*np.exp(-(X**2))
    if (num == 1):
        psi = -2.*X*F0
    elif (num == 2):
        psi = 2/(3**(1/2)) * (-1+2*X**2)*F0
    elif (num == 3):
        psi = 4/(15**(1/2)) * X * (3-2*X**2)*F0
    elif (num == 4):
        psi = 4/(105**(1/2)) * (3-12*X**2+4*X**4)*F0
    elif (num == 5):
        psi = 8/(3*(105**(1/2))) * X * (-15+20*X**2-4*X**4)*F0
    elif (num == 6):
        psi = 8/(3*(1155**(1/2))) * (-15+90*X**2-60*X**4+8*X**6)*F0
    elif (num == 7):
        psi = 16/(3*(15015**(1/2))) * X * (105-210*X**2+84*X**4-8*X**6)*F0
    elif (num == 8):
        psi = 16/(45*(1001**(1/2))) * (105-840*X**2+840*X**4-224*X**6+16*X**8)*F0
    return (psi,X)


def ref_cgau(LB,UB,N,num):
    X = np.linspace(LB,UB,N)
    F0 = np.exp(-X**2)
    F1 = np.exp(-1j*X)
    F2 = (F1*F0)/(np.exp(-1/2)*2**(1/2)*np.pi**(1/2))**(1/2)
    if (num == 1):
        psi = F2*(-1j-2*X)*2**(1/2)
    elif (num == 2):
        psi = 1/3*F2*(-3+4j*X+4*X**2)*6**(1/2)
    elif (num == 3):
        psi = 1/15*F2*(7j+18*X-12j*X**2-8*X**3)*30**(1/2)
    elif (num == 4):
        psi = 1/105*F2*(25-56j*X-72*X**2+32j*X**3+16*X**4)*210**(1/2)
    elif (num == 5):
        psi = 1/315*F2*(-81j-250*X+280j*X**2+240*X**3-80j*X**4-32*X**5)*210**(1/2)
    elif (num == 6):
        psi = 1/3465*F2*(-331+972j*X+1500*X**2-1120j*X**3-720*X**4+192j*X**5+64*X**6)*2310**(1/2)
    elif (num == 7):
        psi = 1/45045*F2*(1303j+4634*X-6804j*X**2-7000*X**3+3920j*X**4+2016*X**5-448j*X**6-128*X**7)*30030**(1/2)
    elif (num == 8):
        psi = 1/45045*F2*(5937-20848j*X-37072*X**2+36288j*X**3+28000*X**4-12544j*X**5-5376*X**6+1024j*X**7+256*X**8)*2002**(1/2)

    psi = psi/np.real(np.sqrt(np.real(np.sum(psi*np.conj(psi)))*(X[1]-X[0])))
    return (psi, X)


def test_gaus():
    LB = -5
    UB = 5
    N = 1000
    for num in np.arange(1,9):
        [psi,x] = ref_gaus(LB,UB,N,num)
        w = pywt.Wavelet("gaus"+str(num))
        PSI, X = w.wavefun(length=N)

        assert_allclose(np.real(PSI), np.real(psi))
        assert_allclose(np.imag(PSI), np.imag(psi))
        assert_allclose(X, x)


def test_cgau():
    LB = -5
    UB = 5
    N = 1000
    for num in np.arange(1,9):
        [psi,x] = ref_cgau(LB,UB,N,num)
        w = pywt.Wavelet("cgau"+str(num))
        PSI_r, PSI_i, X = w.wavefun(length=N)
        PSI = PSI_r + 1j*PSI_i

        assert_allclose(np.real(PSI), np.real(psi))
        assert_allclose(np.imag(PSI), np.imag(psi))
        assert_allclose(X, x)


if __name__ == '__main__':
    run_module_suite()
