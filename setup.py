# -*- coding: utf-8 -*-
"""Setup file for chime
"""
__version__ = "1.1.0"
__author__ = "Predictive Healthcare @ Penn Medicine"

from os import path

from setuptools import setup, find_namespace_packages

CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, "README.md"), encoding="utf-8") as inp:
    LONG_DESCRIPTION = inp.read()

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

setup(
    name="penn_chime",
    python_requires=">=3.7",
    version=__version__,
    description="COVID-19 Hospital Impact Model for Epidemics",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email="",
    url="https://github.com/CodeForPhilly/chime",
    project_urls={
        "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
        "Source": "https://github.com/CodeForPhilly/chime",
        "Documentation": "https://codeforphilly.github.io/chime/",
    },
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude=("tests")),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["penn_chime=penn_chime.cli:main"]},
    keywords=[],
    include_package_data=True,
)
