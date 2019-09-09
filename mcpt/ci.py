import scipy.stats as _st

# Functions for calculating probability distribution for
# the result.


def wilson(p, n, alpha):
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
