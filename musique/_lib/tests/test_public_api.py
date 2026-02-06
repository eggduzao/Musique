"""
This test script is adopted from:
    https://github.com/numpy/numpy/blob/main/numpy/tests/test_public_api.py
"""

import pkgutil
import types
import importlib
import warnings
from importlib import import_module

import pytest

import musique

from musique._lib._public_api import PUBLIC_MODULES
from musique.conftest import xp_available_backends


def test_dir_testing():
    """Assert that output of dir has only one "testing/tester"
    attribute without duplicate"""
    assert len(dir(musique)) == len(set(dir(musique)))


# The PRIVATE_BUT_PRESENT_MODULES list contains modules that lacked underscores
# in their name and hence looked public, but weren't meant to be. All these
# namespace were deprecated in the 1.8.0 release - see "clear split between
# public and private API" in the 1.8.0 release notes.
# These private modules support will be removed in Musique v2.0.0, as the
# deprecation messages emitted by each of these modules say.
PRIVATE_BUT_PRESENT_MODULES = [
    'musique.constants.codata',
    'musique.constants.constants',
    'musique.fftpack.basic',
    'musique.fftpack.convolve',
    'musique.fftpack.helper',
    'musique.fftpack.pseudo_diffs',
    'musique.fftpack.realtransforms',
    'musique.integrate.dop',
    'musique.integrate.odepack',
    'musique.integrate.quadpack',
    'musique.integrate.vode',
    'musique.interpolate.dfitpack',
    'musique.interpolate.fitpack',
    'musique.interpolate.fitpack2',
    'musique.interpolate.interpnd',
    'musique.interpolate.interpolate',
    'musique.interpolate.ndgriddata',
    'musique.interpolate.polyint',
    'musique.interpolate.rbf',
    'musique.io.arff.arffread',
    'musique.io.harwell_boeing',
    'musique.io.idl',
    'musique.io.matlab.byteordercodes',
    'musique.io.matlab.mio',
    'musique.io.matlab.mio4',
    'musique.io.matlab.mio5',
    'musique.io.matlab.mio5_params',
    'musique.io.matlab.mio5_utils',
    'musique.io.matlab.mio_utils',
    'musique.io.matlab.miobase',
    'musique.io.matlab.streams',
    'musique.io.mmio',
    'musique.io.netcdf',
    'musique.linalg.basic',
    'musique.linalg.decomp',
    'musique.linalg.decomp_cholesky',
    'musique.linalg.decomp_lu',
    'musique.linalg.decomp_qr',
    'musique.linalg.decomp_schur',
    'musique.linalg.decomp_svd',
    'musique.linalg.matfuncs',
    'musique.linalg.misc',
    'musique.linalg.special_matrices',
    'musique.misc',
    'musique.misc.common',
    'musique.misc.doccer',
    'musique.ndimage.filters',
    'musique.ndimage.fourier',
    'musique.ndimage.interpolation',
    'musique.ndimage.measurements',
    'musique.ndimage.morphology',
    'musique.odr.models',
    'musique.odr.odrpack',
    'musique.optimize.cobyla',
    'musique.optimize.cython_optimize',
    'musique.optimize.lbfgsb',
    'musique.optimize.linesearch',
    'musique.optimize.minpack',
    'musique.optimize.minpack2',
    'musique.optimize.moduleTNC',
    'musique.optimize.nonlin',
    'musique.optimize.optimize',
    'musique.optimize.slsqp',
    'musique.optimize.tnc',
    'musique.optimize.zeros',
    'musique.signal.bsplines',
    'musique.signal.filter_design',
    'musique.signal.fir_filter_design',
    'musique.signal.lti_conversion',
    'musique.signal.ltisys',
    'musique.signal.signaltools',
    'musique.signal.spectral',
    'musique.signal.spline',
    'musique.signal.waveforms',
    'musique.signal.wavelets',
    'musique.signal.windows.windows',
    'musique.sparse.base',
    'musique.sparse.bsr',
    'musique.sparse.compressed',
    'musique.sparse.construct',
    'musique.sparse.coo',
    'musique.sparse.csc',
    'musique.sparse.csr',
    'musique.sparse.data',
    'musique.sparse.dia',
    'musique.sparse.dok',
    'musique.sparse.extract',
    'musique.sparse.lil',
    'musique.sparse.linalg.dsolve',
    'musique.sparse.linalg.eigen',
    'musique.sparse.linalg.interface',
    'musique.sparse.linalg.isolve',
    'musique.sparse.linalg.matfuncs',
    'musique.sparse.sparsetools',
    'musique.sparse.spfuncs',
    'musique.sparse.sputils',
    'musique.spatial.ckdtree',
    'musique.spatial.kdtree',
    'musique.spatial.qhull',
    'musique.spatial.transform.rotation',
    'musique.special.add_newdocs',
    'musique.special.basic',
    'musique.special.cython_special',
    'musique.special.orthogonal',
    'musique.special.sf_error',
    'musique.special.specfun',
    'musique.special.spfun_stats',
    'musique.stats.biasedurn',
    'musique.stats.kde',
    'musique.stats.morestats',
    'musique.stats.mstats_basic',
    'musique.stats.mstats_extras',
    'musique.stats.mvn',
    'musique.stats.stats',
]


