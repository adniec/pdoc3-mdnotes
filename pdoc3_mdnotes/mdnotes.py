#!/usr/bin/env python3
"""#### mdnotes

Contains all necessary functions, classes and methods to use extension. It can
be run as standalone script. Then `html` notes will be created from files
placed in script directory ('templates' folder can be also added there for
customization). `main` function creates `tempfile.TemporaryDirectory` and
places there `.md` files content enclosed with docstring converted to `.py`.
Directory structure is preserved. All `README.md` are renamed to `__init__.py`
which helps build `index.html` page for each folder with notes. Modules used:
`os`, `pathlib`, `sys`, `tempfile` and `pdoc`.


#### License
Code interacting with [pdoc](https://pdoc3.github.io/pdoc/) is under [GNU
AGPL-3.0+](https://raw.githubusercontent.com/pdoc3/pdoc/master/LICENSE.txt)
License. To the rest of program apply MIT License and below statement:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import pdoc

ACCESS_ERRORS = (AttributeError, FileNotFoundError,
                 NotADirectoryError, PermissionError)


def load(path: Path) -> str:
    """Loads and returns file content from set path."""
    with open(path, 'r') as data:
        return data.read()


def save(path: Path, content: str):
    """Saves passed content to file stored in set path."""
    with open(path, 'w') as data:
        data.write(content)


class Converter:
    """
    Class responsible for `.md` files conversion to `.py` preserving original
    directory structure.

    ...

    Attributes
    ----------
    files_paths : list
        containing paths to collected files from `self.path`
    directories_paths : list
        containing paths to collected directories from `self.path`
    path : pathlib.Path
        path to directory containing `.md` files to convert
    destination : pathlib.Path
        path to directory where converted files fill be saved
    """
    def __init__(self, path, destination):
        self.files_paths = []
        self.directories_paths = []
        self.path = path
        self.destination = destination

    def process(self):
        """Goes through all steps needed to make conversion.

        First it collects files and folders from `self.path`. Then creates new
        directory structure in `self.destination`. Finally places there
        converted files.
        """
        self.collect(self.path)
        self.create_structure()
        self.convert()

    def convert(self):
        """Converts all collected files from `.md` to `.py`.

        If file name is `README.md` changes it to `__init__.py`. Each file is
        saved to `self.destination` preserving its relative path to project
        directory - `self.path`.
        """
        for path in self.files_paths:
            if path.suffix == '.md':
                if path.stem.upper() == 'README':
                    name = '__init__.py'
                else:
                    name = path.stem + '.py'
                data = '"""\n' + load(path) + '\n"""'
                path = (self.destination /
                        self.get_relative_path(path.parent) /
                        name)
                save(path, data)

    def collect(self, directory):
        """Collects all files from set directory.

        Iterates through files in set directory and places them in
        `self.directories_paths` or `self.files_paths`. When folder is met
        calls self again with that path. In case of `PermissionError` skips
        that location.

        Parameters
        ----------
        directory : pathlib.Path
            directory from which paths will be collected
        """
        for path in directory.iterdir():
            try:
                if path.is_dir():
                    self.directories_paths.append(path)
                    self.collect(path)
                else:
                    if path.suffix == '.md':
                        self.files_paths.append(path)
            except PermissionError:
                pass

    def create_structure(self):
        """Reproduces project directory structure in `self.destination`."""
        for path in self.directories_paths:
            self.create_directory(path)

    def create_directory(self, path):
        """Reproduces directory from set path in `self.destination`

        Parameters
        ----------
        path : pathlib.Path
            directory which will be reproduced in `self.destination`
        """
        path = self.destination / self.get_relative_path(path)
        path.mkdir(parents=True, exist_ok=True)

    def get_relative_path(self, path):
        """Removes base `self.path` from passed path to file or directory.

        Parameters
        ----------
        path : pathlib.Path
            path to file or directory from which relative path is needed

        Returns
        -------
        str
            string containing relative path
        """
        parts = path.parts
        relative_parts = parts[parts.index(self.path.name):]
        return '/'.join(relative_parts)


class Notes:
    """
    Class interacting with `pdoc` to create `html` notes.

    ...

    Attributes
    ----------
    destination : pathlib.Path
        path to project directory where folder from `self.name` will be created
    name : str, optional
        name of directory where `html` files will be stored (default is "docs")
    module : pdoc.Module
        `pdoc` object representing module from which notes will be generated
    """
    def __init__(self, path, destination, name='docs', templates=None):
        """
        Parameters
        ----------
        path : pathlib.Path
            path to directory containing `.py` files with notes
        templates : pathlib.Path or None, optional
            path to directory containing customized templates which will be
            used to create `html` notes (default is `None`)
        """
        self.destination = destination
        self.name = name
        self.set_templates(templates)

        context = pdoc.Context()
        source = str(path / destination.name)
        self.modules = pdoc.Module(source, context=context)
        pdoc.link_inheritance(context)

    def generate(self):
        """Creates `html` notes in `self.destination`/`self.name` directory."""
        for path, content in self.get(self.modules):
            relative = '/'.join(Path(path).parts[1:])
            path = self.destination / self.name / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            save(path, content)

    def get(self, module):
        """Obtains `url` and `html` content from set module and its submodules.

        Paramters
        ---------
        module : pdoc.Module
            object from which `url` and `html` content will be obtained, can
            contain submodules

        Yields
        ------
        tuple
            containing module `url` and its `html` content
        """
        yield module.url(), module.html()
        for submodule in module.submodules():
            yield from self.get(submodule)

    def set_templates(self, directory):
        """Sets `pdoc` templates according to available options.

         When passed path contains templates then they are used. If not folder
         `templates` in `self.destination` is checked. If still nothing is
         found templates from installation directory are taken. If it could not
         find them anywhere it does not modify anything - templates provided
         with `pdoc` are used.

         Parameters
         ----------
         directory : pathlib.Path or None
             path to directory containing templates, `None` when not specified
         """
        destination = self.destination / 'templates'
        module_dir = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        module = Path(module_dir) / 'templates'
        for path in (directory, destination, module):
            if self.change_templates(path):
                break

    def change_templates(self, path):
        """Changes `pdoc` templates if set `path` contains all necessary files.

        Parameters
        ----------
        path : pathlib.Path or None
            path to directory containing templates, `None` when not specified

        Returns
        -------
        bool
            information if templates were changed or not
        """
        if self.has_templates(path):
            pdoc.tpl_lookup.directories = [str(path)]
            return True
        return False

    @staticmethod
    def has_templates(directory):
        """Checks if templates files are stored in set `directory`

        Parameters
        ----------
        directory : pathlib.Path
            path to directory which will be checked if templates are there

        Returns
        -------
        bool
            information if folder contains templates or not
        """
        templates = ('config', 'credits', 'css', 'head', 'html', 'logo')
        try:
            files = set(path.name for path in directory.iterdir())
            expected = set(f'{name}.mako' for name in templates)
            return not expected - files
        except ACCESS_ERRORS:
            return False


def main(path, *args):
    """Generates notes in `html` format.

    Creates `tempfile.TemporaryDirectory`. Then converts `.md` files from set
    path to `.py` and stores them in that directory. Finally generates `html`
    notes from those files.

    Parameters
    ----------
    path : pathlib.Path
        path to directory with notes
    *args
        optional arguments passed to `Notes` class
    """
    with TemporaryDirectory() as temp_dir:
        converter = Converter(path, Path(temp_dir))
        converter.process()
        notes = Notes(converter.destination, path, *args)
        notes.generate()


if __name__ == '__main__':
    main(Path().absolute())
