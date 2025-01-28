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

# Wavelet Packets

## `import pywt` and construct a helper function

```{code-cell}
import pywt
```

This helper function can format arrays in a consistent manner across
different systems. Please note that this function is just for the purpose of
this example and is not part of the PyWavelets library, and it is not necessary
or required to use it in your own code:

```{code-cell}
def format_array(a):
    """Consistent array representation across different systems"""
    import numpy
    a = numpy.where(numpy.abs(a) < 1e-5, 0, a)
    return numpy.array2string(a, precision=5, separator=' ', suppress_small=True)
```

## Create Wavelet Packet structure

Okay, let's create a sample instance of the `WaveletPacket` class:

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

The input data and decomposition coefficients are stored in the
`WaveletPacket.data` attribute:

```{code-cell}
print(wp.data)
```

Nodes are identified by their paths, i.e., `Node.path`. For the root
node, the path is `''` and the decomposition level is `0`.

```{code-cell}
print(repr(wp.path))
```

```{code-cell}
print(wp.level)
```

The `maxlevel` attribute, if not given as param in the constructor, is
automatically computed:

```{code-cell}
print(wp['ad'].maxlevel)
```

## Traversing the WP tree

### Accessing subnodes

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

First check what is the maximum level of decomposition:

```{code-cell}
print(wp.maxlevel)
```

and try accessing subnodes of the WP tree.

1st level:

```{code-cell}
print(wp['a'].data)
```

```{code-cell}
print(wp['a'].path)
```

2nd level:

```{code-cell}
print(wp['aa'].data)
```

```{code-cell}
print(wp['aa'].path)
```

3rd level:

```{code-cell}
print(wp['aaa'].data)
```

```{code-cell}
print(wp['aaa'].path)
```

Oops, we have reached the maximum level of decomposition and received an `IndexError`:

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

Now, try an invalid path:

```{code-cell}
---
tags: [raises-exception, remove-output]
---
print(wp['ac'])
```

+++ {"tags": ["jupyterlite_sphinx_strip"]}

```{code-block} python
:class: pywt-handcoded-cell-output
Traceback (most recent call last):
...
ValueError: Subnode name must be in ['a', 'd'], not 'c'.
```

which just yielded a `ValueError`.

### Accessing `Node`'s attributes

The `WaveletPacket` object is a tree data structure, which evaluates to a set
of `Node` objects. `WaveletPacket` is just a special subclass
of the `Node` class (which in turn inherits from the `BaseNode` class).

Tree nodes can be accessed using the `obj[x]` (`Node.__getitem__`)
operator.

Each tree node has a set of attributes: `data`, `path`,
`node_name`, `parent`, `level`,
`maxlevel` and `mode`.

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

```{code-cell}
print(wp['ad'].data)
```

```{code-cell}
print(wp['ad'].path)
```

```{code-cell}
print(wp['ad'].node_name)
```

```{code-cell}
print(wp['ad'].parent.path)
```

```{code-cell}
print(wp['ad'].level)
```

```{code-cell}
print(wp['ad'].maxlevel)
```

```{code-cell}
print(wp['ad'].mode)
```

### Collecting nodes

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

We can get all nodes on the particular level either in `natural` order:

```{code-cell}
print([node.path for node in wp.get_level(3, 'natural')])
```

or sorted based on the band frequency (`freq`):

```{code-cell}
print([node.path for node in wp.get_level(3, 'freq')])
```

Note that `WaveletPacket.get_level()` also performs automatic decomposition
until it reaches the specified `level`.

## Reconstructing data from Wavelet Packets

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

Now create a new instance of the `WaveletPacket` class and set its nodes
with some data.

```{code-cell}
new_wp = pywt.WaveletPacket(data=None, wavelet='db1', mode='symmetric')
```

```{code-cell}
new_wp['aa'] = wp['aa'].data
new_wp['ad'] = [-2., -2.]
```

For convenience, `Node.data` gets automatically extracted from the `Node` object:

```{code-cell}
new_wp['d'] = wp['d']
```

And reconstruct the data from the `aa`, `ad` and `d` packets.

```{code-cell}
print(new_wp.reconstruct(update=False))
```

If the `update` param in the reconstruct method is set to `False`, the
node's `Node.data` will not be updated.

```{code-cell}
print(new_wp.data)
```

Otherwise, the `Node.data` attribute will be set to the reconstructed
value.

```{code-cell}
print(new_wp.reconstruct(update=True))
```

```{code-cell}
print(new_wp.data)
```

```{code-cell}
print([n.path for n in new_wp.get_leaf_nodes(False)])
```

```{code-cell}
print([n.path for n in new_wp.get_leaf_nodes(True)])
```

## Removing nodes from Wavelet Packet tree

Let's create some sample data:

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

First, let's start with a tree decomposition at level 2. The leaf nodes in the tree are:

```{code-cell}
dummy = wp.get_level(2)
for n in wp.get_leaf_nodes(False):
    print(n.path, format_array(n.data))
```

```{code-cell}
node = wp['ad']
print(node)
```

To remove a node from the WP tree, use Python's `del obj[x]` (`Node.__delitem__`):

```{code-cell}
del wp['ad']
```

The leaf nodes that left in the tree are:

```{code-cell}
for n in wp.get_leaf_nodes():
    print(n.path, format_array(n.data))
```

And the reconstruction is:

```{code-cell}
print(wp.reconstruct())
```

Now, restore the deleted node value.

```{code-cell}
wp['ad'].data = node.data
```

Printing leaf nodes and tree reconstruction confirms the original state of the
tree:

```{code-cell}
for n in wp.get_leaf_nodes(False):
    print(n.path, format_array(n.data))
```

```{code-cell}
print(wp.reconstruct())
```

## Lazy evaluation

:::{note}
This section is for demonstration of PyWavelets' internal purposes
only. Do not rely on the attribute access to nodes as presented in
this example.
:::

```{code-cell}
x = [1, 2, 3, 4, 5, 6, 7, 8]
wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='symmetric')
```

At first the wp's attribute `a` is `None`:

```{code-cell}
print(wp.a)
```

**Remember that you should not rely on the attribute access.**

At the first attempt to access the node, it is computed via the decomposition
of its parent node (which is the `wp` object itself).

```{code-cell}
print(wp['a'])
```

Now `wp.a` is set to the newly created node:

```{code-cell}
print(wp.a)
```

And so is `wp.d`:

```{code-cell}
print(wp.d)
```
