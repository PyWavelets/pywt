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

# Signal Extension Modes

Import `pywt` first:

```{code-cell}
import pywt
```

and construct a helper function that can format arrays in a consistent manner
across different systems. Please note that this function is just for the purpose of
this example and is not part of the PyWavelets library, and it is not necessary or
required to use it in your own code:

```{code-cell}
def format_array(a):
    """Consistent array representation across different systems"""
    import numpy
    a = numpy.where(numpy.abs(a) < 1e-5, 0, a)
    return numpy.array2string(a, precision=5, separator=' ', suppress_small=True)
```

A list of available signal extension [modes](Modes):

```{code-cell}
pywt.Modes.modes
```

An invalid mode name should raise a `ValueError`:

```{code-cell}
---
tags: [raises-exception, remove-output]
---
pywt.dwt([1,2,3,4], 'db2', 'invalid')
```

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: Unknown mode name 'invalid'.
```

You can also refer to modes via the attributes of the `Modes` class:

```{code-cell}
x = [1, 2, 1, 5, -1, 8, 4, 6]
for mode_name in ['zero', 'constant', 'symmetric', 'reflect', 'periodic', 'smooth', 'periodization']:
    mode = getattr(pywt.Modes, mode_name)
    cA, cD = pywt.dwt(x, 'db2', mode)
    print("Mode: %d (%s)" % (mode, mode_name))
```

The default mode is [symmetric](Modes.symmetric):

```{code-cell}
cA, cD = pywt.dwt(x, 'db2')
cA
```

```{code-cell}
cD
```

```{code-cell}
pywt.idwt(cA, cD, 'db2')
```

Specify the mode using a keyword argument:

```{code-cell}
cA, cD = pywt.dwt(x, 'db2', mode='symmetric')
cA
```

```{code-cell}
cD
```

```{code-cell}
pywt.idwt(cA, cD, 'db2')
```
