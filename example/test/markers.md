### [Documentation](https://docs.pytest.org/en/latest/mark.html) 

Markers are used to tag tests. They allow to group tests and run individual cases depending on user needs. Tests can be 
marked to skip or fail in set conditions. It can be used for example with tests which cannot succeed on specified 
platform. Through parametrize marker one test can be done multiple times with different arguments. See examples below.

Description of markers. Include it in `pytest.ini` or `tox.ini`, e.g.:

```
markers = 
    smoke : All critical tests
    database : All database tests
    gui : All GUI tests
```

Use: `pytest --markers` to display all available markers.

### Usage

Example `test_me.py` file with markers:

```python
from pytest import mark

@mark.smoke
@mark.gui
def test_something():
    assert True
```

For each function, method or class we can add as many markers as we want to. If class will be marked it means that 
marker will apply to each method of this class, e.g. `@mark.skip` prevents all methods from execution. Check [examples
](https://github.com/ethru/pdoc3-mdnotes/blob/master/example/test/code/test_markers.py).

### Run

- `pytest -m name` : runs each case marked with `@mark.name`
- `pytest -m "smoke and gui"` : runs each case marked with both `@mark.smoke` and `@mark.gui`
- `pytest -m "smoke or gui"` : runs each case marked with `@mark.smoke` or `@mark.gui` or both
- `pytest -m "not gui"` : runs each case except those marked with `@mark.gui`

#### Flags

Several examples:

- `--markers` : show available markers
- `-rs` : display description from skip markers during test run
- `-rx` : display description from xfail markers during test run

### Predefined markers

- `@mark.skip(reason='Fix in next sprint')` - allows to skip test, information why it is skipped can be added in 
`reason` parameter (displayed with `-rs` flag)
- `@mark.skipif(sys.platform=='win32', reason='Test only for Linux')` - skips test when condition is met
- `@mark.xfail` - it means that test will fail. As with `skipif` condition and `reason` can be set (displayed with `-rx`
flag).
- `@mark.parametrize('name', ['arg1', 'arg2'])` - it will run as many times as number of arguments in list. They can be 
passed to function by set name, e.g. `def test_me(name)`

### [Examples](https://docs.pytest.org/en/latest/skipping.html)

### [Parametrize](https://docs.pytest.org/en/latest/parametrize.html)