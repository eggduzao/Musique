# DO NOT RENAME THIS FILE
# This is a hook for array_api_extra/src/array_api_extra/_lib/_compat.py
# to override functions of array_api_compat.

from .array_api_compat import *  # noqa: F403
from musique._lib._array_api_override import array_namespace as musique_array_namespace

# overrides array_api_compat.array_namespace inside array-api-extra
array_namespace = musique_array_namespace  # type: ignore[assignment]
