"""Setup file for chime
"""
__version__ = "1.1.3"  # update VERSION in constants.py
__author__ = "Predictive Healthcare @ Penn Medicine"

from setuptools import setup, find_namespace_packages


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
        "altair",
        "black",
        "gspread",
        "gunicorn",
        "dash",
        "dash_bootstrap_components",
        "numpy",
        "pandas",
        "pytest",
        "pyyaml",
        "selenium",
        "streamlit",
        "gspread",
        "oauth2client"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['penn_chime=penn_chime.cli:main'],
    },
    keywords=[],
    include_package_data=True,
)
