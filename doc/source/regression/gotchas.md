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

+++ {"ignore-when-converting": "true"}

```{eval-rst}
.. currentmodule:: pywt

.. dropdown:: 🧑‍🔬 This notebook can be executed online. Click this section to try it out! ✨
    :color: success

    .. notebooklite:: gotchas.ipynb
      :width: 100%
      :height: 600px
      :prompt: Open notebook

.. dropdown:: Download this notebook
    :color: info
    :open:

    Please use the following links to download this notebook in various formats:

    1. :download:`Download IPyNB (IPython Notebook) <gotchas.ipynb>`
    2. :download:`Download Markdown Notebook (Jupytext) <gotchas.md>`
```

+++

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
