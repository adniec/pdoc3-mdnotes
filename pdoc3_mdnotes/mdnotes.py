#!/usr/bin/env python3


def load(path):
    with open(path, 'r') as f:
        return f.read()


def save(path, data):
    with open(path, 'w') as f:
        f.write(data)


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
                name = '__init__.py' if path.stem == 'README' else path.stem + '.py'
                data = '"""\n' + load(path) + '\n"""'
                path = self.destination / self.get_relative_path(path.parent) / name
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
