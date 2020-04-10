from sys import platform
from pathlib import Path
from PyInstaller import __main__ as Install

sep = ";" if platform == "win32" else ":"

Install.run([
    '--name=pdoc3-mdnotes',
    '--onefile',
    '--windowed',
    f'--add-data={Path("pdoc3_mdnotes/icons/*.png")}{sep}.',
    f'--add-data={Path("pdoc3_mdnotes/templates/*.mako")}{sep}.)',
    f'--icon={Path("data/mdnotes.ico")}',
    str(Path('pdoc3_mdnotes/').absolute() / 'gui.py'),
])
