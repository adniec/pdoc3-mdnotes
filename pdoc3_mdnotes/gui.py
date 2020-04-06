from pathlib import Path
import sys
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msg
import webbrowser

from pdoc3_mdnotes import mdnotes


class Gui(tk.Tk):
    def __init__(self, title, size):
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
        directory = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        return Path(directory) / 'icons' / name


class Directory(tk.Frame):
    def __init__(self, menu):
        super().__init__(menu)
        self.home = Path.home()
        self.icon = tk.PhotoImage(file=menu.get_image('browse.png'))
        self.variable = tk.StringVar(self, value=self.home)
        self.display()

    def display(self):
        tk.Label(self, text='Path: ', font='none 10').grid(row=0, column=0)
        tk.Entry(self,
                 textvariable=self.variable,
                 width=42).grid(row=0, column=1, padx=5)
        tk.Button(self, text='Browse',
                  width=20, height=20,
                  image=self.icon,
                  command=self.browse).grid(row=0, column=2)

    def browse(self):
        self.variable.set(askdirectory(initialdir=self.home))


class Buttons(tk.Frame):
    def __init__(self, menu):
        super().__init__(menu)
        tk.Button(self, text='Submit', width=7,
                  command=self.create_notes).grid(row=0, column=0)
        tk.Button(self, text='About', width=7,
                  command=self.open_homepage).grid(row=0, column=1)
        self.get_path = menu.directory.variable.get

    def create_notes(self, *_):
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
                           r'"C:\Desktop\Files", Linux: "/home/user/Files".'))

    @staticmethod
    def open_homepage():
        webbrowser.open('https://ethru.github.io/pdoc3-mdnotes/', new=True)


def main():
    width = '400' if sys.platform == 'win32' else '460'
    Gui('pdoc3-mdnotes', f'{width}x130').mainloop()


if __name__ == '__main__':
    main()
