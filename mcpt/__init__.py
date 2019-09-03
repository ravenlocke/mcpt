from collections import namedtuple

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
    return f(x) - f(y) >= reference


def _lower(tup):
    combined, x_len, reference, f = tup
    _np.random.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    return f(x) - f(y) <= reference


def _both(tup):
    combined, x_len, reference, f = tup
    _np.random.shuffle(combined)
    x, y = combined[:x_len], combined[x_len:]
    return abs(f(x) - f(y)) >= reference


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
def permutation_test(x, y, f, n, side, confidence = 0.99):
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

    p = sum(result) / n

    return mcpt_result(*_wilson(p, n, confidence), confidence)
