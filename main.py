import tkinter as tk
from tkinter.constants import *
import ttkbootstrap as ttk

def write_data(data:str, write_mode = 'a'):
    with open("data.txt", write_mode) as file:
        file.write(data)

def read_data() -> list[str]:
    try:
        with open("data.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError or FileExistsError:
        with open("data.txt", "w") as file:
            file.write("")

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
        self.add_button:ttk.Button = ttk.Button(self, text='Add Task', command=lambda: add_item(master))        
        self.add_entry:ttk.Entry = ttk.Entry(self)

        self.add_button.pack(expand=True, fill='x', side='left')
        self.add_entry.pack(expand=True, fill='x', side='right')




class TodoItem(tk.Frame):
    complete_items:list[str] = []
    incomplete_items:list[str] = []

    def __init__(self, master, label_text:str, is_completed:bool = False):

        #Config
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)

        #Checkbutton
        self.checkbutton = ttk.Checkbutton(self)
        self.checkbutton.invoke()

        if is_completed == False:
            self.checkbutton.invoke()
            TodoItem.incomplete_items.append(label_text)
        else:
            TodoItem.complete_items.append(label_text)

        
        #Label
        self.label = ttk.Label(self, text=label_text)

        #Placement
        self.checkbutton.grid(row=0, column=0, sticky='e')
        self.label.grid(row=0, column=1, sticky='w')

class Body(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)

        #Widgets
        testItem = TodoItem(self, 'Remove this todo item')
        testItem.grid(column=0)

    def load_todo_items(self):
        items = read_data()

        #Placing TodoItems
        for item in items:
            # item = item.removeprefix("+++").removeprefix("---").rstrip() 
            item = item.rstrip()

            if item.startswith("+++"):
                item = item.removeprefix("+++")

                if item in TodoItem.complete_items:
                    continue

                print(item, TodoItem.complete_items)
                todo_item = TodoItem(self, item, is_completed=True)
                todo_item.grid(column=1)
                
            elif item.startswith("---"):
                item = item.removeprefix("---")

                if item in TodoItem.incomplete_items:
                    continue
                    

                print(item, TodoItem.incomplete_items)
                todo_item = TodoItem(self, item, is_completed=False)
                todo_item.grid(column=0)

def add_item(app:App):
    item_text = app.header.add_entry.get()
    app.header.add_entry.delete(0, END)        

    write_data(f'---{item_text}\n')

    
    app.body.load_todo_items()

application = App('World\'s greatest Todo App', (500,500))
application.body.load_todo_items()
application.mainloop()