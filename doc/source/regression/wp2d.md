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

# 2D Wavelet Packets

## Import pywt

```{code-cell}
import pywt
import numpy
```

## Create 2D Wavelet Packet structure

Start with preparing test data:

```{code-cell}
x = numpy.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, 'd')
print(x)
```

Now create a 2D [Wavelet Packet](ref-wp) object:

```{code-cell}
wp = pywt.WaveletPacket2D(data=x, wavelet='db1', mode='symmetric')
```

The input `data` and decomposition coefficients are stored in the
`WaveletPacket2D.data` attribute:

```{code-cell}
print(wp.data)
```

Nodes (the `Node2D` class) are identified by paths. For the root node, the path is
`''` and the decomposition level is `0`.

```{code-cell}
print(repr(wp.path))
```

```{code-cell}
print(wp.level)
```

`WaveletPacket2D.maxlevel`, if not given in the constructor, is
automatically computed based on the data size:

```{code-cell}
print(wp.maxlevel)
```

## Traversing WP tree

Wavelet Packet nodes (`Node2D`) are arranged in a tree. Each node in a WP
tree is uniquely identified and addressed by a `Node2D.path` string.

In the 1D `WaveletPacket` case nodes were accessed using `'a'`
(approximation) and `'d'` (details) path names (each node has two 1D
children).

Because now we deal with a bit more complex structure (each node has four
children), we have four basic path names based on the dwt 2D output convention
to address the WP2D structure:

- `a` - LL, low-low coefficients
- `h` - LH, low-high coefficients
- `v` - HL, high-low coefficients
- `d` - HH, high-high coefficients

In other words, subnode naming corresponds to the `dwt2` function output
naming convention (as wavelet packet transform is based on the dwt2 transform):

```
                            -------------------
                            |        |        |
                            | cA(LL) | cH(LH) |
                            |        |        |
(cA, (cH, cV, cD))  <--->   -------------------
                            |        |        |
                            | cV(HL) | cD(HH) |
                            |        |        |
                            -------------------

   (fig.1: DWT 2D output and interpretation)
```

Knowing what the nodes names are, we can now access them using the indexing
operator `obj[x]` (`WaveletPacket2D.__getitem__`):

```{code-cell}
print(wp['a'].data)
```

```{code-cell}
print(wp['h'].data)
```

```{code-cell}
print(wp['v'].data)
```

```{code-cell}
print(wp['d'].data)
```

Similarly, a subnode of a subnode can be accessed by:

```{code-cell}
print(wp['aa'].data)
```

Indexing base 2D (`WaveletPacket2D`) (as well as 1D `WaveletPacket`)
using compound paths is just the same as indexing the WP subnode:

```{code-cell}
node = wp['a']
print(node['a'].data)
```

```{code-cell}
print(wp['a']['a'].data is wp['aa'].data)
```

Following down the decomposition path:

```{code-cell}
print(wp['aaa'].data)
```

```{code-cell}
---
tags: [raises-exception, remove-output]
---
print(wp['aaaa'].data)
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
IndexError: Path length is out of range.
```

Oops, we have reached the maximum level of decomposition for the `'aaaa'` path,
which, by the way, was:

```{code-cell}
print(wp.maxlevel)
```

Now, try an invalid path:

```{code-cell}
---
tags: [raises-exception, remove-output]
---
print(wp['f'])
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: Subnode name must be in ['a', 'h', 'v', 'd'], not 'f'.
```

### Accessing Node2D's attributes

`WaveletPacket2D` is a tree data structure, which evaluates to a set
of `Node2D` objects. `WaveletPacket2D` is just a special the `Node2D` class (which in turn inherits from a `BaseNode` class
just like with `Node` and `WaveletPacket` for the 1D case).

```{code-cell}
print(wp['av'].data)
```

```{code-cell}
print(wp['av'].path)
```

```{code-cell}
print(wp['av'].node_name)
```

```{code-cell}
print(wp['av'].parent.path)
```

```{code-cell}
print(wp['av'].parent.data)
```

```{code-cell}
print(wp['av'].level)
```

```{code-cell}
print(wp['av'].maxlevel)
```

```{code-cell}
print(wp['av'].mode)
```

### Collecting nodes

We can get all nodes on the particular level using the
`WaveletPacket2D.get_level` method:

0 level - the root `wp` node:

```{code-cell}
len(wp.get_level(0))
```

```{code-cell}
print([node.path for node in wp.get_level(0)])
```

- 1st level of decomposition:

```{code-cell}
len(wp.get_level(1))
```

```{code-cell}
print([node.path for node in wp.get_level(1)])
```

