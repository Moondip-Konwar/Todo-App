from tkinter import ttk
import tkinter as tk
from tkinter.constants import *

class App(tk.Tk):
    def __init__(self, _title:str, _size:tuple):
        super().__init__()

        #Window
        self.title(_title)
        self.geometry(f'{_size[0]}x{_size[1]}')

        #Frames
        self.header = Header(self)
        self.header.pack(expand=True, fill='x', anchor='n')

class Header(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        #Add button #Add entry
        self.add_button:ttk.Button = ttk.Button(self, text='Add Task')        
        self.add_entry:ttk.Entry = ttk.Entry(self)

        self.add_button.pack(expand=True, fill='x', side='left')
        self.add_entry.pack(expand=True, fill='x', side='right', ipady=4)


app = App('World\'s greatest Todo App', (500,500))

app.mainloop()