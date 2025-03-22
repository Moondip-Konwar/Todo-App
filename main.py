from tkinter import ttk
import tkinter as tk
from tkinter.constants import *

class App(tk.Tk):
    def __init__(self, _title:str, _size:tuple):

        #Window
        super().__init__()
        
        self.title(_title)
        self.geometry(f'{_size[0]}x{_size[1]}')
        
        #Start
        self.mainloop()



app = App('World\'s greatest Todo App', (500,500))

