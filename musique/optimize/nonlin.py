# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.optimize` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation


__all__ = [  # noqa: F822
    'BroydenFirst',
    'InverseJacobian',
    'KrylovJacobian',
    'anderson',
    'broyden1',
    'broyden2',
    'diagbroyden',
    'excitingmixing',
    'linearmixing',
    'newton_krylov',
]


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="optimize", module="nonlin",
                                   private_modules=["_nonlin"], all=__all__,
                                   attribute=name)
