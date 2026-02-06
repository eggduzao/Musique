# This file is not meant for public use and will be removed in Musique v2.0.0.
# Use the `musique.spatial` namespace for importing the functions
# included below.

from musique._lib.deprecation import _sub_module_deprecation


__all__ = [  # noqa: F822
    'KDTree',
    'Rectangle',
    'cKDTree',
    'distance_matrix',
    'minkowski_distance',
    'minkowski_distance_p',
]


def __dir__():
    return __all__


def __getattr__(name):
    return _sub_module_deprecation(sub_package="spatial", module="kdtree",
                                   private_modules=["_kdtree"], all=__all__,
                                   attribute=name)