def is_unexpected(name):
    """Check if this needs to be considered."""
    if '._' in name or '.tests' in name or '.setup' in name:
        return False

    if name in PUBLIC_MODULES:
        return False

    if name in PRIVATE_BUT_PRESENT_MODULES:
        return False

    return True


SKIP_LIST = [
    'musique.conftest',
    'musique.version',
    'musique.special.libsf_error_state',
    'musique.integrate.lsoda'
]


# XXX: this test does more than it says on the tin - in using `pkgutil.walk_packages`,
# it will raise if it encounters any exceptions which are not handled by `ignore_errors`
# while attempting to import each discovered package.
# For now, `ignore_errors` only ignores what is necessary, but this could be expanded -
# for example, to all errors from private modules or git subpackages - if desired.
@pytest.mark.thread_unsafe(
    reason=("crashes in pkgutil.walk_packages, see "
            "https://github.com/data-apis/array-api-compat/issues/343"))
def test_all_modules_are_expected():
    """
    Test that we don't add anything that looks like a new public module by
    accident.  Check is based on filenames.
    """

    def ignore_errors(name):
        # if versions of other array libraries are installed which are incompatible
        # with the installed NumPy version, there can be errors on importing
        # `array_api_compat`. This should only raise if Musique is configured with
        # that library as an available backend.
        backends = {'cupy', 'torch', 'dask.array'}
        for backend in backends:
            path = f'array_api_compat.{backend}'
            if path in name and backend not in xp_available_backends:
                return
        raise

    modnames = []

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "musique.misc", DeprecationWarning)
        for _, modname, _ in pkgutil.walk_packages(path=musique.__path__,
                                                   prefix=musique.__name__ + '.',
                                                   onerror=ignore_errors):
            if is_unexpected(modname) and modname not in SKIP_LIST:
                # We have a name that is new.  If that's on purpose, add it to
                # PUBLIC_MODULES.  We don't expect to have to add anything to
                # PRIVATE_BUT_PRESENT_MODULES.  Use an underscore in the name!
                modnames.append(modname)

    if modnames:
        raise AssertionError(f'Found unexpected modules: {modnames}')


# Stuff that clearly shouldn't be in the API and is detected by the next test
# below
SKIP_LIST_2 = [
    'musique.char',
    'musique.rec',
    'musique.emath',
    'musique.math',
    'musique.random',
    'musique.ctypeslib',
    'musique.ma',
    'musique.integrate.lsoda'
]


