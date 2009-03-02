# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id: $

"""
Continuous Wavelets definitions.
"""

__all__ = [
    'mexican_hat', 'morlet',
    'gauss1', 'gauss2', 'gauss3',
    'cgauss1', 'cgauss2',
    'cmorlet', 'cshannon', 'cfbsp',
]
__all__ += ['cwavelist']

from math import sqrt, pi
from numerix import cos, exp, sinc
from numerix import linspace

"""
class WaveletFunction(object):
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_xgrid(self, points):
        return linspace(self.lower_bound, self.upper_bound, points)

    @classmethod
    def for_name(cls, name):
        pass

class MexicanHat(WaveletFunction):
    def __init__(self, lower_bound=-8.0, upper_bound=8.0):
        super(MexicanHat, self).__init__(lower_bound, upper_bound)

        self.properties = {
                "family": "Mexican Hat", "orthogonal": False, "biorthogonal": False,
                "compact support": False, "complex": False,"support": "infinite",
                "effective support": [-5, 5], "symmetry": "symmetric"
            }

    def __call__(self, points):
        x = self.get_xgrid(points)
        x2 = x*x
        psi = -x2
        psi += 1
        psi *= (2.0/sqrt(3)*(pi**-0.25))
        psi *= exp(-0.5 * x2)
        return psi, x


class Morlet(WaveletFunction):
    def __init__(self, lower_bound=-8.0, upper_bound=8.0):
        super(Morlet, self).__init__(lower_bound, upper_bound)

    def __call__(self, points):
        x = self.get_xgrid(points)
        minus_half_x2 = x*x
        minus_half_x2 *= -0.5
        psi = exp(minus_half_x2)
        psi *= cos(5*x)
        return psi, x

class GaussDerivative(WaveletFunction):
    def __init__(self, lower_bound=-5.0, upper_bound=5.0):
        super(GaussDerivative, self).__init__(lower_bound, upper_bound)
        assert order in [1, 2, 3]

        self.order = order
        self.psi, self.properties = {
                1: (self.gauss1, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": [-5, 5], "symmetry": "symmetric"
                        }
                    ),
                2: (self.gauss2, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": [-5, 5], "symmetry": "anti-symmetric"
                        }
                    ),
                3: (self.gauss3, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": [-5, 5], "symmetry": "symmetric"
                        }
                    ),
            }[self.order]

    def __call__(self, points):
        return self.psi(points, self.lower_bound, self.upper_bound)

    def gauss1(self, points, lower_bound, upper_bound):
        x = self.get_xgrid(points)
        x2 = x*x
        psi = exp(-x2)
        psi *= x
        psi *= -2*(2.0/pi)**0.25
        return psi, x

    def gauss2(self, points, lower_bound, upper_bound):
        x = self.get_xgrid(points)
        x2 = x*x
        psi = exp(-x2)
        psi *=  -1+2*x2
        psi *= -2.0/(3**0.25) * (2.0/pi)**0.25
        return psi, x

    def gauss3(self, points, lower_bound, upper_bound):
        x = self.get_xgrid(points)
        x2 = x*x
        psi =  exp(-x2)
        psi *=  x
        psi *= (3-2*x2)
        psi *= (2.0/pi)**0.25 * -4.0/(15**0.5)
        return psi, x

class ComplexMorlet(WaveletFunction):
    def __init__(self, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
        super(ComplexMorlet, self).__init__(lower_bound, upper_bound)
        assert bandwidth > 0
        assert center_frequency > 0
        self.bandwidth = bandwidth
        self.center_frequency = center_frequency

    def __call__(self, points):
        x = self.get_xgrid(points)
        a = x*x
        a *= -1.0/self.bandwidth
        psi = 1.0 / sqrt(pi * self.bandwidth) * exp(2j*pi*self.center_frequency*x)
        psi *= exp(a)
        return psi, x

class ComplexFrequencyBSpline(WaveletFunction):
    def __init__(self, order, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
        super(ComplexFrequencyBSpline, self).__init__(lower_bound, upper_bound)
        assert order > 0
        assert bandwidth > 0
        assert center_frequency > 0
        self.order = order
        self.bandwidth = bandwidth
        self.center_frequency = center_frequency

    def __call__(self, points):
        x = self.get_xgrid(points)
        psi = exp(2j*pi*center_frequency*x)
        psi *= sinc(bandwidth/order*x)**order
        psi *= sqrt(bandwidth)
        return psi, x

def cfbsp(points, order, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
    order, bandwidth, center_frequency = int(order), float(bandwidth), float(center_frequency)
    assert bandwidth > 0
    assert center_frequency > 0
cfbsp.params = [int, float, float]

def cshannon(points, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
    bandwidth, center_frequency = float(bandwidth), float(center_frequency)
    assert bandwidth > 0
    assert center_frequency > 0
    x = self.get_xgrid(points)
    psi = exp(2j*pi*center_frequency*x)
    psi *= sinc(bandwidth*x)
    psi *= sqrt(bandwidth)
    return psi, x
cshannon.params = [float, float]

"""


