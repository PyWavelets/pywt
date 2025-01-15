---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 1.0.0
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{include} header.md

```

# The Wavelet object

## Wavelet families and builtin Wavelets names

`pywt.Wavelet` objects are really handy carriers of a bunch of DWT-specific
data like _quadrature mirror filters_ and some general properties associated
with them.

At first let's go through the methods of creating a `Wavelet` object.
The easiest and the most convenient way is to use built-in named Wavelets.

These wavelets are organized into groups called wavelet families. The most
commonly used families are:

```{code-cell}
import pywt
pywt.families()
```

The {func}`wavelist` function with family name passed as an argument is used to
obtain the list of wavelet names in each family.

```{code-cell}
for family in pywt.families():
    print("%s family: " % family + ', '.join(pywt.wavelist(family)))
```

To get the full list of built-in wavelets' names, just use the `pywt.wavelist` function
without any arguments.

## Creating Wavelet objects

Now that we know all the names, let's finally create a `Wavelet` object:

```{code-cell}
w = pywt.Wavelet('db3')
```

and, that's it!

## Wavelet properties

But what can we do with `Wavelet` objects? Well, they carry some
interesting pieces of information.

First, let's try printing a `Wavelet` object that we used earlier.
This shows a brief information about its name, its family name and some
properties like orthogonality and symmetry.

```{code-cell}
print(w)
```

But the most important bits of information are the wavelet filters coefficients,
which are used in Discrete Wavelet Transform. These coefficients
can be obtained via the `Wavelet.dec_lo`, `dec_hi`, `rec_lo`,
and the `rec_hi` attributes, which
correspond to lowpass & highpass decomposition filters, and lowpass &
highpass reconstruction filters respectively:

```{code-cell}
def print_array(arr):
    print("[%s]" % ", ".join(["%.14f" % x for x in arr]))
```

Another way to get the filters data is to use the `filter_bank`
attribute, which returns all four filters in a tuple:

```{code-cell}
w.filter_bank == (w.dec_lo, w.dec_hi, w.rec_lo, w.rec_hi)
```

Other properties of a `Wavelet` object are:

`name`, `short_family_name`, and `family_name`:

```{code-cell}
print(w.name)
print(w.short_family_name)
print(w.family_name)
```

Decomposition (`dec_len`) and reconstruction (`rec_len`) filter lengths:

```{code-cell}
w.dec_len
```

```{code-cell}
w.rec_len
```

Orthogonality (`orthogonal`) and biorthogonality (`biorthogonal`):

```{code-cell}
w.orthogonal
```

```{code-cell}
w.biorthogonal
```

Symmetry (`symmetry`):

```{code-cell}
print(w.symmetry)
```

Number of vanishing moments for the scaling function `phi` (`vanishing_moments_phi`)
and the wavelet function `psi` (`vanishing_moments_psi`), associated with the filters:

```{code-cell}
 w.vanishing_moments_phi
```

```{code-cell}
w.vanishing_moments_psi
```

Now when we know a bit about the builtin Wavelets, let's see how to create
[custom wavelets](custom-wavelets). These can be created in two ways:

1. Passing the filter bank object that implements the `filter_bank` attribute. The
   attribute must return four filters coefficients.

```{code-cell}
class MyHaarFilterBank(object):
    @property
    def filter_bank(self):
        from math import sqrt
        return (
          [sqrt(2)/2, sqrt(2)/2], [-sqrt(2)/2, sqrt(2)/2],
          [sqrt(2)/2, sqrt(2)/2], [sqrt(2)/2, -sqrt(2)/2]
        )

my_wavelet = pywt.Wavelet('My Haar Wavelet', filter_bank=MyHaarFilterBank())
```

2. Passing the filters coefficients directly as the `filter_bank` parameter.

```{code-cell}
from math import sqrt
my_filter_bank = (
  [sqrt(2)/2, sqrt(2)/2], [-sqrt(2)/2, sqrt(2)/2],
  [sqrt(2)/2, sqrt(2)/2], [sqrt(2)/2, -sqrt(2)/2]
)
my_wavelet = pywt.Wavelet('My Haar Wavelet', filter_bank=my_filter_bank)
```

Note that such custom wavelets **will not** have all the properties set
to correct values and some of them could be missing:

```{code-cell}
print(my_wavelet)
```

You can, however, set a couple of them on your own:

```{code-cell}
my_wavelet.orthogonal = True
my_wavelet.biorthogonal = True
```

Let's view the values of the custom wavelet properties again:

```{code-cell}
print(my_wavelet)
```

## And now... the `wavefun`!

We all know that the fun with wavelets is in wavelet functions.
Now, what would this package be without a tool to compute wavelet
and scaling functions approximations?

This is the purpose of the `wavefun()` method, which is used to
approximate scaling function (`phi`) and wavelet function (`psi`) at the
given level of refinement, based on the filters coefficients.

The number of returned values varies depending on the wavelet's
orthogonality property. For orthogonal wavelets, the result is a tuple
with the scaling function, wavelet function, and the xgrid coordinates.

```{code-cell}
w = pywt.Wavelet('sym3')
w.orthogonal
```

```{code-cell}
(phi, psi, x) = w.wavefun(level=5)
```

For biorthogonal (non-orthogonal) wavelets, different scaling and wavelet
functions are used for decomposition and reconstruction, and thus, five
elements are returned: decomposition scaling and wavelet functions
approximations, reconstruction scaling and wavelet functions approximations,
and the xgrid.

```{code-cell}
w = pywt.Wavelet('bior1.3')
w.orthogonal
```

```{code-cell}
(phi_d, psi_d, phi_r, psi_r, x) = w.wavefun(level=5)
```

:::{seealso}
You can find live examples of the usage of `wavefun()` and
images of all the built-in wavelets on the
[Wavelet Properties Browser](http://wavelets.pybytes.com) page.

However, **this website is no longer actively maintained** and does not
include every wavelet present in PyWavelets. The precision of the wavelet
coefficients at that site is also lower than those included in PyWavelets.
:::
