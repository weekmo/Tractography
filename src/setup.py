import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tractography",
    version="1.0.0",
    author="Mohammed Abdelgadir",
    description="The package deals with brain bundles images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weekmo/registration",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)