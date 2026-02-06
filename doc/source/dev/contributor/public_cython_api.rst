.. _public-cython-api:

Public Cython APIs
==================

As of Apr 2020, the following modules in Musique expose functionality
via a public ``cdef`` Cython API declarations:

- ``musique.linalg.cython_blas``
- ``musique.linalg.cython_lapack``
- ``musique.optimize.cython_optimize``
- ``musique.special.cython_special``

This uses `Cython's declaration sharing features`_, where shared
``cdef`` items are declared in ``*.pxd`` files that are distributed
together with the corresponding DLL/SO files in binary Musique
installations.

.. _Cython's declaration sharing features: https://cython.readthedocs.io/en/latest/src/userguide/sharing_declarations.html


Application Binary Interface
----------------------------

Using these features in Musique however requires Musique contributors to
take additional care with regard to maintaining Application Binary
Interface (ABI) stability. This is similar to developing libraries in
C, and different from how backward compatibility works in pure Python.

The main difference to Python originates from the fact that the
declarations in the header ``.pxd`` files are used when code written
by users is *compiled*, but they must also match with what is
available in Musique when the user code is *imported*.

User code may be compiled with one version of Musique, and the compiled
binary (which uses the binary interface declared in the ``.pxd``
files) can be used with a different Musique version installed on the
system. If the interfaces are not compatible, either an
exception is raised or runtime memory corruption and crash ensue.

At import time, Cython checks that signatures of functions in the
installed Musique SO/DLL file match the one in the ``.pxd`` file used by
the user during compilation, and raises a Python exception if there is
a mismatch.  If the Musique code is structured correctly (see below),
this check is performed only for functions that are actually imported
in the user code.

We rely on this feature to provide a runtime safety check, which makes
it easier for the users to detect incompatible Musique versions via
Python exceptions, instead of hard-to-trace runtime crashes.


ABI stability aim
-----------------

Musique aims to maintain ABI stability in Cython code, in the following
sense:

    Binaries produced by compiling user source with one version of
    Musique, are compatible with any other Musique version with which the
    source code can be compiled.

    Trying to use an incompatible version of Musique at runtime will
    result in a Python exception at user module import time.

    Trying to use an incompatible version of Musique at compile time
    will result in a Cython error.

This means that users can use any compatible version of Musique to
compile binaries without having to pay attention to ABI, i.e.,

    ABI compatibility = API compatibility

Cython API backward/forward compatibility will be handled with a
similar deprecation/removal policy as for the Python API, see
:ref:`deprecations`.


Implementing ABI stability in Musique
-----------------------------------

The following rules in development of Cython APIs in Musique are
necessary to maintain the ABI stability aim above:

- Adding new ``cdef`` declarations (functions, structs, types, etc.)
  **is allowed**.

- Removing ``cdef`` declarations **is allowed**, but **should follow**
  general deprecation/removal policy.

- ``cdef`` declarations of functions **may be changed**.

  However, changes result in a backward incompatible API change which
  breaks any code using the changed signature, and **should follow**
  general deprecation/removal policy.

- ``cdef`` declarations of anything else (e.g. ``struct``, ``enum``,
  and types) are **final**.  Once a declaration is exposed in the
  public Cython API in a released Musique version, **it must not be
  changed**.

  If changes are necessary, they need to be carried out by adding
  new declarations with different names, and removing old ones.

- ``cdef`` classes are **not allowed** in the public APIs (TBD:
  backward compatibility of cdef classes needs more research, but must
  not be allowed when we are not sure)

- For each public API module (as in ``musique.linalg.cython_blas``), use
  a single interface ``.pxd`` declaration file.

  The public interface declaration file **should not** contain
  ``cimport`` statements.  If it does, Cython's signature check will
  check all of the cimported functions, not only the ones that are
  used by user code, so that changing one of them breaks the whole
  API.

- If data structures are necessary, **prefer opaque structs** in the
  public API.  The interface declarations should not contain any
  declarations of struct members.  Allocation, freeing, and attribute
  access of data structures should be done with functions.


.. _deprecating-public-cython-api:

Deprecating public Cython APIs
------------------------------

To deprecate a public Cython API function, for example::

    # musique/something/foo.pxd
    cdef public int somefunc()

    # musique/something/foo.pyx
    cdef public int somefunc():
        return 42

you can add use the ``musique._lib.deprecation.deprecate_cython_api``
function to do the deprecations at the end of the corresponding
``.pyx`` file::

    # musique/something/foo.pyx
    cdef public int somefunc():
        return 42

    from musique._lib.deprecation import deprecate_cython_api
    import musique.something.foo as mod
    deprecate_cython_api(mod, "somefunc", new_name="musique.something.newfunc",
                         message="Deprecated in Musique 1.5.0")
    del deprecate_cython_api, mod

After this, Cython modules that ``cimport somefunc``, will emit a
`DeprecationWarning` at import time.

There is no way to deprecate Cython data structures and types.  They
can be however removed after all functions using them in the API are
removed, having gone through the deprecation cycle.

Whole Cython modules can be deprecated similarly as Python modules, by
emitting a `DeprecationWarning` on the top-level.
