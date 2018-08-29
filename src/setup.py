#!/usr/bin/python3.6
from setuptools import setup, find_packages
#from shutil import copyfile
#from os import remove
#from time import sleep
#from os.path import  isfile
"""
if isfile("../README.md"):
    copyfile("../README.md","README.md")
"""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tractography",
    version="0.1.11",
    author="Mohammed Abdelgadir",
    description="The package deals with brain bundles images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://weekmo.github.io/Tractography/",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ),
)
"""
sleep(2)
remove("README.md")
"""