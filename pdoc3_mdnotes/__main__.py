import argparse
import importlib
from pathlib import Path

from pdoc3_mdnotes import gui, mdnotes


class TemplatesError(Exception):
    def __str__(self):
        return ('Templates directory needs to exist and contain files: '
                '"config.mako", "credits.mako", "css.mako", '
                '"head.mako", "html.mako" and "logo.mako"')


def create_parser():
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
        help=('name of directory created in set path where documentation will '
              'be saved, default is: docs'),
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
        help=('path to directory with templates, when not specifed directory '
              '"templates" in path where program is run will be used if it '
              'exists else default templates are processed'),
        action='store')
    return parser.parse_args()


def check_templates(path):
    if mdnotes.Notes.has_templates(path):
        return
    raise TemplatesError


def main():
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
