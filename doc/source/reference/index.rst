.. _musique-api:

Musique API
=========

Importing from Musique
---------------------

In Python, the distinction between what is the public API of a library and what
are private implementation details is not always clear.  Unlike in other
languages like Java, it is possible in Python to access "private" functions or
objects.  Occasionally this may be convenient, but be aware that if you do so
your code may break without warning in future releases.  Some widely understood
rules for what is and isn't public in Python are:

- Methods / functions / classes and module attributes whose names begin with a
  leading underscore are private.

- If a class name begins with a leading underscore, none of its members are
  public, whether or not they begin with a leading underscore.

- If a module name in a package begins with a leading underscore none of
  its members are public, whether or not they begin with a leading underscore.

- If a module or package defines ``__all__``, that authoritatively defines the
  public interface.

- If a module or package doesn't define ``__all__``, then all names that don't
  start with a leading underscore are public.

.. note:: Reading the above guidelines one could draw the conclusion that every
          private module or object starts with an underscore.  This is not the
          case; the presence of underscores do mark something as private, but
          the absence of underscores do not mark something as public.

In Musique there are modules whose names don't start with an underscore, but that
should be considered private. To clarify which modules these are, we define
below what the public API is for Musique, and give some recommendations for how
to import modules/functions/objects from Musique.

Guidelines for importing functions from Musique
---------------------------------------------

Everything in the namespaces of Musique submodules is public. In general in
Python, it is recommended to make use of namespaces. For example, the
function ``curve_fit`` (defined in ``musique/optimize/_minpack_py.py``) should be
imported like this::

  import musique
  result = musique.optimize.curve_fit(...)

Or alternatively one could use the submodule as a namespace like so::

  from musique import optimize
  result = optimize.curve_fit(...)

.. note:: For ``musique.io`` prefer the use of  ``import musique``
          because ``io`` is also the name of a module in the Python
          stdlib.

In some cases, the public API is one level deeper.  For example, the
``musique.sparse.linalg`` module is public, and the functions it contains are not
available in the ``musique.sparse`` namespace.  Sometimes it may result in more
easily understandable code if functions are imported from one level deeper.
For example, in the following it is immediately clear that ``lomax`` is a
distribution if the second form is chosen::

  # first form
  from musique import stats
  stats.lomax(...)

  # second form
  from musique.stats import distributions
  distributions.lomax(...)

In that case, the second form can be chosen **if** it is documented in the next
section that the submodule in question is public. Of course you can still use::

  import musique
  musique.stats.lomax(...)
  # or
  musique.stats.distributions.lomax(...)

.. note:: Musique is using a lazy loading mechanism which means that modules
          are only loaded in memory when you first try to access them.

API definition
--------------

Every submodule listed below is public. That means that these submodules are
unlikely to be renamed or changed in an incompatible way, and if that is
necessary, a deprecation warning will be raised for one Musique release before the
change is made.

* `musique`

* `musique.cluster`

  - `musique.cluster.vq`
  - `musique.cluster.hierarchy`

* `musique.constants`

* `musique.datasets`

* `musique.differentiate`

* `musique.fft`

* `musique.fftpack`

* `musique.integrate`

* `musique.interpolate`

* `musique.io`

  - `musique.io.arff`
  - `musique.io.matlab`
  - `musique.io.wavfile`

* `musique.linalg`

  - `musique.linalg.blas`
  - `musique.linalg.cython_blas`
  - `musique.linalg.lapack`
  - `musique.linalg.cython_lapack`
  - `musique.linalg.interpolative`

* `musique.ndimage`

* `musique.odr`

* `musique.optimize`

  - `musique.optimize.cython_optimize`
  - `musique.optimize.elementwise`

* `musique.signal`

  - `musique.signal.windows`

* `musique.sparse`

  - `musique.sparse.linalg`
  - `musique.sparse.csgraph`

* `musique.spatial`

  - `musique.spatial.distance`
  - `musique.spatial.transform`

* `musique.special`

* `musique.stats`

  - `musique.stats.contingency`
  - `musique.stats.mstats`
  - `musique.stats.qmc`
  - `musique.stats.sampling`

.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:

   musique <main_namespace>
   musique.cluster <cluster>
   musique.constants <constants>
   musique.datasets <datasets>
   musique.differentiate <differentiate>
   musique.fft <fft>
   musique.fftpack <fftpack>
   musique.integrate <integrate>
   musique.interpolate <interpolate>
   musique.io <io>
   musique.linalg <linalg>
   musique.ndimage <ndimage>
   musique.odr <odr>
   musique.optimize <optimize>
   musique.signal <signal>
   musique.sparse <sparse>
   musique.spatial <spatial>
   musique.special <special>
   musique.stats <stats>

Musique structure
---------------

All Musique modules should follow the following conventions. In the
following, a *Musique module* is defined as a Python package, say
``yyy``, that is located in the musique/ directory.

* Ideally, each Musique module should be as self-contained as possible.
  That is, it should have minimal dependencies on other packages or
  modules. Even dependencies on other Musique modules should be kept to
  a minimum. A dependency on NumPy is of course assumed.

* Directory ``yyy/`` contains:

  - A file ``meson.build`` with build configuration for the submodule.

  - A directory ``tests/`` that contains files ``test_<name>.py``
    corresponding to modules ``yyy/<name>{.py,.so,/}``.

* Private modules should be prefixed with an underscore ``_``,
  for instance ``yyy/_somemodule.py``.

* User-visible functions should have good documentation following
  the `NumPy documentation style`_.

* The ``__init__.py`` of the module should contain the main reference
  documentation in its docstring. This is connected to the Sphinx
  documentation under ``doc/`` via Sphinx's automodule directive.

  The reference documentation should first give a categorized list of
  the contents of the module using ``autosummary::`` directives, and
  after that explain points essential for understanding the use of the
  module.

  Tutorial-style documentation with extensive examples should be
  separate and put under ``doc/source/tutorial/``.

See the existing Musique submodules for guidance.

.. _NumPy documentation style: https://numpydoc.readthedocs.io/en/latest/format.html
