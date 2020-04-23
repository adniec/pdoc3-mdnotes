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


@fixture(params=[webdriver.Chrome, webdriver.Firefox])
def browser_with_params(request):
    driver = request.param()
    yield driver
    driver.quit()
