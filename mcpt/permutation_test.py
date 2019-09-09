import random as _rd
import multiprocessing as _mp

import numpy as _np

from mcpt import _GT, _LT, _BOTH, _RESULT
from mcpt.ci import wilson
from mcpt.plot import plot_histogram


# Handlers for the different sides.
def _greater(tup):
    combined, x_len, reference, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = f(x) - f(y)
    return diff >= reference, diff


def _lower(tup):
    combined, x_len, reference, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = f(x) - f(y)
    return diff <= reference, diff


def _both(tup):
    combined, x_len, reference, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = abs(f(x) - f(y))
    return diff >= reference, diff


def _job_hander(f, jobs, cores):
    if cores == 1:
        return map(f, jobs)

    with _mp.Pool(cores) as p:
        results = p.map(f, jobs)
    return results


# Main function.
def permutation_test(
    x, y, f, side, n=10000, confidence=0.99, plot=None, cores=1, seed=None
):
    if seed:
        rng = _rd.Random(seed)
    else:
        rng = _rd.Random()

    x_len = len(x)

    combined = list(x) + list(y)

    if callable(f):
        _f = f
    elif f == "mean":
        _f = _np.mean
    elif f == "median":
        _f = _np.median
    elif f == "stdev":
        _f = _np.std
    else:
        raise ValueError(
            "{} not valid for f -- must be a function, 'mean', 'median' or 'stdev'".format(
                f
            )
        )

    if side in _GT:
        diff = _f(x) - _f(y)
    elif side in _LT:
        diff = _f(x) - _f(y)
    elif side in _BOTH:
        diff = abs(_f(x) - _f(y))
    else:
        raise ValueError(
            "{} not valid for side -- should be 'greater', 'lower', or 'both'".format(
                side
            )
        )

    jobs = ((combined, x_len, diff, _f, rng.randint(0, 1e100)) for _ in range(n))

    if side in _GT:
        result = _job_hander(_greater, jobs, cores)
    elif side in _LT:
        result = _job_hander(_lower, jobs, cores)
    else:
        result = _job_hander(_both, jobs, cores)

    v = []
    p = 0

    for truth, val in result:
        p += truth
        v.append(val)

    p /= n

    if plot:
        plot_histogram(x=v, x0=diff, outfile=plot, side=side)

    lower, upper = wilson(p, n, confidence)
    return _RESULT(lower, upper, confidence)
