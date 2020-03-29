"""Setup file for chime
"""
__version__ = "0.2.0"
__author__ = "Predictive Healthcare @ Penn Medicine"

from os import path
from setuptools import setup, find_packages, find_namespace_packages


setup(
    name="penn_chime",
    version=__version__,
    author=__author__,
    author_email="",
    description="COVID-19 Hospital Impact Model for Epidemics",
    url="https://github.com/CodeForPhilly/chime",
    project_urls={
        "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
        "Source": "https://github.com/CodeForPhilly/chime",
        "Documentation": "https://codeforphilly.github.io/chime/",
    },
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src', exclude=('tests')),
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
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': ['penn_chime=penn_chime.cli:main'],
    },
    keywords=[],
    include_package_data=True,
)
