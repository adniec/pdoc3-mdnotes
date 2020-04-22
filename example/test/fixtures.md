### [Documentation](https://docs.pytest.org/en/latest/fixture.html)

Fixtures can be treated as functions which are defined in one place and are available across test files (with no need 
of import). Collect them in `conftest.py` file situated in folder with tests. From this directory (and all his 
subdirectories) every test will get access to fixtures defined there. To overwrite previously created fixture new 
`conftest.py` can be created in subdirectory with fixture named the same.

### Usage

In `conftest.py` place:

```python
from pytest import fixture
from time import sleep

from selenium import webdriver

@fixture
def browser():
    driver = webdriver.Firefox()
    yield driver
    sleep(5)
    driver.quit()

@fixture(scope='session')
def homepage(browser):
    return browser.get('https://github.com/')
```

In above example there are two fixtures defined. First one yields browser object. Note that `yield` is used instead of 
`return`. It allows to write code executed after work in this case with browser is done. Second uses previously defined 
browser fixture to open homepage. Take a look how it is done. Homepage function is also fixture, so decorator `@fixture`
is used as in previous example. Parameter which it takes is name of `browser` function. Now calling any method on 
`browser` will be equal to calling it on `driver` (`webriver.Firefox()`).
 
 Let's explain what will happen 
now if in other file (e.g. `test_me.py`) in same directory as `conftest.py` somebody will use `homepage`. First of all 
`driver` for Firefox will be created. By `yield` it will go to homepage fixture where method 
`get('https://github.com/')` is called. It opens Firefox and displays `GitHub` website. Then teardown from browser 
function is executed: `sleep(5)` and `driver.quit()`. After 5 seconds Firefox is closed.

[See example on GitHub.](https://github.com/ethru/pdoc3-mdnotes/blob/master/example/test/code/conftest.py)

### Scope

It allows to specify whether we are calling the same object or new one. Object can be created as one existing for whole 
test session. Then each call (doesn't matter from which function, class or file) will apply to the same (once created) 
object. It allows to share state between tests. On the other hand we can set scope to `function` which means that for 
each function new object will be created. Several operations can be made on this object within one function, but after 
going to the next one we will get new, fresh object (no affected by our previous manipulations). Available scopes:

- `session` : one (the same) object for whole test session
- `package` : one (the same) object for each package
- `module` : one (the same) object for each module
- `class` : one (the same) object for each class
- `function` : one (the same) object for each function or method

### Parametrize

```python
from pytest import fixture
from selenium import webdriver

@fixture(params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
def browser(request):
    driver = request.param()
    yield driver
    driver.quit()
```

Parameters are added as list to `params` of `@fixture`. To use them we pass `request` (keyword, predefined in `pytest`) 
to our fixture (in this case called browser). Access to each parameter is gained by `request.param` as on example above.

#### [Example](https://docs.pytest.org/en/latest/example/parametrize.html)