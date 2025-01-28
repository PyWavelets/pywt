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

# Multilevel DWT, IDWT and SWT

## Multilevel DWT decomposition

Here is an example of multilevel DWT decomposition using the `db1` wavelet into
approximation and detail coefficients:

```{code-cell}
import pywt
x = [3, 7, 1, 1, -2, 5, 4, 6]
db1 = pywt.Wavelet('db1')
cA3, cD3, cD2, cD1 = pywt.wavedec(x, db1)
```

```{code-cell}
cA3
```

```{code-cell}
cD3
```

```{code-cell}
cD2
```

```{code-cell}
cD1
```

The number of levels in the decomposition can be determined as well:

```{code-cell}
pywt.dwt_max_level(len(x), db1)
```

or decompose to a specific level:

```{code-cell}
cA2, cD2, cD1 = pywt.wavedec(x, db1, mode='constant', level=2)
```

## Multilevel IDWT reconstruction

```{code-cell}
coeffs = pywt.wavedec(x, db1)
pywt.waverec(coeffs, db1)
```

## Multilevel SWT decomposition

```{code-cell}
x = [3, 7, 1, 3, -2, 6, 4, 6]
(cA2, cD2), (cA1, cD1) = pywt.swt(x, db1, level=2)
```

```{code-cell}
cA1
```

```{code-cell}
cD1
```

```{code-cell}
cA2
```

```{code-cell}
cD2
```

```{code-cell}
[(cA2, cD2)] = pywt.swt(cA1, db1, level=1, start_level=1)
```

```{code-cell}
cA2
```

```{code-cell}
cD2
```

```{code-cell}
coeffs = pywt.swt(x, db1)
len(coeffs)
```

```{code-cell}
pywt.swt_max_level(len(x))
```