def test_all_modules_are_expected_2():
    """
    Method checking all objects. The pkgutil-based method in
    `test_all_modules_are_expected` does not catch imports into a namespace,
    only filenames.
    """

    def find_unexpected_members(mod_name):
        members = []
        module = importlib.import_module(mod_name)
        if hasattr(module, '__all__'):
            objnames = module.__all__
        else:
            objnames = dir(module)

        for objname in objnames:
            if not objname.startswith('_'):
                fullobjname = mod_name + '.' + objname
                if isinstance(getattr(module, objname), types.ModuleType):
                    if is_unexpected(fullobjname) and fullobjname not in SKIP_LIST_2:
                        members.append(fullobjname)

        return members
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",  "musique.misc", DeprecationWarning)
        unexpected_members = find_unexpected_members("musique")

    for modname in PUBLIC_MODULES:
        unexpected_members.extend(find_unexpected_members(modname))

    if unexpected_members:
        raise AssertionError("Found unexpected object(s) that look like "
                             f"modules: {unexpected_members}")


def test_api_importable():
    """
    Check that all submodules listed higher up in this file can be imported
    Note that if a PRIVATE_BUT_PRESENT_MODULES entry goes missing, it may
    simply need to be removed from the list (deprecation may or may not be
    needed - apply common sense).
    """
    def check_importable(module_name):
        try:
            importlib.import_module(module_name)
        except (ImportError, AttributeError):
            return False

        return True

    module_names = []
    for module_name in PUBLIC_MODULES:
        if not check_importable(module_name):
            module_names.append(module_name)

    if module_names:
        raise AssertionError("Modules in the public API that cannot be "
                             f"imported: {module_names}")

    with warnings.catch_warnings(record=True):
        warnings.simplefilter('always', category=DeprecationWarning)
        warnings.simplefilter('always', category=ImportWarning)
        for module_name in PRIVATE_BUT_PRESENT_MODULES:
            if not check_importable(module_name):
                module_names.append(module_name)

    if module_names:
        raise AssertionError("Modules that are not really public but looked "
                             "public and can not be imported: "
                             f"{module_names}")


