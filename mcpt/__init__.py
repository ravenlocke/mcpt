from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as _np
import scipy.stats as _st

_GT = {"g", "gt", ">", "greater"}
_LT = {"l", "lt", "<", "lower"}
_BOTH = {"both"}

mcpt_result = namedtuple("Result", ["lower", "upper", "confidence"])

# Handlers for the different sides.
def _greater(tup):
    combined, x_len, reference, f = tup
    _np.random.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = f(x) - f(y)
    return diff >= reference, diff


def _lower(tup):
    combined, x_len, reference, f = tup
    _np.random.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = f(x) - f(y)
    return diff <= reference, diff


def _both(tup):
    combined, x_len, reference, f = tup
    _np.random.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    diff = abs(f(x) - f(y))

    return diff >= reference, diff

def _correlation_greater(tup):
    x, y, stat_0, f = tup
    _np.random.shuffle(y)
    stat = f(x, y)
    return stat >= stat_0, stat

def _correlation_lower(tup):
    x, y, stat_0, f = tup
    _np.random.shuffle(y)
    stat = f(x, y)
    return stat <= stat_0, stat

def _correlation_both(tup):
    x, y, stat_0, f = tup
    _np.random.shuffle(y)
    stat = abs(f(x, y))
    return stat >= stat_0, stat

# Functions for calculating probability distribution for
# the result.


def _wilson(p, n, alpha):
    # Convert alpha to Z-score.
    # We want 1 - alpha proportion of values contained.
    z = _st.norm.ppf((1 - alpha) / 2 + alpha)
    # Calculate lower and upper bounds
    lower = (p + z * z / (2 * n) - z * ((p * (1 - p) + z * z / (4 * n)) / n) ** 0.5) / (
        1 + z * z / n
    )
    upper = (p + z * z / (2 * n) + z * ((p * (1 - p) + z * z / (4 * n)) / n) ** 0.5) / (
        1 + z * z / n
    )

    return (lower, upper)


# Main function.
def permutation_test(x, y, f, side, n=10_000, confidence=0.99, plot=None):
    x_len = len(x)
    combined = list(x) + list(y)
    _np.random.shuffle(combined)

    if callable(f):
        _f = f
    elif f == "mean":
        _f = _np.mean
    elif f == "median":
        _f = _np.median
    elif f == "stdev":
        _f = _np.std
    else:
        raise Exception

    if side in _GT:
        diff = _f(x) - _f(y)
    elif side in _LT:
        diff = _f(x) - _f(y)
    elif side in _BOTH:
        diff = abs(_f(x) - _f(y))
    else:
        raise Exception("side is not valid")

    jobs = ((combined, x_len, diff, _f) for _ in range(n))

    if side in _GT:
        result = map(_greater, jobs)
    elif side in _LT:
        result = map(_lower, jobs)
    elif side in _BOTH:
        result = map(_both, jobs)
    else:
        raise Exception("side is not valid")

    v = []
    p = 0

    for truth, val in result:
        p += truth
        v.append(val)

    p /= n

    if plot:
        ax = plt.hist(v, bins=25)
        plt.axvline(diff, c="r", alpha=0.5, linestyle="--")
        plt.xlabel(f'{"Absolute " if side=="both" else ""}difference in test statistic')
        plt.ylabel("Frequency")
        plt.savefig(plot)

    return mcpt_result(*_wilson(p, n, confidence), confidence)

def _pearsonr(x, y):
    return _st.pearsonr(x, y)[0]

def _spearmanr(x, y):
    return _st.spearmanr(x, y)[0]

def correlation_permutation_test(x, y, f, side, n=10_000, confidence=0.99, plot=None):
    if callable(f):
        _f = f
    elif f == "pearsonr":
        _f = _pearsonr
    elif f == "spearmanr":
        _f = _spearmanr
    else:
        raise Exception

    if side in _GT:
        stat_0 = _f(x, y)
    elif side in _LT:
        stat_0 = _f(x, y)
    elif side in _BOTH:
        stat_0 = abs(_f(x, y))
    else:
        raise Exception("side is not valid")


    jobs = ((x, y, stat_0, _f) for _ in range(n))

    if side in _GT:
        result = map(_correlation_greater, jobs)
    elif side in _LT:
        result = map(_correlation_lower, jobs)
    elif side in _BOTH:
        result = map(_correlation_both, jobs)
    else:
        raise Exception("side is not valid")

    v = []
    p = 0

    for truth, val in result:
        p += truth
        v.append(val)

    p /= n

    if plot:
        ax = plt.hist(v, bins=25)
        print(stat_0)
        plt.axvline(stat_0, c="r", alpha=0.5, linestyle="--")
        plt.xlabel(f'{"Absolute d" if side=="both" else "D"}ifference in test statistic')
        plt.ylabel("Frequency")
        plt.savefig(plot)

    return mcpt_result(*_wilson(p, n, confidence), confidence)