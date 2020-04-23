from pytest import mark
from sys import platform


@mark.skip
def test_skip_marker():
    print('Test 1: this will be skipped.')
    assert True


@mark.smoke
@mark.gui
def test_marker_gui():
    print('Test 2: this will be run with marker gui, smoke.')
    assert True


@mark.smoke
def test_some_necessary_thing():
    print('Test 3: this will be run with marker smoke.')
    assert True


@mark.skipif(platform == "win32", reason="Cant be tested on Windows")
def test_me_everywhere_except_Windows():
    print('Test 4: this will be skipped on Windows.')
    assert platform != 'win32'


@mark.skipif(platform == "linux", reason="Cant be tested on Linux")
def test_me_everywhere_except_Linux():
    print('Test 5: this will be skipped on Linux.')
    assert platform != 'linux'


@mark.xfail(platform != 'win32', reason='Can be tested only on Windows.')
def test_me_on_windows():
    print('Test 6: if platform is other than Windows it will xfail.')
    assert platform == 'win32'


@mark.xfail(1 < 5, reason='It will always fail because 1 is smaller than 5.')
def test_condition_xfail():
    print('Test 7: it xfails always.')
    assert False


@mark.parametrize('my_args', ['go', 'for', 'it'])
def test_two_parameters(my_args):
    print('Test 8: it will run as many times as set parameters now uses: '
          f'"{my_args}" as parameter.')
    assert len(my_args) < 5


@mark.xfail
class TestXfail:
    def test_xfail_method(self):
        print('Test 9: method which fails in class marked with xfail.')
        assert False

    def test_next_xfail_method(self):
        print('Test 10: method which fails in class marked with xfail.')
        assert False
