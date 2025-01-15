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

# DWT and IDWT

## Discrete Wavelet Transform

Let's do a [Discrete Wavelet Transform](ref-dwt) of some sample data `x`
using the `db2` wavelet. It's simple:

```{code-cell}
import pywt
x = [3, 7, 1, 1, -2, 5, 4, 6]
cA, cD = pywt.dwt(x, 'db2')
```

And the approximation and details coefficients are in `cA` and `cD`
respectively:

```{code-cell}
cA
```

```{code-cell}
cD
```

## Inverse Discrete Wavelet Transform

Now let's do the opposite operation, an [Inverse Discrete Wavelet Transform](ref-idwt):

```{code-cell}
pywt.idwt(cA, cD, 'db2')
```

Voilà! That's it!

## More examples

Now let's experiment with `dwt()` some more. For example, let's pass a
`Wavelet` object instead of the wavelet name and specify the signal
extension mode (the default is `Modes.symmetric`) for the border effect
handling:

```{code-cell}
w = pywt.Wavelet('sym3')
cA, cD = pywt.dwt(x, wavelet=w, mode='constant')
```

```{code-cell}
print(cA)
```

```{code-cell}
print(cD)
```

Note that the output coefficients arrays' length depends not only on the
input data length but also on the `Wavelet` type (particularly on its
filters length `Wavelet.dec_len` that are used in the transformation).

To find out what the size of the output data will be, use the `dwt_coeff_len()`
function:

```{code-cell}
pywt.dwt_coeff_len(data_len=len(x), filter_len=w.dec_len, mode='symmetric')
```

```{code-cell}
pywt.dwt_coeff_len(len(x), w, 'symmetric')
```

and the length of the output is:

```{code-cell}
len(cA)
```

Looks fine. (And if you expected that the output length would be a half of the
input data length, well, that's the trade-off that allows for the perfect
reconstruction...).

The third argument of the `dwt_coeff_len()` function is the already mentioned signal
extension mode (please refer to the PyWavelets' documentation for the `modes`
description). Currently, there are six extension modes available under `Modes`:

```{code-cell}
pywt.Modes.modes
```

As you see in the above example, the periodization (`Modes.periodization`) mode
is slightly different from the others. Its aim when doing the `pywt.dwt` transform
is to output coefficients arrays that are half of the length of the input data.

Knowing that, you should never mix the periodization mode with other modes when
doing `dwt` and `idwt`. Otherwise, it will produce **invalid results**:

```{code-cell}
x = [3, 7, 1, 1, -2, 5, 4, 6]

cA, cD = pywt.dwt(x, wavelet=w, mode='periodization')
print(pywt.idwt(cA, cD, 'sym3', 'symmetric'))  # invalid mode
```

```{code-cell}
print(pywt.idwt(cA, cD, 'sym3', 'periodization'))
```

## Tips & tricks

### Passing `None` instead of coefficients data to `pywt.idwt()`

Now, we showcase some tips and tricks. Passing `None` as one of the coefficient
arrays parameters is similar to passing a _zero-filled_ array. The results are
simply the same:

```{code-cell}
print(pywt.idwt([1,2,0,1], None, 'db2', 'symmetric'))
```

```{code-cell}
print(pywt.idwt([1, 2, 0, 1], [0, 0, 0, 0], 'db2', 'symmetric'))
```

```{code-cell}
print(pywt.idwt(None, [1, 2, 0, 1], 'db2', 'symmetric'))
```

```{code-cell}
print(pywt.idwt([0, 0, 0, 0], [1, 2, 0, 1], 'db2', 'symmetric'))
```

Remember that only one argument at a time can be `None`:

```{code-cell}
---
tags: [raises-exception, remove-output]
---
print(pywt.idwt(None, None, 'db2', 'symmetric'))
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: At least one coefficient parameter must be specified.
```

### Coefficients data size in `pywt.idwt`

When doing the `idwt` transform, usually the coefficient arrays
must have the same size.

```{code-cell}
---
tags: [raises-exception, remove-output]
---
print(pywt.idwt([1, 2, 3, 4, 5], [1, 2, 3, 4], 'db2', 'symmetric'))
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: Coefficients arrays must have the same size.
```

Not every coefficient array can be used in `idwt`. In the
following example the `idwt` will fail because the input arrays are
invalid - they couldn't be created as a result of `dwt`, because
the minimal output length for dwt using `db4` wavelet and the `Modes.symmetric`
mode is `4`, not `3`:

```{code-cell}
---
tags: [raises-exception, remove-output]
---
pywt.idwt([1,2,4], [4,1,3], 'db4', 'symmetric')
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: Invalid coefficient arrays length for specified wavelet. Wavelet and mode must be the same as used for decomposition.
```

```{code-cell}
int(pywt.dwt_coeff_len(1, pywt.Wavelet('db4').dec_len, 'symmetric'))
```
