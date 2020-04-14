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
    """Return file content from set path."""
    with open(path, "r") as data:
        return data.read()


def save(path: Path, content: str):
    """Save passed content to file located in set path."""
    with open(path, "w") as data:
        data.write(content)


class Converter:
    """
    Class responsible for `.md` files conversion to `.py`.

    It preserves original directory structure.

    ...

    Attributes
    ----------
    path : pathlib.Path
        project path leading to directory containing `.md` files to convert
    files : list
        containing paths to collected files
    directories : list
        containing paths to collected directories
    """

    def __init__(self, path):
        """Collect `.md` files and directories paths from set location."""
        self.path = path
        self.files = []
        self.directories = []
        self.collect(path)

    def convert(self, directory):
        """Convert all collected files from `.md` to `.py`.

        If file name is `README.md` change it to `__init__.py`. Each file is
        saved to passed location preserving its relative path to project
        directory.

        Parameters
        ----------
        directory : pathlib.Path
            path to directory where converted files will be stored
        """
        self.create_structure(directory)
        for path in self.files:
            if path.suffix == ".md":
                if path.stem.upper() == "README":
                    name = "__init__.py"
                else:
                    name = path.stem + ".py"
                data = '"""\n' + load(path) + '\n"""'
                path = directory / path.relative_to(self.path.parent).parent
                save(path / name, data)

    def collect(self, directory):
        """Collect all files from set directory.

        Iterate through files in set directory and place them in
        `self.directories` or `self.files`. When folder is met call self again
        with that path. In case of `PermissionError` skip that location.

        Parameters
        ----------
        directory : pathlib.Path
            directory from which paths will be collected
        """
        for path in directory.iterdir():
            try:
                if path.is_dir():
                    self.directories.append(path)
                    self.collect(path)
                else:
                    if path.suffix == ".md":
                        self.files.append(path)
            except PermissionError:
                pass

    def create_structure(self, directory):
        """Reproduce project directory structure in set location.

        Parameters
        ----------
        directory : pathlib.Path
            path to directory where converted files will be stored
        """
        self.create_directory(self.path, directory)
        for path in self.directories:
            self.create_directory(path, directory)

    def create_directory(self, path, destination):
        """Reproduce directory from set path in destination.

        Parameters
        ----------
        path : pathlib.Path
            directory which will be reproduced
        destination : pathlib.Path
            location where to reproduce directory
        """
        path = destination / path.relative_to(self.path.parent)
        path.mkdir(parents=True, exist_ok=True)


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

    def __init__(self, path, destination, name="docs", templates=None):
        """Set notes templates. Initialize `pdoc` linker.

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
        self.module = pdoc.Module(source, context=context)
        pdoc.link_inheritance(context)

    def generate(self):
        """Create `html` notes in `self.destination`/`self.name` directory."""
        for path, content in self.get(self.module):
            relative = "/".join(Path(path).parts[1:])
            path = self.destination / self.name / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            save(path, content)

    def get(self, module):
        """Obtain `url` and `html` content from set module and its submodules.

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
        """Set `pdoc` templates according to available options.

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
        destination = self.destination / "templates"
        module_dir = getattr(sys, "_MEIPASS", Path(__file__).parent.absolute())
        module = Path(module_dir) / "templates"
        for path in (directory, destination, module):
            if self.change_templates(path):
                break

    def change_templates(self, path):
        """Change `pdoc` templates if set `path` contains all necessary files.

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
        """Check if templates files are stored in set `directory`.

        Parameters
        ----------
        directory : pathlib.Path
            path to directory which will be checked if templates are there

        Returns
        -------
        bool
            information if folder contains templates or not
        """
        templates = ("config", "credits", "css", "head", "html", "logo")
        try:
            files = set(path.name for path in directory.iterdir())
            expected = set(f"{name}.mako" for name in templates)
            return not expected - files
        except ACCESS_ERRORS:
            return False


def main(path, *args, **kwargs):
    """Generate notes in `html` format.

    Create `tempfile.TemporaryDirectory`. Then convert `.md` files from set
    path to `.py` and store them in that directory. Finally generate `html`
    notes from those files.

    Parameters
    ----------
    path : pathlib.Path
        path to directory with notes
    *args
        optional arguments passed to `Notes` class
    """
    with TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        converter = Converter(path)
        converter.convert(temp)
        notes = Notes(temp, path, *args, **kwargs)
        notes.generate()


if __name__ == "__main__":
    main(Path().absolute())
