import mcpt


def test_i():
    # From https://www.thoughtco.com/example-of-a-permutation-test-3997741
    # One sided (lower) should be 0.1,

    x = [10, 9, 11]
    y = [12, 11, 13]
    f = "mean"
    n = 100000
    side = "lower"

    result = mcpt.permutation_test(x, y, f, side, n=n, seed=3919)
    assert 0.1 >= result.lower
    assert 0.1 <= result.upper


def test_ii():
    # From https://www.thoughtco.com/example-of-a-permutation-test-3997741
    # Two sided should be 0.2

    x = [10, 9, 11]
    y = [12, 11, 13]
    f = "mean"
    n = 100000
    side = "both"

    result = mcpt.permutation_test(x, y, f, side, n=n, seed=3919)
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

    f = "mean"
    n = 100000
    side = "greater"
    result = mcpt.permutation_test(x, y, f, side, n=n, seed=3919)
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

    f = "mean"
    n = 100000
    side = "lower"
    result = mcpt.permutation_test(x, y, f, side, n=n, seed=3919)
    assert 1 >= result.lower
    assert 1 <= result.upper


def test_v():
    # Taken from http://biol09.biol.umontreal.ca/PLcourses/Statistical_tests.pdf
    # True p-value calculated through exhaustive permutation of y.
    x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
    y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]

    expected = 0.0144144069664903

    f = "pearsonr"
    n = 100000
    side = "greater"
    result = mcpt.correlation_permutation_test(x, y, f, side, n=n, seed=4919)

    assert expected >= result.lower
    assert expected <= result.upper


def test_vi():
    # Taken from http://biol09.biol.umontreal.ca/PLcourses/Statistical_tests.pdf
    # True p-value calculated through exhaustive permutation of y.
    x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
    y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]

    expected = 0.025554177689594355

    f = "pearsonr"
    n = 100000
    side = "both"
    result = mcpt.correlation_permutation_test(x, y, f, side, n=n, seed=4919)

    assert expected >= result.lower
    assert expected <= result.upper


def test_vii():
    # From https://www.thoughtco.com/example-of-a-permutation-test-3997741
    # One sided (lower) should be 0.1,

    x = [10, 9, 11]
    y = [12, 11, 13]
    f = "mean"
    n = 100000
    side = "lower"

    result = mcpt.permutation_test(x, y, f, side, n=n, cores=2, seed=4919)
    assert 0.1 >= result.lower
    assert 0.1 <= result.upper


def test_viii():
    # Taken from http://biol09.biol.umontreal.ca/PLcourses/Statistical_tests.pdf
    # True p-value calculated through exhaustive permutation of y.
    x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
    y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]

    expected = 0.025554177689594355

    f = "pearsonr"
    n = 100000
    side = "both"
    result = mcpt.correlation_permutation_test(x, y, f, side, n=n, cores=2, seed=4919)

    assert expected >= result.lower
    assert expected <= result.upper


def test_ix():
    # Test that seeding works.
    x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
    y = [ -1.28, 1.04, -1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05,]

    seed = 4919
    n = 10000
    for side in ["greater", "lower", "both"]:
        for cores in [1, 2]:
            result_a = mcpt.permutation_test(
                x, y, "mean", side, n=n, cores=cores, seed=seed
            )
            result_b = mcpt.permutation_test(
                x, y, "mean", side, n=n, cores=cores, seed=seed
            )
            result_c = mcpt.permutation_test(
                x, y, "mean", side, n=n, cores=cores)
            result_d = mcpt.permutation_test(
                x, y, "mean", side, n=n, cores=cores)
            
            assert (result_a == result_b) 
            assert (result_a != result_c)
            assert (result_a != result_d)
            assert (result_c != result_d)

            result_a = mcpt.correlation_permutation_test(
                x, y, "pearsonr", side, n=n, cores=cores, seed=seed
            )
            result_b = mcpt.correlation_permutation_test(
                x, y, "pearsonr", side, n=n, cores=cores, seed=seed
            )
            result_c = mcpt.correlation_permutation_test(
                x, y, "pearsonr", side, n=n, cores=cores
            )
            result_c = mcpt.correlation_permutation_test(
                x, y, "pearsonr", side, n=n, cores=cores
            )

            assert (result_a == result_b) 
            assert (result_a != result_c)
            assert (result_a != result_d)
            assert (result_c != result_d)

def test_x():
    from scipy.stats import kendalltau

    x = [4.02, 4.52, 4.79, 4.89, 5.27, 5.63, 5.89, 6.08, 6.13, 6.19, 6.47]
    y = [4.56, 2.92, 2.71, 3.34, 3.53, 3.47, 3.20, 4.51, 3.76, 3.77, 4.03]

    def ktau(x, y):
        tau, _ = kendalltau(x, y)
        return tau

    result = mcpt.correlation_permutation_test(x, y, side="both", f=ktau)
    assert result.lower <= 0.1646
    assert result.upper >= 0.1646 