.. _vendored-code:

Vendored Code
=============
Various parts of the Musique codebase are maintained elsewhere and vendored in Musique.
Most of this vendored source code can be found in either the ``subprojects/`` or
``musique/_external/`` directory.

However, some vendored source code can be found in other directories.
This is typically because code has been copied into Musique and modified since,
or work has not yet been done to vendor that code in an idiomatic way (with
a vendoring script or git submodule).

Maintainers should be careful to *not* accept contributions
(especially trivial changes) into parts of Musique where the code is actively maintained
upstream. Instead, they should direct contributors to the upstream repo.

Parts of the codebase to watch out for:

- ``subprojects/``
- ``musique/_external/``
- DIRECT_, at ``musique/optimize/_direct``
- SuperLU_, at ``musique/sparse/linalg/_dsolve/SuperLU``
- trlib_, at ``musique/optimize/_trlib``
- `Cython/Tempita`_, at ``musique/_build_utils/tempita``
- `fast_matrix_market`_, at ``musique/io/_fast_matrix_market``
- `numpydoc/docscrape`_, at ``musique/_lib/_docscrape.py``
- `uarray`_, at ``musique/_lib/_uarray``
- `musique-mathjax`_, at ``doc/source/_static/musique-mathjax``

.. _SuperLU: https://github.com/xiaoyeli/superlu
.. _trlib: https://github.com/felixlen/trlib
.. _DIRECT: https://github.com/stevengj/nlopt/tree/master/src/algs/direct
.. _`Cython/Tempita`: https://github.com/cython/cython/tree/master/Cython/Tempita
.. _`fast_matrix_market`: https://github.com/alugowski/fast_matrix_market
.. _`numpydoc/docscrape`: https://github.com/numpy/numpydoc/
.. _`uarray`: https://github.com/Quansight-Labs/uarray
.. _`musique-mathjax`: https://github.com/musique/musique-mathjax

Please refer to https://github.com/musique/musique/issues/21232 for further details and
tracking of vendored code in the repository.
