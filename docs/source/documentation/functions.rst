**********************
Functions
**********************

In this section, more advanced usage of the two main functions will be discussed:

* ``mcpt.permutation_test``  
* ``mcpt.correlation_permation_test`` 


Common features
===============
There are a number of advanced uses of the functions discussed here that are common to both functions. 

Setting the number of permutations
----------------------------------
The number of random permutations to be used is set by specifying the ``n`` parameter when calling either function. By default this value is ``10,000``; increasing this value is one approach to narrowing the p-value range returned if required.

Multiprocessing
---------------
In order to speed up calculations, both functions are configured to take a ``cores`` parameter. This determines the number of (logical) CPUs to be used for permuting; ``multiprocessing.Pool`` is used to create a pool of workers, and the permutation calculations farmed across these workers. **Note that the default is to use a single core (i.e., not multiprocessed).**

Seeding
-------
To allow reproducibility of results, ``mcpt`` also implemented seeding, and can be set by passing the ``seed`` parameter to either function. By default, ``seed=None``, meaning that two runs of ``mcpt`` will `not` give exactly the same answer unless a seed is explicitly passed. Seeding works in both single core and multi-core versions.

If a seed is given, this is used to seed a random number generator (``random.Random``), which in turn is used to generate random integers in :math:`[0, 1e100)` to seed the randomisation in each permutation. If no seed is given, then the initial seed is random.

Confidence
----------
A Monte Carlo permutation test has a random factor and, thus, the p-value returned differs from run-to-run. However, based on the number of permutations and the p-value returned, it is possible to calculate a range in which, with a certain confidence, we can say the true p-value lies in. There are a number of ways to achieve this, but ``mcpt`` uses the `Wilson score interval <https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval>`_ binomial approximation approach. The confidence can be set by passing the ``confidence`` parameter, where confidence is a float -- for example, passing ``confidence = 0.999`` means that there is a :math:`1/1000` chance that the true p-value lies outside the interval returned by the function called.


.. _permutation-test-advanced:

Permutation test 
================
There are two main advanced uses to consider with the ``mcpt.permutation_test`` function. The first is passing a custom function, and the second is using multi-dimensional inputs.

Using a custom function
-----------------------
Normally, ``x`` and ``y`` passed to the function are one dimensional iterables (e.g., a ``list``) of values. For this section, we will assume this is the case, but the next section will consider the multi-dimensional situation.

Let's say rather than standard deviation, we want to consider the interquartile range (IQR). We can define a function that can take a list and calculate / return the value of the test statistic (IQR in this case) to use with ``mcpt.permutation_test``

.. code-block:: python

	import numpy as np

	def iqr(x):
	    q3 = np.quantile(x, .75)
	    q1 = np.quantile(x, .25)
	    return q3 - q1


We can now call ``mcpt.permutation_test`` with ``f=iqr``. In the below example we create ``x`` and ``y`` by sampling from a normal distribution with ``mean = 0.5, std=0.5`` and ``mean = 0.5, std=1.5`` respectively. We would expect ``x`` to have a lower IQR than ``y``, and can test this as follows:

.. code-block:: python

	import mcpt

	# Generate x
	x = [np.random.normal(0.5, 0.5) for _ in range(100)]
	# Generate y
	y = [np.random.normal(0.5, 1.5) for _ in range(100)]
	# Run the permutation test
	result = mcpt.permutation_test(x, y, side="lower", f=iqr)
	print(result)

The result may vary from run-to-run (unseeded), but the result obtained should be something around ``Result(lower=0.0, upper=0.0006630497334598373, confidence=0.99)``; unsurprisingly, a statistically significant difference was detected.

Of course, ``scipy`` has an interquartile range function, and this can be used directly instead of defining a custom function.

.. code-block:: python

	from scipy import stats as _st
	result = mcpt.permutation_test(x, y, side="lower", f=_st.iqr)
	print(result)

Which gives (subject to randomness) approximately the same answer. Thus, to summarize, ``mcpt.permutation_test`` gives a flexible interface for hypothesis testing.


Multi-dimensional inputs
------------------------
It may be the case that, rather than having as single value for the members of your group, you have multiple values. An example use-case for this would be where you have a pair of values :math:`(x_1, y_1), (x_2, y_2)...(x_i, y_i)` for two groups, `A` and `B`, and you wish to test whether the correlation between `x` and `y` differs between `A` and `B`.

``mcpt.permutation_test`` puts no restrictions on what ``x`` and ``y`` look like, and so you can define custom functions that are aware of this shape. The below example shows this for considering whether there is a statistically significant difference in the correlation of variables in two groups (and fails to reject the null hypothesis).


.. code-block:: python

	import mcpt

	from scipy.stats import pearsonr

	x = [(10, 8), (9, 6), (8, 9), (2, 4), (5, 3), (3, 10), (3, 4), (8,10)]
	y = [(1, 9), (10, 4), (2, 3), (2, 8), (5, 9), (7, 2), (5, 5), (1, 4)]

	def pearson_correlation(a):
		x_vals = [i[0] for i in a]
		y_vals = [i[1] for i in a]

		return pearsonr(x_vals, y_vals)[0]

	result = mcpt.permutation_test(x, y, side="both", f=pearson_correlation)
	print(result)
	# Result(lower=0.11605000822777765, upper=0.13304820734194409, confidence=0.99)



.. _correlation-permutation-test-advanced:

Correlation permutation test
============================
Similar to ``mcpt.permutation_test``, this ``mcpt.correlation_permutation_test`` can accept a custom function where a custom test statistic is being calculated. We anticipate that these will most often be either ``spearmanr`` or ``pearsonr``. However, other correlation measures exist (e.g., `Kendall's tau <https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient>`_).

The key difference in the implementation of custom functions for ``mcpt.correlation_permutation_test`` is that we expect to be able to pass two variables to it -- ``x`` and ``y``.


.. code-block:: python

	import mcpt

	from scipy.stats import kendalltau

	x = [4.02, 4.52, 4.79, 4.89, 5.27, 5.63, 5.89, 6.08, 6.13, 6.19, 6.47]
	y = [4.56, 2.92, 2.71, 3.34, 3.53, 3.47, 3.20, 4.51, 3.76, 3.77, 4.03]

	def ktau(x, y):
		tau, _ = kendalltau(x, y)
		return tau

	result = mcpt.correlation_permutation_test(x, y, side="both", f=ktau)
	print(result)
	# Result(lower=0.1594695442150737, upper=0.17876952731842338, confidence=0.99)


The above example is from `here <https://www.uvm.edu/~dhowell/StatPages/R/RandomizationTestsWithR/RandomCorr/randomization_Correlation.html>`_, where the true value was found to be 0.1646.

