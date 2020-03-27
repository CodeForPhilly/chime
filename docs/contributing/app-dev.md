# Contributing: Application Development

## Table of Contents

- [Developer Requirements](#developer-requirements)
- [Project Layout](#project-layout)
- [Running CHIME Locally](#running-chime-locally)
- [Testing](#testing)
- [Validating CHIME](#validating-chime)

## Developer Requirements

The application is built with [Streamlit](https://www.streamlit.io/), Streamlit requires:

- Python 2.7.0 or later / Python 3.6.x or later
- PIP

See [Streamlit's Getting Started guide](https://docs.streamlit.io/getting_started.html) for detailed information on prerequisites and setup

## Running CHIME Locally

### With `pipenv`

```bash
pipenv shell
pipenv install
streamlit run src/app.py
```

### With `conda`

```bash
conda env create -f environment.yml
source activate chime
pip install streamlit
streamlit run src/app.py
```

### Choosing a Different Port

If you need to run the application on a different port than the default (8000), you can export a variable in your shell session to override it with any port number of your choice before running:

```bash
export STREAMLIT_SERVER_PORT=1234
streamlit run src/app.py
```

## Project Layout

### Application files

- `src/app.py`: Main source for the application
- `src/test_app.py`: [pytest](https://docs.pytest.org/en/latest/) tests for `app.py`
- `script/`: Developer workflow scripts following [GitHub's Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) pattern.
- `.streamlit/`: [Streamlit config options](https://docs.streamlit.io/cli.html)
- `.env`: Local environment variables to use when running application, this file is copied from `.env.example` to start you out and then ignored by git
- `pytest.ini`: Configuration for [pytest](https://docs.pytest.org/en/latest/)
- `Pipfile`
- `Pipfile.lock`
- `environment.yml`
- `requirements.txt`
- `setup.py`

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

## Validating CHIME

*No validation routine is available yet. If you have thoughts on how to add one, please contribute!*
