**********************
Quickstart
**********************


``mcpt`` comes with two main functions: ``permutation_test`` and ``correlation_permutation_test``.


Permutation test
================
This function takes the results for two groups, ``X`` and ``Y``, and tests whether the labels on the members of the group are exchangable under the null hypothesis. 


For simplest use, the ``permutation_test`` function takes four arguments:

* ``x`` - A list of values for members of the 1st group.
* ``y`` - A list of values for members of the 2nd group.
* ``side`` - The side that we want to test under the null hypothesis ("both" for two-sided, "greater" or "lower" for one-sided)
* ``f`` - The function for calculating the test statistic


.. code-block:: python

	>> import mcpt
	>> treatment = [10, 9, 11]
	>> control = [12, 11, 13]
	>> side = "lower"
	>> f = "mean"

	>> result = mcpt.permutation_test(treatment, control, f=f, side=side)
	>> print(result)
	Result(lower=0.09815650454064283, upper=0.10305649415095638, confidence=0.99)

In the above example, we are evaluating whether the mean of the samples in the ``treatment`` group is signifcantly lower than the mean of the samples in ``control`` group. Rather than returning a single p-value, ``mcpt`` returns a the upper and lower bounds of a confidence interval (default is 99%). In the above example, there is a 99% probability that the true p-value is between ~0.098 and ~0.103.


Correlation permutation test
============================
This function takes a set of paired scores, :math:`(x_1, y_1), (x_2, y_2)...(x_i, y_i)`, and tests whether the pairings are exchangable under the null hypothesis.

For simplest use, the ``correlaton_permutation_test`` function takes four arguments:

* ``x`` - A list of the :math:`x` values for the pairs.
* ``y`` - A list of the :math:`y` values for the pairs.
* ``side`` - The side that we want to test under the null hypothesis
* ``f`` - The function for calculating the test statistic

.. code-block:: python

	>> import mcpt
	>> x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
	>> y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]
	>> side = "both"
	>> f = "pearsonr"

	>> result = mcpt.correlation_permutation_test(x, y, f=f, side=side)
	>> print(result)
	Result(lower=0.021282451892029475, upper=0.029347445354757373, confidence=0.99)

