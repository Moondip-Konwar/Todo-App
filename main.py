import tkinter as tk
from tkinter.constants import *
import ttkbootstrap as ttk

class App(tk.Tk):
    def __init__(self, _title:str, _size:tuple):
        super().__init__()

        #Window
        self.title(_title)
        self.geometry(f'{_size[0]}x{_size[1]}')

        #Frames
        self.header = Header(self)
        self.header.pack(expand=True, fill='x', anchor='n')

        self.body = Body(self)
        self.body.pack(expand=True, fill='both')

class Header(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        #Widgets
        self.add_button:ttk.Button = ttk.Button(self, text='Add Task')        
        self.add_entry:ttk.Entry = ttk.Entry(self)

        self.add_button.pack(expand=True, fill='x', side='left')
        self.add_entry.pack(expand=True, fill='x', side='right')

class Body(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)

        #Widgets
        # testItem = TodoItem(self, 'Remove this todo item')
        # testItem.grid(column=0)

class TodoItem(tk.Frame):
    def __init__(self, master, label_text:str, check_button_state = ON):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)

        self.checkbutton = ttk.Checkbutton(self, command= lambda: print(self.checkbutton.state()))
        self.checkbutton.invoke()

        if not check_button_state == ON:
            self.checkbutton.invoke()
        self.label = ttk.Label(self, text=label_text)

        self.checkbutton.grid(row=0, column=0, sticky='e')
        self.label.grid(row=0, column=1, sticky='w')
        


app = App('World\'s greatest Todo App', (500,500))

app.mainloop()