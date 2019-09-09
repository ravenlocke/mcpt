**********************
Quickstart
**********************


``mcpt`` comes with two main functions: ``permutation_test`` and ``correlation_permutation_test``.


Permutation test
================
This function takes values for two groups, ``X`` and ``Y``, and tests whether the labels on the members of the group are exchangable under the null hypothesis. 


For simplest use, the ``permutation_test`` function takes four arguments:

* ``x`` - An iterable of values for members of the 1st group.
* ``y`` - An iterable of values for members of the 2nd group.
* ``side`` - The side that we want to test under the null hypothesis 

* ``f`` - The function for calculating the test statistic



.. code-block:: python

	>>> import mcpt
	>>> treatment = [10, 9, 11]
	>>> control = [12, 11, 13]
	>>> side = "lower"
	>>> f = "mean"

	>>> result = mcpt.permutation_test(treatment, control, f=f, side=side)
	>>> print(result)
	Result(lower=0.09815650454064283, upper=0.10305649415095638, confidence=0.99)

In the above example, we are evaluating whether the mean of the samples in the ``treatment`` group is signifcantly lower than the mean of the samples in ``control`` group. 

Unlike an exhaustive permutation test, ``mcpt`` samples from the distribution of all possible permutations. Thus, the p-value obtained by ``mcpt`` is *approximate*, and will vary run-to-run; rather than returning the approximate p-value, therefore, ``mcpt`` returns upper and lower bounds that, with a given confidence, contains the true p-value. The default confidence is :math:`99\%`; see `this link <https://journals.sagepub.com/doi/full/10.1177/1094428118795272>`_ for more information on approximating p-values. 

In the above example, there is a :math:`99\%` probability that the p-value is between :math:`0.098` and :math:`0.103` -- thus, at an alpha of :math:`0.05`, we cannot reject the null hypothesis.

``f`` takes a string value (``"mean"``, ``"median"``, or ``"stdev"``) -- alternatively, a function can be passed (e.g. ``"numpy.mean"``). 

``side`` takes one of three values: ``"both"`` for a two-sided permutation test, or ``"greater"`` and ``"lower"`` for one-sided permutation tests.

For more advanced usage, see :ref:`permutation-test-advanced`.


Correlation permutation test
============================
This function takes a set of paired scores, :math:`(x_1, y_1), (x_2, y_2)...(x_i, y_i)`, and tests whether the pairings are exchangable under the null hypothesis.

For simplest use, the ``correlaton_permutation_test`` function takes four arguments:

* ``x`` - An iterable of the :math:`x` values for the pairs.
* ``y`` - An iterable of the :math:`y` values for the pairs.
* ``side`` - The side that we want to test under the null hypothesis
* ``f`` - The function for calculating the test statistic

.. code-block:: python

	>>> import mcpt
	>>> x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
	>>> y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]
	>>> side = "both"
	>>> f = "pearsonr"

	>>> result = mcpt.correlation_permutation_test(x, y, f=f, side=side)
	>>> print(result)
	Result(lower=0.021282451892029475, upper=0.029347445354757373, confidence=0.99)


In the above example, we determine that there is a :math:`99\%` probability that the p-value is between :math:`0.021` and :math:`0.029`. If we set an alpha value of :math:`0.05`, then it would be reasonable to reject the null hypothesis that the correlation is significantly different from :math:`\rho=0`.

``f`` takes a string value (``"pearsonr"`` or ``"spearmanr"``) -- alternatively, a function can be passed. 

``side`` takes one of three values: ``"both"`` for a two-sided permutation test, or ``"greater"`` and ``"lower"`` for one-sided permutation tests.

For more advanced usage, see :ref:`correlation-permutation-test-advanced`.