2nd level of decomposition:

```{code-cell}
len(wp.get_level(2))
```

```{code-cell}
paths = [node.path for node in wp.get_level(2)]
for i, path in enumerate(paths):
    if (i+1) % 4 == 0:
        print(path)
    else:
        print(path, end=' ')
```

3rd level of decomposition:

```{code-cell}
print(len(wp.get_level(3)))
```

```{code-cell}
paths = [node.path for node in wp.get_level(3)]
for i, path in enumerate(paths):
    if (i+1) % 8 == 0:
        print(path)
    else:
        print(path, end=' ')
```

Note that `WaveletPacket2D.get_level` performs automatic decomposition
until it reaches the given level.

## Reconstructing data from Wavelet Packets

Let's create a new empty 2D Wavelet Packet structure and set its nodes
values with known data from the previous examples:

```{code-cell}
new_wp = pywt.WaveletPacket2D(data=None, wavelet='db1', mode='symmetric')
```

```{code-cell}
new_wp['vh'] = wp['vh'].data  # [[0.0, 0.0], [0.0, 0.0]]
new_wp['vv'] = wp['vh'].data  # [[0.0, 0.0], [0.0, 0.0]]
new_wp['vd'] = [[0.0, 0.0], [0.0, 0.0]]
```

```{code-cell}
new_wp['a'] = [[3.0, 7.0, 11.0, 15.0], [3.0, 7.0, 11.0, 15.0],
              [3.0, 7.0, 11.0, 15.0], [3.0, 7.0, 11.0, 15.0]]
new_wp['d'] = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
```

For convenience, `Node2D.data` gets automatically extracted from the
base `Node2D` object:

```{code-cell}
new_wp['h'] = wp['h'] # all zeros
```

Note: just remember to not assign to the `node.data parameter directly (TODO).

And reconstruct the data from the `a`, `d`, `vh`, `vv`, `vd` and `h`
packets (Note that `va` node was not set and the WP tree is "not complete"
\- the `va` branch will be treated as _zero-array_):

```{code-cell}
print(new_wp.reconstruct(update=False))
```

Now set the `va` node with the known values and do the reconstruction again:

```{code-cell}
new_wp['va'] = wp['va'].data # [[-2.0, -2.0], [-2.0, -2.0]]
print(new_wp.reconstruct(update=False))
```

which is just the same as the base sample data `x`.

Of course we can go the other way and remove nodes from the tree. If we delete
the `va` node, again, we get the "not complete" tree from one of the previous
examples:

```{code-cell}
del new_wp['va']
print(new_wp.reconstruct(update=False))
```

Just restore the node before the next examples:

```{code-cell}
new_wp['va'] = wp['va'].data
```

If the `update` param in the `WaveletPacket2D.reconstruct` method is set
to `False`, the node's `Node2D.data` attribute will not be updated.

```{code-cell}
print(new_wp.data)
```

Otherwise, the `WaveletPacket2D.data` attribute will be set to the
reconstructed value.

```{code-cell}
print(new_wp.reconstruct(update=True))
```

```{code-cell}
print(new_wp.data)
```

Since we have an interesting WP structure built, it is a good occasion to
present the `WaveletPacket2D.get_leaf_nodes()` method, which collects
non-zero leaf nodes from the WP tree:

```{code-cell}
print([n.path for n in new_wp.get_leaf_nodes()])
```

Passing the `decompose = True` parameter to the method will force the WP
object to do a full decomposition up to the _maximum level_ of decomposition:

```{code-cell}
paths = [n.path for n in new_wp.get_leaf_nodes(decompose=True)]
len(paths)
```

```{code-cell}
for i, path in enumerate(paths):
    if (i+1) % 8 == 0:
        print(path)
    else:
        try:
            print(path, end=' ')
        except:
            print(path, end=' ')
```

## Lazy evaluation

:::{note}
This section is for the demonstration of PyWavelets' internals' purposes
only. Do not rely on the attribute access to nodes as presented in
this example.
:::

```{code-cell}
x = numpy.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8)
wp = pywt.WaveletPacket2D(data=x, wavelet='db1', mode='symmetric')
```

At first, the `wp`'s attribute `a` is `None`

```{code-cell}
print(wp.a)
```

**Remember that you should not rely on the attribute access.**

During the first attempt to access the node it is computed
via decomposition of its parent node (the wp object itself).

```{code-cell}
print(wp['a'])
```

Now the `a` is set to the newly created node:

```{code-cell}
print(wp.a)
```

And so is `wp.d`:

```{code-cell}
print(wp.d)
```
