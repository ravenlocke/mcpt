import numpy as _np
import mcpt


def test_i():
    # From https://www.thoughtco.com/example-of-a-permutation-test-3997741
    # One sided (lower) should be 0.1,

    _np.random.seed(3919)

    x = [10, 9, 11]
    y = [12, 11, 13]
    f = "mean"
    n = 100_000
    side = "lower"

    result = mcpt.permutation_test(x, y, f, n, side)
    assert 0.1 >= result.lower
    assert 0.1 <= result.upper


def test_ii():
    # From https://www.thoughtco.com/example-of-a-permutation-test-3997741
    # Two sided should be 0.2

    _np.random.seed(3919)

    x = [10, 9, 11]
    y = [12, 11, 13]
    f = "mean"
    n = 100_000
    side = "both"

    result = mcpt.permutation_test(x, y, f, n, side)
    assert 0.2 >= result.lower
    assert 0.2 <= result.upper


def test_iii():
    x = [1]
    y = [0]
    # The difference for a "mean" test is 1 - 0 = 1
    # Through randomisation, we get the following pairs:
    #   - [1] & [0] (50% of the time, diff = 1)
    #   - [0] & [1] (50% of the time diff = -1)
    # Thus, 50% of the time we would expect a result at least as
    # extreme or greater than 1.0.
    _np.random.seed(3919)

    f = "mean"
    n = 100_000
    side = "greater"
    result = mcpt.permutation_test(x, y, f, n, side)
    assert 0.5 >= result.lower
    assert 0.5 <= result.upper


def test_iv():
    x = [1]
    y = [0]
    # The difference for a "mean" test is 1 - 0 = 1
    # Through randomisation, we get the following pairs:
    #   - [1] & [0] (50% of the time, diff = 1)
    #   - [0] & [1] (50% of the time diff = -1)
    # Thus, 100% of the time we would expect a result at least as
    # extreme or lower than 1.0.

    # Possible groupings here are:
    # 1 & 0 or 0 & 1.
    # Thus, 50% of the time we would expect a result at least this
    # extreme or greater.
    _np.random.seed(3919)

    f = "mean"
    n = 100_000
    side = "lower"
    result = mcpt.permutation_test(x, y, f, n, side)
    assert 1 >= result.lower
    assert 1 <= result.upper
