"""Setup file for chime
"""
__version__ = "0.1.0"
__author__ = "Predictive Healthcare @ Penn Medicine"

import io
from os import path
from setuptools import setup, find_packages, find_namespace_packages

CWD = path.abspath(path.dirname(__file__))

#with io.open(path.join(CWD, "README.md"), encoding="utf-8") as inp:
#    LONG_DESCRIPTION = inp.read()

#with io.open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
#    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

with io.open("README.md", "r") as inp:
    LONG_DESCRIPTION = inp.read()

with io.open("requirements.txt", "r") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

    
setup(
    name="penn_chime",
    version=__version__,
    author=__author__,
    author_email="",
    description="COVID-19 Hospital Impact Model for Epidemics",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeForPhilly/chime",
    project_urls={
        "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
        "Source": "https://github.com/CodeForPhilly/chime",
        "Documentation": "https://codeforphilly.github.io/chime/",
    },
    package_dir={'': 'src'},
    #packages=find_namespace_packages(where='src', exclude=('tests')),
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "altair",
        "pytest",
        "dash", 
        "dash_bootstrap_components", 
        "pyyaml", 
        "gunicorn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['penn_chime=penn_chime.cli:main'],
    },
    keywords=[],
    packages=find_packages(".", exclude=["docs", "k82", "script", "tests"]),
    #install_requires=REQUIREMENTS,
    include_package_data=True,
)
