import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="registration",
    version="0.0.1",
    author="Mohammed Abdelgadir",
    description="Direct Bundle Registration",
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