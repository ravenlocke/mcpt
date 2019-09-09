try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib

    matplotlib.use("agg")
    import matplotlib.pyplot as plt


def plot_histogram(x, x0, outfile, side):
    ax = plt.hist(x, bins=25)
    plt.axvline(x0, c="r", alpha=0.5, linestyle="--")
    plt.xlabel(
        "{}ifference in test statistic".format("Absolute d" if side == "both" else "D")
    )
    plt.ylabel("Frequency")
    plt.savefig(outfile)
    plt.close()
