**********************
FAQ
**********************

How does mcpt compare to the `mlxtend <http://rasbt.github.io/mlxtend/user_guide/evaluate/permutation_test/>`_ implementation?
-----------------------------------------------------------------------------------------------------------------------------------------------
This is a fair question, as a Google search for "permutation test Python" brings ``mlxtend``'s implementation up. I would like to start by saying that ``mlxtend`` is a great package, which I've used on a number of projects. However, there are a few reasons I would prefer ``mcpt`` over ``mlxtend`` for permutation testing. 

Firstly, I have a couple of concerns with the implementation of permutation test in ``mlxtend``. 

1. In the `source code <https://github.com/rasbt/mlxtend/blob/master/mlxtend/evaluate/permutation.py>`_ for the latest release (``9c044a9`` at the time of writing), it appears that the p-value returned is the probability of getting a more extreme (:math:`>`) result by chance. However, p-value should actually be the probability of getting a result `at least as extreme <https://en.wikipedia.org/wiki/Exact_test>`_ (:math:`\ge`).
2. ``mlxtend`` uses a single function for p-values in both correlations `and` comparing a test statistic in two groups. This is problematic, because the treatment of ``x`` and ``y`` is different in the two tests. In the correlation case, only ``y`` should be permuted `to create different pairs <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#Using_a_permutation_test>`_. However, ``mlxtend`` pools ``x`` and ``y`` together and randomizes both, meaning that new pairs such as :math:`(x_1, x_2)` are possible, which should not be the case.
3. Permutation tests from Monte Carlo sampling, due to randomisation, results in approximations of the p-value, which differ from run-to-run. It would be incorrect to state that an approximate p-value of 0.049 from one run is significant  with ``alpha = 0.05``, as randomness may make this value differ run-to-run. What is better is to return a confidence interval, and conclude significance if :math:`p_{upper} < 0.05` at a confidence that we're satisfied with (e.g. :math:`99.9\%`).
4. ``mlxtend.evalue.permutation_test`` uses combinations for ``method='exact'`` calculations. This does not work for correlations, because the order matters for correlation (i.e., which ``x`` is paired with which ``y``). For this reason, the result obtained for example 2 `in the documentation <http://rasbt.github.io/mlxtend/user_guide/evaluate/permutation_test/#example-2-calculating-the-p-value-for-correlation-analysis-pearsons-r>`_ is actually incorrect.

Test-driven development for ``mcpt`` means that we test our implementation against a number of use-cases before release.


The second set of reasons I would prefer ``mcpt`` over ``mlxtend`` are quality-of-life based.

1. We implement multiprocessing, allowing the use of multiple processors if desired and available.
2. Subjectively, we believe the combination of our documentation and implementation is more intuitive, flexible, and simple.
3. The use of confidence intervals rather than the approximate p-value from randomisation testing is i) easier to justify and ii) more scientifically sound. For example, in a study, you can report:

	"We used ``mcpt`` to calculate approximate p-values using a Monte Carlo permutation test. A result was deemed to be significant if the upper bound of a 99.9% confidence interval was < 0.05."