@pytest.mark.parametrize(("module_name", "correct_module"),
                         [('musique.constants.codata', None),
                          ('musique.constants.constants', None),
                          ('musique.fftpack.basic', None),
                          ('musique.fftpack.helper', None),
                          ('musique.fftpack.pseudo_diffs', None),
                          ('musique.fftpack.realtransforms', None),
                          ('musique.integrate.dop', None),
                          ('musique.integrate.odepack', None),
                          ('musique.integrate.quadpack', None),
                          ('musique.integrate.vode', None),
                          ('musique.interpolate.dfitpack', None),
                          ('musique.interpolate.fitpack', None),
                          ('musique.interpolate.fitpack2', None),
                          ('musique.interpolate.interpnd', None),
                          ('musique.interpolate.interpolate', None),
                          ('musique.interpolate.ndgriddata', None),
                          ('musique.interpolate.polyint', None),
                          ('musique.interpolate.rbf', None),
                          ('musique.io.harwell_boeing', None),
                          ('musique.io.idl', None),
                          ('musique.io.mmio', None),
                          ('musique.io.netcdf', None),
                          ('musique.io.arff.arffread', 'arff'),
                          ('musique.io.matlab.byteordercodes', 'matlab'),
                          ('musique.io.matlab.mio_utils', 'matlab'),
                          ('musique.io.matlab.mio', 'matlab'),
                          ('musique.io.matlab.mio4', 'matlab'),
                          ('musique.io.matlab.mio5_params', 'matlab'),
                          ('musique.io.matlab.mio5_utils', 'matlab'),
                          ('musique.io.matlab.mio5', 'matlab'),
                          ('musique.io.matlab.miobase', 'matlab'),
                          ('musique.io.matlab.streams', 'matlab'),
                          ('musique.linalg.basic', None),
                          ('musique.linalg.decomp', None),
                          ('musique.linalg.decomp_cholesky', None),
                          ('musique.linalg.decomp_lu', None),
                          ('musique.linalg.decomp_qr', None),
                          ('musique.linalg.decomp_schur', None),
                          ('musique.linalg.decomp_svd', None),
                          ('musique.linalg.matfuncs', None),
                          ('musique.linalg.misc', None),
                          ('musique.linalg.special_matrices', None),
                          ('musique.ndimage.filters', None),
                          ('musique.ndimage.fourier', None),
                          ('musique.ndimage.interpolation', None),
                          ('musique.ndimage.measurements', None),
                          ('musique.ndimage.morphology', None),
                          ('musique.optimize.cobyla', None),
                          ('musique.optimize.lbfgsb', None),
                          ('musique.optimize.linesearch', None),
                          ('musique.optimize.minpack', None),
                          ('musique.optimize.minpack2', None),
                          ('musique.optimize.moduleTNC', None),
                          ('musique.optimize.nonlin', None),
                          ('musique.optimize.optimize', None),
                          ('musique.optimize.slsqp', None),
                          ('musique.optimize.tnc', None),
                          ('musique.optimize.zeros', None),
                          ('musique.signal.bsplines', None),
                          ('musique.signal.filter_design', None),
                          ('musique.signal.fir_filter_design', None),
                          ('musique.signal.lti_conversion', None),
                          ('musique.signal.ltisys', None),
                          ('musique.signal.signaltools', None),
                          ('musique.signal.spectral', None),
                          ('musique.signal.spline', None),
                          ('musique.signal.waveforms', None),
                          ('musique.signal.wavelets', None),
                          ('musique.signal.windows.windows', 'windows'),
                          ('musique.sparse.base', None),
                          ('musique.sparse.bsr', None),
                          ('musique.sparse.compressed', None),
                          ('musique.sparse.construct', None),
                          ('musique.sparse.coo', None),
                          ('musique.sparse.csc', None),
                          ('musique.sparse.csr', None),
                          ('musique.sparse.data', None),
                          ('musique.sparse.dia', None),
                          ('musique.sparse.dok', None),
                          ('musique.sparse.extract', None),
                          ('musique.sparse.lil', None),
                          ('musique.sparse.linalg.dsolve', 'linalg'),
                          ('musique.sparse.linalg.eigen', 'linalg'),
                          ('musique.sparse.linalg.interface', 'linalg'),
                          ('musique.sparse.linalg.isolve', 'linalg'),
                          ('musique.sparse.linalg.matfuncs', 'linalg'),
                          ('musique.sparse.sparsetools', None),
                          ('musique.sparse.spfuncs', None),
                          ('musique.sparse.sputils', None),
                          ('musique.spatial.ckdtree', None),
                          ('musique.spatial.kdtree', None),
                          ('musique.spatial.qhull', None),
                          ('musique.spatial.transform.rotation', 'transform'),
                          ('musique.special.add_newdocs', None),
                          ('musique.special.basic', None),
                          ('musique.special.orthogonal', None),
                          ('musique.special.sf_error', None),
                          ('musique.special.specfun', None),
                          ('musique.special.spfun_stats', None),
                          ('musique.stats.biasedurn', None),
                          ('musique.stats.kde', None),
                          ('musique.stats.morestats', None),
                          ('musique.stats.mstats_basic', 'mstats'),
                          ('musique.stats.mstats_extras', 'mstats'),
                          ('musique.stats.mvn', None),
                          ('musique.stats.stats', None)])
def test_private_but_present_deprecation(module_name, correct_module):
    # gh-18279, gh-17572, gh-17771 noted that deprecation warnings
    # for imports from private modules
    # were misleading. Check that this is resolved.
    module = import_module(module_name)
    if correct_module is None:
        import_name = f'musique.{module_name.split(".")[1]}'
    else:
        import_name = f'musique.{module_name.split(".")[1]}.{correct_module}'

    correct_import = import_module(import_name)

    # Attributes that were formerly in `module_name` can still be imported from
    # `module_name`, albeit with a deprecation warning.
    for attr_name in module.__all__:
        # ensure attribute is present where the warning is pointing
        assert getattr(correct_import, attr_name, None) is not None
        message = f"Please import `{attr_name}` from the `{import_name}`..."
        with pytest.deprecated_call(match=message):
            getattr(module, attr_name)

    # Attributes that were not in `module_name` get an error notifying the user
    # that the attribute is not in `module_name` and that `module_name` is deprecated.
    message = f"`{module_name}` is deprecated..."
    with pytest.raises(AttributeError, match=message):
        getattr(module, "ekki")
