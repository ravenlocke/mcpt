import setuptools

setuptools.setup(
    name="mcpt",
    version="0.1.0",
    description="A Python library for calculating p-values using Monte Carlo sampling",
    url="https://github.com/ravenlocke/mcpt",
    author="David J. Skelton",
    licence="MIT",
    packages=["mcpt"],
    install_requires=["scipy", "numpy"],
    zip_safe=False,
)
