"""#### GUI

Module gathers classes and methods necessary to create GUI. Its divided for two
blocks `Directory` and `Buttons` both extending `tkinter.Frame`. `Directory`
holds label, path entry and browse button. In `Buttons` frame there are bottom
buttons with their functions. `Gui` connects each part and places them in main
window which will be displayed. Modules used: `pathlib`, `sys` and `tkinter`
with `filedialog`, `messagebox`.


#### License
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
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msg

from pdoc3_mdnotes import mdnotes


class Gui(tk.Tk):
    """
    Configures GUI. Places individual widgets and allows their communication.
    Extends `tk.Tk`.

    ...

    Attributes
    ----------
    directory : Directory
        used for communication with `Directory` widget
    """

    def __init__(self, title, size):
        """
        Parameters
        ----------
        title : str
            name of application, displayed on top bar
        size : str
            application size in format 'heightxwidth'
        """
        super().__init__(className=title)
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)
        self.iconphoto(False,
                       tk.PhotoImage(file=self.get_image('mdnotes.png')))

        self.directory = Directory(self)
        self.directory.grid(row=0, column=0, padx=20, pady=25)
        buttons = Buttons(self)
        buttons.grid(row=1, column=0, padx=10, pady=15, sticky='SE')

        self.bind('<Return>', buttons.create_notes)
        self.bind('<Escape>', sys.exit)

    @staticmethod
    def get_image(name):
        """Gets image path.

        According to type of installation picks method to get image path. It
        can by obtained from module directory or from `_MEIPASS` when
        application is built.

        Parameters
        ----------
        name : str
            name of image with extension to get

        Returns
        -------
        pathlib.Path
            image path
        """
        directory = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        return Path(directory) / 'icons' / name


class Directory(tk.Frame):
    """
    Creates directory widget. Extends `tk.Frame`.

    ...

    Attributes
    ----------
    home : pathlib.Path
        home directory path displayed in entry on application startup, set as
        initial directory for browse button
    icon : tk.PhotoImage
        object containing icon used with browse button
    variable : tk.StringVar
        stores value for path used in application, displayed in entry
    """

    def __init__(self, menu):
        """
        Parameters
        ----------
        menu : Gui
            container where `Directory` widget will be bound
        """
        super().__init__(menu)
        self.home = Path.home()
        self.icon = tk.PhotoImage(file=menu.get_image('browse.png'))
        self.variable = tk.StringVar(self, value=self.home)
        self.display()

    def display(self):
        """Creates frame elements: label, entry and button."""
        tk.Label(self, text='Path: ', font='none 10').grid(row=0, column=0)
        tk.Entry(self,
                 textvariable=self.variable,
                 width=42).grid(row=0, column=1, padx=5)
        tk.Button(self, text='Browse',
                  width=20, height=20,
                  image=self.icon,
                  command=self.browse).grid(row=0, column=2)

    def browse(self):
        """Uses `tkinter.askdirectory` to pick directory.

        Initial directory is set to `self.home`. When user picks new one
        `self.variable` is updated.
        """
        self.variable.set(askdirectory(initialdir=self.home))


class Buttons(tk.Frame):
    """
    Creates buttons widget. Extends `tk.Frame`.

    ...

    Methods
    -------
    get_path
        method bound to get path from application entry
    """

    def __init__(self, menu):
        """
        Parameters
        ----------
        menu : Gui
            container where `Buttons` widget will be bound
        """
        super().__init__(menu)
        tk.Button(self, text='Create', width=7,
                  command=self.create_notes).grid(row=0, column=0)
        tk.Button(self, text='Exit', width=7,
                  command=sys.exit).grid(row=0, column=1)
        self.get_path = menu.directory.variable.get

    def create_notes(self, *_):
        """Makes `html` notes.

        If path from application entry is correct it creates `html` notes with
        `pdoc3_mdnotes.mdnotes.main` function. In case of error appropriate
        notification is displayed.
        """
        try:
            path = Path(self.get_path())
            if not path.is_absolute():
                raise AttributeError
            mdnotes.main(path)
            msg.showinfo('Success',
                         'Notes created in set directory. Exiting...')
            sys.exit()
        except mdnotes.ACCESS_ERRORS:
            msg.showerror('Error',
                          ('Wrong path. It must be a directory with write '
                           'permission. Use absolute path only, e.g. Windows: '
                           r'"C:\Desktop\Files", Linux: "/home/user/Files".')
                          )


def main():
    """Adjusts GUI width according to used platform then creates it."""
    width = '400' if sys.platform == 'win32' else '460'
    Gui('pdoc3-mdnotes', f'{width}x130').mainloop()


if __name__ == '__main__':
    main()
