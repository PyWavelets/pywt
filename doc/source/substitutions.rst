.. |mode| replace:: Signal extension mode to deal with the border distortion problem. See :ref:`Modes <ref-modes>` for details.

.. |data| replace::
    Input signal can be NumPy array, Python list or other iterable object. Both *single* and *double* precision floating-point data types are supported and the output type depends on the input type. If the input data is not in one of these types it will be converted to the default *double* precision data format before performing computations.

.. |wavelet| replace::
   Wavelet to use in the transform. This can be a name of the wavelet from the :func:`wavelist` list or a :class:`Wavelet` object instance.

.. |axis| replace::
   Axis to perform the transform over, in the case of multi-dimensional input.
