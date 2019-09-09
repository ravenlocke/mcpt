import random as _rd
import multiprocessing as _mp

import scipy.stats as _st

from mcpt import _GT, _LT, _BOTH, _RESULT
from mcpt.ci import wilson
from mcpt.plot import plot_histogram


def _correlation_greater(tup):
    x, y, stat_0, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(y)
    stat = f(x, y)
    return stat >= stat_0, stat


def _correlation_lower(tup):
    x, y, stat_0, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(y)
    stat = f(x, y)
    return stat <= stat_0, stat


def _correlation_both(tup):
    x, y, stat_0, f, seed = tup
    _rd.seed(seed)
    _rd.shuffle(y)
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


def correlation_permutation_test(
    x, y, f, side, n=10000, confidence=0.99, plot=None, cores=1, seed=None
):
    """This function carries out Monte Carlo permutation tests comparing whether the correlation between two variables is statistically significant

    :param x: An iterable of X values observed
    :param y: An iterable of Y values observed
    :param f: The function for calculating the relationship strength between X and Y
    :param side: The side to use for hypothesis testing
    :param n: The number of permutations to sample, defaults to 10000
    :type n: int, optional
    :param confidence: The probability that the true p-value is contained in the intervals returned, defaults to 0.99
    :type confidence: float, optional
    :param plot: The name of a file to draw a plot of permuted correlations to, defaults to None
    :type plot: str, optional
    :param cores: The number of logical CPUs to use, defaults to 1
    :type cores: int, optional
    :param seed: The seed for randomisation, defaults to None
    :type seed: int, optional
    :return: Named tuple containing upper and lower bounds of p-value at the given confidence
    """

    if seed:
        rng = _rd.Random(seed)
    else:
        rng = _rd.Random()

    if callable(f):
        _f = f
    elif f == "pearsonr":
        _f = _pearsonr
    elif f == "spearmanr":
        _f = _spearmanr
    else:
        raise ValueError(
            "{} not valid for f -- must be a function, 'pearsonr', or 'spearmanr'".format(
                f
            )
        )

    _x = list(x)
    _y = list(y)

    if side in _GT:
        stat_0 = _f(_x, _y)
    elif side in _LT:
        stat_0 = _f(_x, _y)
    elif side in _BOTH:
        stat_0 = abs(_f(_x, _y))
    else:
        raise ValueError(
            "{} not valid for side -- should be 'greater', 'lower', or 'both'".format(
                side
            )
        )

    jobs = ((_x[:], _y[:], stat_0, _f, rng.randint(0, 1e100)) for _ in range(n))

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
