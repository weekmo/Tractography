#!/usr/bin/python3.6
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tractography",
    version="1.0.5",
    author="Mohammed Abdelgadir",
    description="The package deals with brain bundles images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weekmo/registration",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ),
)
