import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xboxpy",
    version="0-dev",
    maintainer="XboxDev maintainers",
    description="Python module to interface with original Xbox hard- and software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XboxDev/xboxpy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
