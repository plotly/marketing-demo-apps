from setuptools import find_packages, setup

VERSION = "0.0.1"
DESCRIPTION = "Custom theme package for Bank of America Graphs"
LONG_DESCRIPTION = "My first Python package with a slightly longer description"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="dash-templates",
    version=VERSION,
    author="Andres",
    author_email="andres.rodriguez@plot.ly",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["plotly"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    python_requires=">=3.6",
    keywords=["python", "first package"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
