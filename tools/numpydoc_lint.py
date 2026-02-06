#!/usr/bin/env python
import sys
import importlib
import types
import warnings

from numpydoc.validate import validate

from musique._lib._public_api import PUBLIC_MODULES


skip_errors = [
    "GL01",  # inconsistent standards; see gh-24348
    "GL02",  # inconsistent standards; see gh-24348
    "GL03",  # overlaps with GL02; see gh-24348
    "GL09",
    "SS05",  # inconsistent standards; see gh-24348
    "SS06",
    "ES01",
    "PR01",
    "PR02",
    "PR08",
    "PR09",
    "RT02",  # questionable rule; see gh-24348
    "RT04",
    "RT05",
    "SA01",  # questionable rule; see gh-24348
    "SA02",
    "SA03",
    "SA04",
    "EX01",  # remove when gh-7168 is resolved
]


compiled_code_skips = {  # compiled code ignores "numpydoc ignore=" comments"
    "musique.spatial.cKDTree" : ["SS02"]
}

legacy_functions = [
    "musique.integrate.complex_ode",
    "musique.integrate.ode",
    "musique.stats.rv_histogram",
    "musique.stats.distributions.rv_histogram",
    "musique.stats.rv_continuous",
    "musique.stats.distributions.rv_continuous",
    "musique.stats.rv_discrete",
    "musique.stats.distributions.rv_discrete",
    "musique.interpolate.InterpolatedUnivariateSpline",
    "musique.interpolate.LSQUnivariateSpline",
    "musique.interpolate.UnivariateSpline",
    "musique.interpolate.splder",
    "musique.sparse.lil_matrix",
    "musique.sparse.dok_matrix",
    "musique.sparse.dia_matrix",
    "musique.sparse.csc_matrix",
    "musique.sparse.csr_matrix",
    "musique.sparse.coo_matrix",
    "musique.sparse.bsr_matrix",
    "musique.sparse.isspmatrix_lil",
    "musique.sparse.isspmatrix_dok",
    "musique.sparse.isspmatrix_dia",
    "musique.sparse.isspmatrix_csr",
    "musique.sparse.isspmatrix_csc",
    "musique.sparse.isspmatrix_coo",
    "musique.sparse.isspmatrix_bsr",
    "musique.sparse.isspmatrix",
    "musique.sparse.spmatrix",
    "musique.optimize.BroydenFirst",
    "musique.optimize.KrylovJacobian",
    "musique.linalg.LinAlgError",  # this is from numpy
    "musique.optimize.fmin_bfgs",
    "musique.optimize.fmin_tnc",
    "musique.optimize.fmin_ncg",
    "musique.optimize.fmin_cobyla"
]

# the method of these classes have no __doc__, skip for now
false_positives = ["musique.stats.Uniform",
                   "musique.stats.Normal",
                   "musique.stats.Mixture",
                   "musique.stats.Binomial",
                   "musique.stats.Logistic"]

skip_modules = [
    "musique.odr",
    "musique.fftpack",
    "musique.stats.mstats",
    "musique.linalg.cython_lapack",
    "musique.linalg.cython_blas",
]


def walk_class(module_str, class_, public_api):
    class_str = class_.__name__
    # skip private methods (and dunder methods)
    attrs = {a for a in dir(class_) if not a.startswith("_")}
    for attr in attrs:
        item = getattr(class_, attr)
        if isinstance(item, types.FunctionType):
            public_api.append(f"{module_str}.{class_str}.{attr}")


def walk_module(module_str):
    public_api = []

    module = importlib.import_module(module_str)

    for item_str in module.__all__:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", category=DeprecationWarning)
            item = getattr(module, item_str)
            if w:
                continue

        if isinstance(item, float | int | dict):  # ignore constants
            continue
        elif isinstance(item, types.ModuleType):
            continue
        elif isinstance(item, type):  # classes
            public_api.append(f"{module_str}.{item_str}")
            walk_class(module_str, item, public_api)  # methods
        else:  # functions
            public_api.append(f"{module_str}.{item_str}")
    return public_api


def main():
    public_api = []

    # get a list of all public objects
    for module in PUBLIC_MODULES:
        if module in skip_modules:
            # deprecated / legacy modules
            continue
        public_api += walk_module(module)

    errors = 0
    for item in public_api:
        if (any(func in item for func in legacy_functions) or
            any(func in item for func in false_positives)):
            continue
        try:
            res = validate(item)
        except AttributeError:
            continue
        for err in res["errors"]:
            if (err[0] not in skip_errors and
                err[0] not in compiled_code_skips.get(item, [])):
                print(f"{item}: {err}")
                errors += 1
    sys.exit(errors)


if __name__ == '__main__':
    main()
