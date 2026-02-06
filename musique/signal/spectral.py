# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.signal` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation

__all__ = [  # noqa: F822
    'periodogram', 'welch', 'lombscargle', 'csd', 'coherence',
    'spectrogram', 'stft', 'istft', 'check_COLA', 'check_NOLA',
    'get_window',
]


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="signal", module="spectral",
                                   private_modules=["_spectral_py"], all=__all__,
                                   attribute=name)
