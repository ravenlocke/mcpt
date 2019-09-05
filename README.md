<p align="center">
    <a href="https://pypi.python.org/pypi/mcpt/" alt="version">
        <img src="https://img.shields.io/pypi/v/mcpt.svg" /></a>
    <a href="https://pypi.python.org/pypi/mcpt/" alt="status">
        <img src="https://img.shields.io/pypi/status/mcpt.svg" /></a>
    <a href="https://pypi.python.org/pypi/mcpt/" alt="status">
        <img src="https://img.shields.io/pypi/pyversions/mcpt.svg" /></a>
    <br>
    <a href="https://doi.org/10.5281/zenodo.3387528" alt="status">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3387528.svg" /></a>
     <a href="https://pypi.python.org/pypi/mcpt/" alt="status">
        <img src="https://img.shields.io/pypi/l/mcpt.svg" /></a> 
     <a href="https://pypi.python.org/pypi/mcpt/" alt="status">
        <img src="https://img.shields.io/pypi/dm/mcpt.svg" /></a> 
</p>


# mcpt: Monte Carlo permutation tests for Python
`mcpt` is a Python 3 library for calculating p-values through Monte Carlo permutation tests, providing an intuitive, simple, and highly customisable interface to determining statistical significance.

To get started, we recommend you read through Installation, Quickstart, and Functions sections of our [read the docs documentation](https://mcpt.readthedocs.io/en/latest/). Also check out the [FAQ](https://mcpt.readthedocs.io/en/latest/documentation/faq.html), which we update regularly. If you have concerns about the software, or feel that there is something that should be more explicit, then we’d love to hear from you – [please open an issue on Github](https://github.com/Ravenlocke/mcpt/issues) and we’ll get back in touch ASAP.

If you use `mcpt` in your research, please support us by citing the initial release:

> David J. Skelton. (2019, September 5). mcpt: Monte Carlo permutation tests for Python (Version 0). Zenodo. http://doi.org/10.5281/zenodo.3387528



## TLDR;
### Installation
The simplest way to install this package is directly from PyPI using pip

<pre>
pip install mcpt
</pre>

### Usage
`mcpt` contains two main functions: `mcpt.permutation_test` and `mcpt.correlation_permutation_test`. 


Below is an example of the `mcpt.permutation_test` - for more info, please see the documentation [here](https://mcpt.readthedocs.io/en/latest/documentation/quickstart.html#permutation-test)
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

Below is an example of `mcpt.correlation_permutation_test` - for more information, please see the documentation [here](https://mcpt.readthedocs.io/en/latest/documentation/quickstart.html#correlation-permutation-test)

<pre>
>> import mcpt
>> x = [-2.31, 1.06, 0.76, 1.38, -0.26, 1.29, -1.31, 0.41, -0.67, -0.58]
>> y = [-1.08, 1.03, 0.90, 0.24, -0.24, 0.76, -0.57, -0.05, -1.28, 1.04]
>> side = "both"
>> f = "pearsonr"

>> result = mcpt.correlation_permutation_test(x, y, f=f, side=side)
>> print(result)
Result(lower=0.021282451892029475, upper=0.029347445354757373, confidence=0.99)
</pre>
