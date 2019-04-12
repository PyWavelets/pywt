---
title: 'PyWavelets: A Python package for wavelet analysis'
tags:
  - Python
  - wavelets
  - wavelet packets
  - discrete wavelet transform
  - continuous wavelet transform
  - computational harmonic analysis
authors:
  - name: Gregory R. Lee
    orcid: 0000-0001-8895-2740
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Ralf Gommers
    orcid: 0000-0002-0300-3333
    affiliation: "3, 4"
  - name: Filip Waselewski
    orcid: 0000-0003-0729-5879
    affiliation: 6
  - name: Kai Wohlfahrt
    orcid: 0000-0002-0970-5539
    affiliation: 5
  - name: Aaron O&#8217;Leary
    orcid: 0000-0003-1984-2323
    affiliation: 6
affiliations:
 - name: Department of Radiology, Cincinnati Children's Hospital Medical Center, Cincinnati, OH, USA
   index: 1
 - name: Department of Radiology, University of Cincinnati School of Medicine, Cincinnati, OH, USA
   index: 2
 - name: Scion, 49 Sala Street, Private Bag 3020, Rotorua 3046, New Zealand
   index: 3
 - name: FPInnovations, 2665 East Mall, Vancouver, BC V6T 1Z4, Canada
   index: 4
 - name: Department of Biochemistry, University of Cambridge, Old Addenbrookes Site, 80 Tennis Court Road, Cambridge, CB2 1GA, United Kingdom
   index: 5
 - name: None
   index: 6

date: 24 August 2018
bibliography: paper.bib
---

# Summary

Wavelets are a popular tool for computational harmonic analysis. They provide
localization in both the temporal (or spatial) domain as well as in the
frequency domain [@Daubechies1992]. A prominent feature is the ability to
perform a multiresolution analysis [@mallat2008wavelet]. The wavelet transform
of natural signals and images tends to have most of its energy concentrated in
a small fraction of the coefficients. This sparse representation property is
key to the good performance of wavelets in applications such as data
compression and denoising. For example, the wavelet transform is a key
component of the JPEG 2000 image compression standard.

``PyWavelets`` is a Python package implementing a number of n-dimensional
discrete wavelet transforms as well as the 1D continuous wavelet transform. A
wide variety of predefined wavelets are provided and it is possible for users
to specify custom wavelet filter banks. All discrete wavelet transforms are
implemented by convolution with finite impulse response filters. The required
up/downsampling convolutions are implemented in C for good performance.
Cython [@cython] is used to wrap the C code and implement axis-specific 1D
transformations based on the low-level C routines. All multi-dimensional
transforms are implemented in Python via separable application of the 1D
transforms. The API for ``PyWavelets`` was designed to be similar to Matlab's
wavelet toolbox and functions such as the 1D, 2D and 3D discrete wavelet
transforms are tested for accuracy vs. their Matlab counterparts. PyWavelets
has additional functionality not common in other wavelet toolboxes such as
support for dimension $n > 3$ and support for both real and complex-valued
data in either single or double precision. It is also possible to transform
only a subset of axes and to vary the wavelet and signal boundary extension
mode on a per-axis basis.

``PyWavelets`` was designed for use by scientists working within a range of
applications including time-series analysis, signal processing, image
processing and medical imaging. It has already been adopted as a required
or optional dependency by a number of other software projects. For example,
it has enabled wavelet-based image denoising in scikit-image [@scikit-image].
The Operator Discretization Library (ODL) [@odl] uses PyWavelets to enable
wavelet-based regularization in iterative inverse problems such as computed
tomography image reconstruction. Another related package which is independent
of ``PyWavelets`` is Kymatio, which implements the wavelet scattering
transform in 1D-3D [@kymatio]. The current implementation in Kymatio uses
non-separable 2D and 3D wavelets defined in the frequency domain and is well
suited to signal classification tasks, but does not have a simple inverse
transform like the standard discrete wavelet transform.

A number of common 1D demo signals used in the literature and in the manuscript
by Stephan Mallat [-@mallat2008wavelet] are provided for use in teaching and for
purposes of reproducible research.

# Acknowledgements

We would to acknowledge the various PyWavelets contributors for their
contributions to the library, and specifically Holger Nahrstaedt for
contributing a continuous wavelet transform.

# References
