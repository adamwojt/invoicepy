# Local development
```
git clone git@github.com:adamwojt/pyinvoice.git
cd pyinvoice
```
> **Note:** We recommend that you use a personal [fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) for this step. If you are new to GitHub collaboration,
> you can refer to the [Forking Projects Guide](https://guides.github.com/activities/forking/).

### Code style
We use [pre-commit](https://pre-commit.com/) to sort out linting
```
pip3 install pre-commit
pre-commit install
```
### poetry
For organising dependencies and eviroment we use [poetry](https://github.com/python-poetry/poetry)

```
poetry install
poetry shell
pyinvoice --help
```

### Testing
We use pytest
```
pytest -vv
```
