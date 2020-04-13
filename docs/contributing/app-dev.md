# Contributing: Application Development

## Table of Contents

- [Developer Requirements](#developer-requirements)
- [Running CHIME Locally](#running-chime-locally)
- [Project Layout](#project-layout)
- [Testing](#testing)
- [Validating CHIME](#validating-chime)

## Developer Requirements

The application is built with [Streamlit](https://www.streamlit.io/), Streamlit requires:

- Python 3.6.x or later
- PIP

See [Streamlit's Getting Started guide](https://docs.streamlit.io/getting_started.html) for detailed information on prerequisites and setup

## Running CHIME Locally


### With `venv`

```bash
python3 -m venv ~.venv
. ~.venv/bin/activate
pip install -e .
```

### With `pipenv`

```bash
pipenv shell
pipenv sync --dev
```

### With `conda`

```bash
conda env create -f environment.yml
source activate chime
pip install streamlit
```

## Run the Streamlit Web App

```bash
PARAMETERS=-./defaults/webapp.cfg streamlit run st_app.py
```

## Run the Command Line Interface

```bash
PARAMETERS=./defaults/cli.cfg penn_chime
```

## Help with the Command Line Interface

```bash
penn_chime --help
```

### Choosing a Different Set of Parameters

If you want a different set of default parameters, you may use your own configuration file.

```bash
PARAMETERS=./defaults/yours.cfg streamlit run st_app.py
```

Be sure to include `--current-date` in the file, if your `--current-hospitalized` is not today's value.
Be sure to include `--mitigation-date` in the file if social distancing was implemented before today.

### Choosing a Different Port

If you need to run the application on a different port than the default (8000), you can set an environment variable.

```bash
STREAMLIT_SERVER_PORT=1234 PARAMETERS=./defaults/webapp.cfg streamlit run st_app.py
```

## Project Layout

### Application files

- `st_app.py`: Startup script for the streamlit web application.
- `src`: Source code for the `penn_chime` module.
- `tests/`: [pytest](https://docs.pytest.org/en/latest/) tests for the `penn_chime` module.
- `script/`: Developer workflow scripts following [GitHub's Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) pattern.
- `.streamlit/`: [Streamlit config options](https://docs.streamlit.io/cli.html)
- `.env`: Local environment variables to use when running application, this file is copied from `.env.example` to start you out and then ignored by git
- `environment.yml`
- `Pipfile`
- `Pipfile.lock`
- `setup.py`
- `setup.cfg`: Configuration for flake8, mypy, [pytest](https://docs.pytest.org/en/latest/)

### Documentation

- `docs/`: Markdown documentation in [GitBook format](https://gitbookio.gitbooks.io/docs-toolchain/structure.html) used to generate `gh-pages` website at [codeforphilly.github.io/chime](https://codeforphilly.github.io/chime)

### Operations support

- `.github/workflows/`: [GitHub Actions](https://github.com/features/actions) workflows implementing automations driven by GitHub events
- `.holo/`: [Hologit](https://github.com/JarvusInnovations/hologit) projection configuration, used to generate `gh-pages` branch from content changes in `docs/` tree
- `k8s/`: Kubernetes manifests for [the `chime-live` cluster](https://codeforphilly.github.io/chime/operations/chime-live-cluster.html)
- `.env.example`: A starter `.env` file distributed with the project
- `docker-compose.yml`: Runtime container configuration for running the application locally via Docker
- `Dockerfile`: Recipe for building Docker container that runs the application
- `Procfile`: Supports running the application on Heroku

## Testing

The project is set up for testing with [pytest](https://docs.pytest.org/en/latest/), and the GitHub repository is configured to execute `pytest` against all pull requests automatically.

To run tests locally, enter an environment first with `pipenv` or `conda` as indicated above in [Running CHIME Locally](#running-chime-locally), and then run:

```bash
pip install pytest
pytest
```

The test code runs from the local `tests` directory. Updating code in `tests` modifies the tests.
Use `pip install -e .` so that your local changes to `src` are also the module under test.
For CI, use `pip install .` to test the module installed in site-packages to ensure that the installed module is packaged correctly with all of its dependencies.
Do not import from src in your tests or your python code as this will appear to work locally, but break the python module.

## Validating CHIME

*No validation routine is available yet. If you have thoughts on how to add one, please contribute!*
