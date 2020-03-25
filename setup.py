import setuptools

from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as inp:
    REQUIREMENTS = [el.strip() for el in inp.read().split(",")]

setuptools.setup(
    name="penn_chime",
    version="1.0.0",
    author="Predictive Healthcare @ Penn Medicine",
    description="COVID-19 Hospital Impact Model for Epidemics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeForPhilly/chime",
    project_urls={
        "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
        "Source": "https://github.com/CodeForPhilly/chime",
        "Documentation": "https://codeforphilly.github.io/chime/",
    },
    package_dir={'': 'src'},
    packages=setuptools.find_namespace_packages(where='src', exclude=('tests')),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['penn_chime=penn_chime.cli:main'],
    }
)
