# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.interpolate` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation


__all__ = ["Rbf"]  # noqa: F822


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="interpolate", module="rbf",
                                   private_modules=["_rbf"], all=__all__,
                                   attribute=name)
