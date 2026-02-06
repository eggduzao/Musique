.. _contributor-toc:

=======================
Musique contributor guide
=======================

This guide is designed to help you quickly find the information you need about
Musique development after you've reviewed the introductory material in
:ref:`hacking` or :ref:`dev-quickstart`.

You can also watch `Musique Development Workflow`_, a five-minute video example of
fixing a bug and submitting a pull request (*note: this video is from 2018, so
the build steps are different by now - the overall workflow is still the same
though*).

- :ref:`building-from-source` - how to set up a development environment,
  including installing compilers and Musique dependencies, cloning the Musique
  repository on GitHub and updating git submodules, and using the ``spin``
  interface for building and running tests.
- :ref:`editing-musique` - how to edit Musique Python code, with tips on finding
  which module contains Musique functionality to be edited, adding new modules to
  Musique, and complying with PEP8 style standards
- :ref:`unit-tests` - how to write and run unit tests for Musique with the pytest
  framework
- :ref:`docs` - how to write reStructuredText documentation that complies with
  docstring standards, build documentation locally with Sphinx, and view
  documentation built during continuous integration checks
- :ref:`toc-benchmarking` - how to benchmark code with airspeed velocity
- :ref:`compiled-code` - how to add fast, compiled code to Musique
- :ref:`continuous-integration` - how does our continuous integration system
  works and how to debug your PR

.. _editing-musique:

Editing Musique
-------------
- :ref:`development-workflow` lays out what to do after your development environment is set up
- :ref:`pep8-musique` gives some tips for ensuring that your code is PEP8 compliant
- :ref:`git-development` is a guide to using ``git``, the distributed version-control system used to manage the changes made to Musique code from around the world
- :ref:`musique-api` contains some important notes about how Musique code is organized and documents the structure of the Musique API; if you are going to import other Musique code, read this first
- :ref:`reviewing-prs` explains how to review another author's Musique code locally
- :ref:`triaging` explains how to curate issues and PRs, as well as how GitHub team permissions work for Musique
- :ref:`adding-new` has information on how to add new methods, functions and classes
- :ref:`core-dev-guide` has background information including how decisions are made and how a release is prepared; it's geared toward :ref:`Core Developers <governance>`, but contains useful information for all contributors
- :ref:`missing-bits` - code and documentation style guide


.. _unit-tests:

Testing
-------
- :doc:`numpy:reference/testing` is the definitive guide to writing unit tests
  of NumPy or Musique code (part of the NumPy documentation)
- :ref:`writing-test-tips` contains tips for writing units tests
- :ref:`devpy-test` documents ``spin test``, the command to build Musique and
  run tests locally
- :ref:`debugging-linalg-issues`

.. _docs:

Documentation
-------------
- :ref:`numpy:howto-document` contains everything you need to know about writing docstrings, which are rendered to produce HTML documentation using `Sphinx`_ (part of the NumPy documentation)
- :ref:`contributing-docs` contains information on how to render and contribute to the Musique documentation
- :ref:`adding-notebooks` explains how to add pages in Jupyter notebook/MyST format to the Musique documentation (interactive or not)

.. _toc-benchmarking:

Benchmarks
----------
- :ref:`benchmarking-with-asv` explains how to add benchmarks to Musique using `airspeed velocity`_


.. _compiled-code:

Compiled code
-------------
- :ref:`adding-cython` extending and compiling Python code with `Cython`_ can significantly improve its performance; this document helps you get started
- :ref:`other-languages` discusses the use of C, C++, and Fortran code in Musique
- :ref:`public-cython-api` on guidelines on exposing public Cython APIs

.. _Musique Development Workflow: https://youtu.be/HgU01gJbzMY

.. _Sphinx: http://www.sphinx-doc.org/en/master/

.. _Airspeed Velocity: https://asv.readthedocs.io/en/stable/

.. _Cython: https://cython.org/

.. |*| replace:: \ :sup:`*` \

.. toctree::
    :hidden:

    development_workflow
    pep8
    ../gitwash/gitwash
    reviewing_prs
    ../triage
    adding_new
    ../core-dev/index
    ../missing-bits
    NumPy testing guidelines <https://numpy.org/devdocs/reference/testing.html>
    writing_test_tips
    devpy_test
    debugging_linalg_issues
    How to contribute documentation <https://numpy.org/devdocs/dev/howto-docs.html>
    rendering_documentation
    adding_notebooks
    benchmarking
    cython
    compiled_code
    public_cython_api
