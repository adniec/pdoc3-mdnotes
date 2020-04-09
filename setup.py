from setuptools import setup
from sys import platform

from pdoc3_mdnotes import __version__


def get_description():
    with open('README.md') as readme:
        return readme.read()


def get_requirements():
    with open('requirements.txt') as required:
        return required.read()


data_files = []
if platform == 'linux':
    data_files.append(('share/applications', ['data/mdnotes.desktop']))
    data_files.append(('share/icons/', ['pdoc3_mdnotes/icons/mdnotes.png']))

setup(
    name='pdoc3-mdnotes',
    version=__version__,
    author='Adrian Niec',
    author_email='ethru@protonmail.com',
    description='Extension to generate notes from markdown files with pdoc3.',
    long_description=get_description(),
    url='https://github.com/ethru/pdoc3-mdnotes',
    license='MIT/AGPLv3+',
    platforms=['any'],
    install_requires=get_requirements(),
    python_requires='>=3.6',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: '
                 'GNU Affero General Public License v3 or later (AGPLv3+)',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Topic :: Documentation',
                 'Topic :: Education',
                 'Topic :: Office/Business',
                 'Topic :: Utilities',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 ],
    packages=['pdoc3_mdnotes'],
    data_files=data_files,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mdnotes = pdoc3_mdnotes.__main__:main',
            'mdnotes-gui = pdoc3_mdnotes.gui:main',
            'pdoc3-mdnotes = pdoc3_mdnotes.__main__:main',
            'pdoc3_mdnotes = pdoc3_mdnotes.__main__:main'
        ],
    },
)
