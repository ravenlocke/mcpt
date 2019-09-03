# mcpt: Monte Carlo permutation tests for Python
Monto Carlo permutation tests are often used in science to calculate p-values.
This package was created to support scientists with these calculations.

## Documentation
### Installation
The simplest way to install this package is directly from PyPI using pip

<pre>
pip install mcpt
</pre>

### Usage
This package comprises one main function, `permutation_test`. This functions requires four arguments 
that must be specified:
* `x` : A list of results for condition one.
* `y` : A list of results for condition two.
* `f` : The function that calculates the test statistic. Alternatively, this can be a string for the following:
    * `mean`
    * `median`
    * `stdev`
* `side`: The side you want to calculate the test statistic for (`both` for two-sided, `greater` for one-sided (greater), and `lower` for one-sided (lower))

Additionally, you can specify the following:
* `n` : The number of Monte Carlo samples to take for calculating the p-value (default 10,000)
* `confidence` : The probability that the p-value is contained between the upper and lower bounds returned by the function (default 0.99).

Upper and lower bounds are calculated with a binomial approximation using [Wilson intervals without continuity correction](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval).

The function returns a `namedtuple`, with the following fields:
* `lower` : The lower bound for the p-value at the given confidence
* `upper` : The upper bound for the p-value at the given confidence
* `confidence` : The confidence supplied

Below is an example of this in action

<pre>
>> import mcpt
>> x = [10, 9, 11]
>> y = [12, 11, 13]
>> f = "mean"
>> n = 100_000
>> side = "lower"

>> result = mcpt.permutation_test(x, y, f, side, n=n)
>> print(result)
Result(lower=0.09815650454064283, upper=0.10305649415095638, confidence=0.99)
</pre>

In the above example, we were attempting to detect whether the mean of the values in `x` was 
significantly lower than the means of values in `y`. The result gives a range back in which the
true p-value is likely to occur (0.098 - 0.103), and that there is a [99% probability that the given 
interval encompasses the true p-value](https://en.wikipedia.org/wiki/Confidence_interval#Meaning_and_interpretation).
