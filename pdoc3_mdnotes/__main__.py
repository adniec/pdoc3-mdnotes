"""#### Main

Contains `main` function which creates argument parser. According to set flags
runs program in proper way, e.g. as GUI application or script with passed
settings. It uses: `argparse`, `importlib` and `pathlib`.


#### License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import importlib
from pathlib import Path

from pdoc3_mdnotes import mdnotes


class TemplatesError(Exception):
    """Exception returning information about expected templates files."""

    def __str__(self):
        """Return exception message."""
        templates = ('config', 'credits', 'css', 'head', 'html', 'logo')
        all = ', '.join([f'"{n}.mako"' for n in templates])
        return (f'Templates directory needs to exist and contain files: {all}')


def create_parser():
    """Create parser then return its arguments."""
    parser = argparse.ArgumentParser(
        description=('Make notes from ".md" files. More information under: '
                     'https://ethru.github.io/pdoc3-mdnotes/'))
    parser.add_argument(
        '-g', '--gui',
        help='launches GUI for application',
        action='store_true'
    )
    parser.add_argument(
        '-n', '--name',
        help=('name of directory where html notes will be saved, default is: '
              '"docs". Path can be used as well. Relative will navigate from '
              'project directory (specified by `-p`, `--path`)'),
        action='store',
        default='docs'
    )
    parser.add_argument(
        '-p', '--path',
        help=('path to directory containing notes (".md" files), when not '
              'specified path where program is run will be used'),
        action='store',
        default='.'
    )
    parser.add_argument(
        '-t', '--templates',
        help=('path to directory with templates, when not specified directory '
              '"templates" in path where program is run will be used if it '
              'exists else default templates are processed'),
        action='store')
    return parser.parse_args()


def check_templates(path):
    """Check if path is correct and contain templates.

    Parameters
    ----------
    path : pathlib.Path
        path to templates provided by user

    Raises
    ------
    TemplatesError
        if set directory does not exist or contain necessary files
    """
    if mdnotes.Notes.has_templates(path):
        return
    raise TemplatesError


def main():
    """Create argument parser and process its values to run program."""
    args = create_parser()

    if args.gui:
        gui = importlib.import_module('pdoc3_mdnotes.gui')
        gui.main()
    else:
        path = Path(args.path).absolute()
        templates = args.templates
        if templates:
            templates = Path(templates).absolute()
            check_templates(templates)
        mdnotes.main(path, args.name, templates)


if __name__ == '__main__':
    main()
