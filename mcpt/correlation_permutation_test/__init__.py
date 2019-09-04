import multiprocessing as _mp

import numpy as _np
import scipy.stats as _st

from mcpt import _GT, _LT, _BOTH, _RESULT
from mcpt.ci import wilson
from mcpt.plot import plot_histogram


def _correlation_greater(tup):
    x, y, stat_0, f, seed = tup
    _np.random.seed(seed)
    _np.random.shuffle(y)
    stat = f(x, y)
    return stat >= stat_0, stat


def _correlation_lower(tup):
    x, y, stat_0, f, seed = tup
    _np.random.seed(seed)
    _np.random.shuffle(y)
    stat = f(x, y)
    return stat <= stat_0, stat


def _correlation_both(tup):
    x, y, stat_0, f, seed = tup
    _np.random.seed(seed)
    _np.random.shuffle(y)
    stat = abs(f(x, y))
    return stat >= stat_0, stat



def _pearsonr(x, y):
    return _st.pearsonr(x, y)[0]


def _spearmanr(x, y):
    return _st.spearmanr(x, y)[0]



def _job_hander(f, jobs, cores):
    if cores == 1:
        return map(f, jobs)

    with _mp.Pool(cores) as p:
        results = p.map(f, jobs)

    return results



def correlation_permutation_test(x, y, f, side, n=10000, confidence=0.99, plot=None, cores=1,
    seed=None):

    rng = _np.random.RandomState(seed)

    if callable(f):
        _f = f
    elif f == "pearsonr":
        _f = _pearsonr
    elif f == "spearmanr":
        _f = _spearmanr
    else:
        raise ValueError("{} not valid for f -- must be a function, 'pearsonr', or 'spearmanr'".format(f))

    if side in _GT:
        stat_0 = _f(x, y)
    elif side in _LT:
        stat_0 = _f(x, y)
    elif side in _BOTH:
        stat_0 = abs(_f(x, y))
    else:
        raise ValueError("{} not valid for side -- should be 'greater', 'lower', or 'both'".format(side))

    jobs = ((x[:], y[:], stat_0, _f, rng.randint(0, 4294967295)) for _ in range(n))

    if side in _GT:
        result = _job_hander(_correlation_greater, jobs, cores)
    elif side in _LT:
        result = _job_hander(_correlation_lower, jobs, cores)
    else:
        result = _job_hander(_correlation_both, jobs, cores)


    v = []
    p = 0

    for truth, val in result:
        p += truth
        v.append(val)

    p /= n

    if plot:
        plot_histogram(x=v, x0=stat_0, outfile=plot, side=side)

    lower, upper = wilson(p, n, confidence)
    return _RESULT(lower, upper, confidence)
