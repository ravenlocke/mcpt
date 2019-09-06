import setuptools

# Read the contents of the README file
import io
from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="mcpt",
    version="0.1.8",
    description="A Python library for calculating p-values using Monte Carlo sampling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravenlocke/mcpt",
    author="David J. Skelton",
    author_email="d.j.skelton1@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["scipy", "numpy", "matplotlib"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires="~=3.5",
)
