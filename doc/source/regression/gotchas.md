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

(reg-gotchas)=

```{eval-rst}
.. currentmodule:: pywt

.. notebooklite:: gotchas.ipynb
   :width: 100%
   :height: 600px
   :prompt: Try classic Notebook!
```

# Gotchas

PyWavelets utilizes `NumPy` under the hood. That's why handling the data
containing `None` values can be surprising. `None` values are converted to
'not a number' (`numpy.NaN`) values:

```{code-cell}
import numpy, pywt
x = [None, None]
mode = 'symmetric'
wavelet = 'db1'
cA, cD = pywt.dwt(x, wavelet, mode)
```

The results are:

```{code-cell}
numpy.all(numpy.isnan(cA))
```

<!-- True -->

```{code-cell}
numpy.all(numpy.isnan(cD))
```

<!-- True -->

```{code-cell}
rec = pywt.idwt(cA, cD, wavelet, mode)
numpy.all(numpy.isnan(rec))
```

<!-- True -->
