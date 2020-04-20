### [Documentation](https://docs.pytest.org/en/latest/contents.html)

- [API Reference](https://docs.pytest.org/en/latest/reference.html)
- [Usage](https://docs.pytest.org/en/latest/usage.html)
- [Examples](https://docs.pytest.org/en/latest/example/index.html)
- [Tutorials](https://docs.pytest.org/en/latest/talks.html)

### [Building tests structure](https://pytest.readthedocs.io/en/reorganize-docs/new-docs/user/directory_structure.html)

- tests mixed with code inside project directory
- tests placed outside of project in `tests` directory

[Read more](https://docs.pytest.org/en/latest/goodpractices.html)

#### Example tests structure

```
setup.py
src/
    mypkg/
        __init__.py
        app.py
        view.py
tests/
    __init__.py
    foo/
        __init__.py
        test_view.py
    bar/
        __init__.py
        test_view.py
```

#### [Examples in projects](https://docs.pytest.org/en/latest/projects.html)

- [circuits](https://github.com/circuits/circuits/tree/master/tests)
- [sentry](https://github.com/getsentry/sentry/tree/master/tests)
- [tox](https://github.com/tox-dev/tox/tree/master/tests)

### Usage

To run tests just write `pytest` in terminal inside `tests` directory, but note:

- names of files `test_*`, classes `Test*`, functions and methods `test_*` should correspond to highlighted convention -
it can be changed in file called 
[pytest.ini](https://docs.pytest.org/en/latest/example/pythoncollection.html#changing-naming-conventions)
- `ImportError` can be displayed which means no access to project source directory, avoid it by:
    - #### `python -m pytest tests`
        - call it from project directory (tests will get access to `src` directory)
    - #### `pip install -e .` 
        - with `setup.py` file project can be installed in `--extended` mode. It means that its files will be linked. 
        Making any change inside them will reflect in each reference to project. No reinstallation needed.
    - #### [tox](https://tox.readthedocs.io/en/latest/)
        - tool to run tests in virtual environment (recommended)

#### Flags

Several examples:

- `-h` : help
- `-v` : display more details
- `-s` : display prints used in tests
- `--markers` : show available markers
- `--fixtures` : show available fixtures
- `-rs` : display description from skip markers during test run
- `-rx` : display description from xfail markers during test run

### Configuration

In `tests` directory place `pytest.ini` file (or add below options to `tox.ini`):

```ini
[pytest]
python_files = check_*
python_classes = *Check
python_functions = *_check

addopts = -v
testpaths = tests
markers = 
    smoke : All critical tests
    database : All database tests
    gui : All GUI tests
```

- `python_files`, `_classes`, `_functions` - allow to edit default name of tests files `test_*`, classes `Test*`, 
methods and functions `test_*`
- `addopts` allows to add [predefined flags
](https://docs.pytest.org/en/latest/customize.html#builtin-configuration-file-options) to each `pytest` call. This 
means that in example above instead normal `pytest` output `pytest -v` will be displayed.
- `testpaths` specifies tests directory, when unset all folders will checked
- `markers` - contains description of custom markers used in tests. Allows new user to display them by `pytest 
--markers`

[See example on GitHub.](https://github.com/ethru/pdoc3-mdnotes/blob/master/example/test/code/pytest.ini)

#### Use of conftest.py and fixtures

Each test placed in same or subdirectory gets access to functions defined in file `conftest.py` and marked as 
`@fixture`. They can be overwritten by creating new `conftest.py` in any subdirectory and making fixture with the same 
name. More information in fixtures tab.  

#### [Configuration options](https://docs.pytest.org/en/latest/reference.html#configuration-options)

### Reports

Reports can be generated from tests runs. Depending on needs proper format can be preferred:

- #### html
    - readable for user
    - use `pytest-html` extension described below
    - create report: `pytest-html --html="results.html"`
- #### xml
    - integration with CI (Jenkins for example)
    - create report: `pytest --junitxml="results.xml"`

### Extensions

- #### [pytest-xdist](https://github.com/pytest-dev/pytest-xdist)
    - allows to run tests parallel
    - installation: `pip install pytest-xdist`
    - usage: `pytest -n4` where `n` means number of used threads. Flag `-nauto` for automatic configuration.
- #### [pytest-socket](https://github.com/miketheman/pytest-socket)
    - allows to disable socket during tests run
    - installation: `pip install pytest-socket`
    - usage: `from pytest_socket import disable_socket`
- #### [pytest-html](https://github.com/pytest-dev/pytest-html)
    - generates `html` reports from tests run
    - installation: `pip install pytest-html`
    - usage: `pytest-html --html="results.html"`
- #### [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
    - checks tests coverage
    - installation: `pip install pytest-cov`
    - usage: `pytest --cov=project tests/`
