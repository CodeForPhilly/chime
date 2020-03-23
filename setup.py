# -*- coding: utf-8 -*-
"""Setup file for chime
"""
__version__ = "0.1.0"
__author__ = ""


from os import path

from setuptools import setup, find_packages

CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, "README.md"), encoding="utf-8") as inp:
    LONG_DESCRIPTION = inp.read()

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]


setup(
    name="penn_chime",
    python_requires=">=3.6",
    version=__version__,
    description=None,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeForPhilly/chime",
    project_urls={
        "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
        "Source": "https://github.com/CodeForPhilly/chime",
        "Documentation": "https://codeforphilly.github.io/chime/",
    },
    author=__author__,
    author_email="",
    keywords=[],
    packages=find_packages(".", exclude=["docs", "k82", "script"]),
    install_requires=REQUIREMENTS,
    classifiers=[],
    include_package_data=True,
)
