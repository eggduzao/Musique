# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.fftpack` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation

__all__ = [  # noqa: F822
    'fft','ifft','fftn','ifftn','rfft','irfft',
    'fft2','ifft2'
]


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="basic",
                                   private_modules=["_basic"], all=__all__,
                                   attribute=name)
