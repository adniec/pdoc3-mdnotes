#!/usr/bin/env python3
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import pdoc

ACCESS_ERRORS = (AttributeError, FileNotFoundError,
                 NotADirectoryError, PermissionError)


def load(path):
    with open(path, 'r') as data:
        return data.read()


def save(path, content):
    with open(path, 'w') as data:
        data.write(content)


class Converter:
    def __init__(self, path, destination):
        self.files_paths = []
        self.directories_paths = []
        self.path = path
        self.destination = destination

    def process(self):
        self.collect(self.path)
        self.create_structure()
        self.convert()

    def convert(self):
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
        for path in self.directories_paths:
            self.create_directory(path)

    def create_directory(self, path):
        path = self.destination / self.get_relative_path(path)
        path.mkdir(parents=True, exist_ok=True)

    def get_relative_path(self, path):
        parts = path.parts
        relative_parts = parts[parts.index(self.path.name):]
        return '/'.join(relative_parts)


class Notes:
    def __init__(self, path, destination, name='docs', templates=None):
        self.destination = destination
        self.name = name
        self.set_templates(templates)

        context = pdoc.Context()
        source = str(path / destination.name)
        self.modules = pdoc.Module(source, context=context)
        pdoc.link_inheritance(context)

    def generate(self):
        for path, content in self.get(self.modules):
            parts = Path(path).parts[1:]
            path = self.destination / self.name / '/'.join(parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            save(path, content)

    def get(self, module):
        yield module.url(), module.html()
        for submodule in module.submodules():
            yield from self.get(submodule)

    def set_templates(self, directory):
        destination = self.destination / 'templates'
        module_dir = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        module = Path(module_dir) / 'templates'
        for path in (directory, destination, module):
            if self.change_templates(path):
                break

    def change_templates(self, path):
        if self.has_templates(path):
            pdoc.tpl_lookup.directories = [str(path)]
            return True
        return False

    @staticmethod
    def has_templates(directory):
        templates = ('config', 'credits', 'css', 'head', 'html', 'logo')
        try:
            files = set(path.name for path in directory.iterdir())
            expected = set(f'{name}.mako' for name in templates)
            return not expected - files
        except ACCESS_ERRORS:
            return False


def main(path, *args):
    with TemporaryDirectory() as temp_dir:
        converter = Converter(path, Path(temp_dir))
        converter.process()
        notes = Notes(converter.destination, path, *args)
        notes.generate()


if __name__ == '__main__':
    main(Path().absolute())
