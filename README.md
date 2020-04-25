# pdoc3-mdnotes

Simplicity is a key. Don't you agree? What would you say to bring your notes online in few easy steps and allow other 
team members to develop them? This can lead to deploying good tutorial for coworkers or building website for university 
project. Spectrum is wide, you decide how to use it!

Idea behind this project is to combine [Markdown](https://www.markdownguide.org/), [pdoc3](https://pdoc3.github.io/) and
[GitHub Pages](https://pages.github.com/) to upload your notes as website without much effort. Markdown is cool, isn't 
it? You can simply create such a file in any notepad. Place headings, links, images and all needed stuff there. To build
notebook just make few `.md` files and divide them into different directories based on notes topic. As on example [here
](https://github.com/ethru/pdoc3-mdnotes/tree/master/example/).

Next step is conversion to `.html` and linking notes with each other. Here comes `pdoc3-mdnotes` with help. It bases on 
fantastic documentation tool [pdoc3](https://pdoc3.github.io/pdoc/doc/pdoc/). Just take a look at its website. Isn't 
that form of keeping your information clean and readable? I think it is! With few modifications which this extension 
makes your notes can look the same. Just check example from previous paragraph converted to [website
](https://ethru.github.io/pdoc3-mdnotes/example/).

Finally you can upload your work to [GitHub Pages](https://pages.github.com/) and share it with others. It's a great way
to open your notes as normal website every time you need them. It also allows other people to contribute and develop 
your project.

***Note:** purpose of this project is to create simple static website from `.md` files with no prior configuration 
needed. You can of course experiment with templates, but for more complex ideas take a look at [Jekyll
](https://jekyllrb.com/).*

## Installation

```
$ git clone https://github.com/ethru/pdoc3-mdnotes.git
$ pip install pdoc3-mdnotes/.
```
***Linux note:** default installer behaviour is to create desktop entry for application. If you are going use it as 
script and don't need that entry. Please change `'linux'` to `None` in line `if platform == 'linux':` of `setup.py` 
file.*

## Build

To build application [PyInstaller](http://www.pyinstaller.org/) is needed. Get it with: `$ pip install pyinstaller` .
```
$ git clone https://github.com/ethru/pdoc3-mdnotes.git
$ cd pdoc3-mdnotes
$ pip install -r requirements.txt
$ python build.py
```
GUI version of application is built. Executable is located in `dist` directory.

## Preparation

- create base directory for your project, e.g. `Notes`
- separate different topics inside new directories
    - each directory name will be website heading
    - e.g. `examples_to_check` directory will transform into `Examples to check` heading
- add `README.md` for each directory
    - it will be treated as `index.html`
    - this means: content displayed below heading (directory name)
- place as many `.md` files as your project needs
    - they will be linked as subpages for their directory
    - this means: grouped under one topic
- you can mix your notes with other files
    - their directories will be ignored unless you will place `.md` file there
    - e.g. `code` directory containing only `test_markers.py` file won't be linked
        - but you can manually place link pointing this file inside your notes
        - e.g. https://github.com/ethru/pdoc3-mdnotes/blob/master/example/test/code/test_markers.py as [see me
        ](https://github.com/ethru/pdoc3-mdnotes/blob/master/example/test/code/test_markers.py)

Just take a look at notebook structure enclosed [here](https://github.com/ethru/pdoc3-mdnotes/tree/master/example).
It will generate following [output](https://ethru.github.io/pdoc3-mdnotes/example/).

## Usage

- **as standalone script**
    - copy `mdnotes.py` from `pdoc3_mdnotes` directory and paste it inside a folder with your notes
    - *optional:* add `templates` directory with customized to your project templates
    - launch script from terminal: `$ python mdnotes.py`
        - *optional:* add execute permission `$ chmod +x mdnotes.py` and run `$ ./mdnotes.py`
- **as command line application**
    - from terminal use one of following: `$ mdnotes`, `$ pdoc3-mdnotes`, `$ pdoc3_mdnotes`, `$ python -m pdoc3_mdnotes`
    to run program in current working directory
    - optional arguments:
        - `-h`, `--help` : to display help
        - `-g`, `--gui` : to launch simple GUI
        - `-n NAME`, `--name NAME` : name of directory where `html` notes will be saved, default is: `docs`. Path can be
        used as well. Relative will navigate from project directory (specified by `-p`, `--path`)
        - `-p PATH`, `--path PATH` : path to directory containing notes (`.md` files), when not specified path where 
        program is run will be used
        - `-t TEMPLATES`, `--templates TEMPLATES` : path to directory with templates, when not specified directory 
        `templates` in path where program is run will be used if it exists else default templates are processed
- **as GUI application**
    - write down absolute path to notes in application entry or use browse button
    - press `Create` to generate `html` notes in `docs` directory inside written down path
    - success or error notification will be displayed
    
![Menu](https://raw.githubusercontent.com/ethru/pdoc3-mdnotes/master/data/menu.png)

## Project Information

##### Documentation

Generated by [pdoc3](https://pdoc3.github.io/pdoc/) and included in 
[docs](https://github.com/ethru/pdoc3-mdnotes/tree/master/docs) directory. Open it 
[here](https://ethru.github.io/pdoc3-mdnotes/).

##### Requirements

- Python3.6+
- Check [requirements.txt](https://raw.githubusercontent.com/ethru/pdoc3-mdnotes/master/requirements.txt) file to see 
used modules.

##### Author

Adrian Niec

##### License

This project is under the MIT License with exclusion of code interacting with [pdoc](https://pdoc3.github.io/pdoc/) 
which is licensed as [GNU AGPL-3.0+](https://raw.githubusercontent.com/pdoc3/pdoc/master/LICENSE.txt).

***Note:** this extension does not modify [pdoc](https://pdoc3.github.io/pdoc/) installation. It is separate module 
which uses elements provided by [pdoc](https://pdoc3.github.io/pdoc/doc/pdoc/#programmatic-usage) to generate html 
notebook from markdown files. For this purpose original templates were downloaded and adjusted from [source
](https://github.com/pdoc3/pdoc/tree/master/pdoc/templates).*
