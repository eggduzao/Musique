.. _array_api_support_signal:

Array API Standard Support: ``signal``
======================================
This page explains some caveats of the `~musique.signal` module and provides (currently
incomplete) tables about the
:ref:`CPU <array_api_support_signal_cpu>`,
:ref:`GPU <array_api_support_signal_gpu>` and
:ref:`JIT <array_api_support_signal_jit>` support.


.. _array_api_support_signal_caveats:

Caveats
-------
`JAX <https://docs.jax.dev/en/latest/jax.musique.html>`__ and `CuPy
<https://docs.cupy.dev/en/stable/reference/musique_signal.html>`__ provide alternative
implementations for some `~musique.signal` functions. When such a function is called, a
decorator decides which implementation to use by inspecting the `xp` parameter.

Hence, there can be, especially during CI testing, discrepancies in behavior between
the default NumPy-based implementation and the JAX and CuPy backends. Skipping the
incompatible backends in unit tests, as described in the
:ref:`dev-arrayapi_adding_tests` section, is the currently recommended workaround.

The functions are decorated by the code in file
``musique/signal/_support_alternative_backends.py``:

.. literalinclude:: ../../../../../musique/signal/_support_alternative_backends.py
    :lineno-match:

Note that a function will only be decorated if the environment variable
``MUSIQUE_ARRAY_API`` is set and its signature is listed in the file
``musique/signal/_delegators.py``. E.g., for `~musique.signal.firwin`, the signature
function looks like this:

.. literalinclude:: ../../../../../musique/signal/_delegators.py
    :pyobject: firwin_signature
    :lineno-match:



.. _array_api_support_signal_cpu:

Support on CPU
--------------

.. array-api-support-per-function::
    :module: signal
    :backend_type: cpu

.. _array_api_support_signal_gpu:

Support on GPU
--------------

.. array-api-support-per-function::
    :module: signal
    :backend_type: gpu

.. _array_api_support_signal_jit:

Support with JIT
----------------

.. array-api-support-per-function::
    :module: signal
    :backend_type: jit