def mexican_hat(points, lower_bound=-8.0, upper_bound=8.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi = -x2
    psi += 1
    psi *= (2.0/sqrt(3)*(pi**-0.25))
    psi *= exp(-0.5 * x2)
    return psi, x

def morlet(points, lower_bound=-8.0, upper_bound=8.0):
    x = linspace(lower_bound, upper_bound, points)
    minus_half_x2 = x*x
    minus_half_x2 *= -0.5
    psi = exp(minus_half_x2)
    psi *= cos(5*x)
    return psi, x

def gauss1(points, lower_bound=-5.0, upper_bound=5.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi = exp(-x2)
    psi *= x
    psi *= -2*(2.0/pi)**0.25
    return psi, x

def gauss2(points, lower_bound=-5.0, upper_bound=5.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi = exp(-x2)
    psi *=  -1+2*x2
    psi *= -2.0/(3**0.25) * (2.0/pi)**0.25
    return psi, x

def gauss3(points, lower_bound=-5.0, upper_bound=5.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi =  exp(-x2)
    psi *=  x
    psi *= (3-2*x2)
    psi *= (2.0/pi)**0.25 * -4.0/(15**0.5)
    return psi, x

def cgauss1(points, lower_bound=-5.0, upper_bound=5.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi = (-1j-2*x)
    psi *= exp(-x2)
    psi *= sqrt(2) / sqrt(exp(-0.5) * sqrt(2) * sqrt(pi))
    psi *= exp(-1j*x)
    return psi, x

def cgauss2(points, lower_bound=-5.0, upper_bound=5.0):
    x = linspace(lower_bound, upper_bound, points)
    x2 = x*x
    psi = 1j*(exp(-x2) * exp(-1j*x))
    tmp = 4j*x
    x2 *= 4
    tmp += x2
    tmp -= 3
    psi *= tmp
    psi *= sqrt(6) * (1.0/sqrt(exp(-0.5) * sqrt(2) * sqrt(pi))) / 3
    return psi, x

def cmorlet(points, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
    assert bandwidth > 0
    assert center_frequency > 0
    x = linspace(lower_bound, upper_bound, points)
    x2b = x*x
    x2b *= -1.0/bandwidth
    psi = 1.0 / sqrt(pi * bandwidth) * exp(2j*pi*center_frequency*x)
    psi *= exp(x2b)
    return psi, x

def cshannon(points, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
    assert bandwidth > 0
    assert center_frequency > 0
    x = linspace(lower_bound, upper_bound, points)
    psi = exp(2j*pi*center_frequency*x)
    psi *= sinc(bandwidth*x)
    psi *= sqrt(bandwidth)
    return psi, x

def cfbsp(points, order, bandwidth, center_frequency, lower_bound=-8.0, upper_bound=8.0):
    assert order > 0
    assert bandwidth > 0
    assert center_frequency > 0
    x = linspace(lower_bound, upper_bound, points)
    psi = exp(2j*pi*center_frequency*x)
    psi *= sinc(bandwidth/order*x)**order
    psi *= sqrt(bandwidth)
    return psi, x

wavelet_functions = {
    #real continuous wavelet functions
    "mexican_hat":  (mexican_hat, {
                            "family": "Mexican Hat", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False,"support": "infinite",
                            "effective support": (-5, 5), "symmetry": "symmetric"
                        }, None
                    ),
    "morlet":       (morlet, {
                            "family": "Morlet", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": (-4, 4), "symmetry": "symmetric"
                        }, None
                    ),
    "gauss1":       (gauss1, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": (-5, 5), "symmetry": "symmetric"
                        }, None
                    ),
    "gauss2":       (gauss2, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": (-5, 5), "symmetry": "anti-symmetric"
                        }, None
                    ),
    "gauss3":      (gauss3, {
                            "family": "Gaussian", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": False, "support": "infinite",
                            "effective support": (-5, 5), "symmetry": "symmetric"
                        }, None
                    ),
    #complex continuous wavelets
    #"cgauss1":     (cgauss1, {
    #                        "family": "Complex Gaussian", "orthogonal": False, "biorthogonal": False,
    #                        "compact support": False, "complex": True, "support": "infinite",
    #                        "symmetry": "symmetric"
    #                    }
    #                ),
    #"cgauss2":     (cgauss2, {
    #                        "family": "Complex Gaussian", "orthogonal": False, "biorthogonal": False,
    #                        "compact support": False, "complex": True, "support": "infinite",
    #                        "symmetry": "anti-symmetric"
    #                    }
    #                ),
    "cmorlet":      (cmorlet, {
                            "family": "Complex Morlet", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": True, "support": "infinite"
                        }, (float, float)
                    ),
    "cshannon":     (cshannon, {
                            "family": "Shannon", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": True, "support": "infinite"
                        }, (float, float)
                    ),
    "cfbsp":        (cfbsp, {
                            "family": "Frequency B-Spline", "orthogonal": False, "biorthogonal": False,
                            "compact support": False, "complex": True, "support": "infinite"
                        }, (int, float, float)
                    ),
    }

"""
def name_to_wavelet_and_params(name):
    if name in wavelet_functions:
        psi, properties = wavelet_functions[self.name]
        return psi, properties, ()
    elif '-' in name:
        for basename in wavelet_functions:
            if wavelet_name.startswith(basename):
                psi, properties = wavelet_functions[basename]
                params = name[len(basename):].split('-')
                if not hasattr(psi, 'params_count') or psi.params_count != len(params):
                    raise ValueError("Invalid parameter string in name: %s. Expected %d hyphen-delimited params." % \
                                        (name[len(basename):], psi.params_count))
                return psi, properties, params
    raise ValueError("Invalid continuous wavelet name: %s." % name)
"""

def format_wavelet_name(basename, params_spec=[]):
    if params_spec:
        (basename + '-'.join(["(%s)" % param.__name__ for param in params_spec]))
    return basename

def function_for_name(name):
    if name in wavelet_functions:
        psi, properties, params_spec = wavelet_functions[name]
        if params_spec:
            raise ValueError("Invalid wavelet name - '%s'. Missing params part for wavelet '%s'." % \
                                format_wavelet_name(name, params_spec))
    else:
        psi = None
        for basename in wavelet_functions:
            if name.startswith(basename):
                _psi, properties, params_spec = wavelet_functions[basename]
                if not params_spec:
                    raise ValueError("Invalid wavelet name - '%s'. No params expected for wavelet '%s'." % \
                                        (name, basename))
                params = name[len(basename):].split('-')
                if len(params_spec) != len(params):
                    raise ValueError("Invalid wavelet name - '%s'. Expected %d parameters for '%s' wavelet, got %d instead." % \
                                        (name, len(params_spec), format_wavelet_name(basename, params_spec), len(params)))
                try:
                    params = [type(value) for type, value in zip(params_spec, params)]
                except ValueError:
                    raise ValueError("Invalid wavelet name - '%s'. Cannot convert parameter '%s' to type '%s'." % \
                                        (value, type.__name__))
                params = tuple(params)

                def psi(points, **kwds):
                    return _psi(points, *params, **kwds)
    if psi is None:
        raise ValueError("Invalid wavelet name - '%s'." % name)

    return psi, properties.copy()


def cwavelist():
    return [format_wavelet_name(basename, spec[2]) for basename, spec in wavelet_functions.items()]
