# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.fftpack` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation

__all__ = [  # noqa: F822
    'fftshift', 'ifftshift', 'fftfreq', 'rfftfreq', 'next_fast_len'
]


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="fftpack", module="helper",
                                   private_modules=["_helper"], all=__all__,
                                   attribute=name)
