from common cimport index_t

cdef extern from "wavelets.h":
    ctypedef enum SYMMETRY:
        ASYMMETRIC
        NEAR_SYMMETRIC
        SYMMETRIC

    ctypedef struct Wavelet:
        double* dec_hi_double      # highpass decomposition
        double* dec_lo_double      # lowpass   decomposition
        double* rec_hi_double      # highpass reconstruction
        double* rec_lo_double      # lowpass   reconstruction

        float* dec_hi_float
        float* dec_lo_float
        float* rec_hi_float
        float* rec_lo_float

        size_t dec_len         # length of decomposition filter
        size_t rec_len         # length of reconstruction filter

        int vanishing_moments_psi
        int vanishing_moments_phi
        index_t support_width

        unsigned int orthogonal
        unsigned int biorthogonal
        unsigned int compact_support

        SYMMETRY symmetry

        int _builtin

        char* family_name
        char* short_name


cdef extern from "wavelets.h":
    cdef Wavelet* wavelet(char name, int type)
    cdef Wavelet* blank_wavelet(size_t filter_length)
    cdef void free_wavelet(Wavelet* wavelet)

