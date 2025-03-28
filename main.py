import tkinter as tk
from tkinter.constants import *
from ttkbootstrap.constants import *
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
class App(ttk.Window):
    def __init__(self, _title:str, _size:tuple):
        super().__init__(themename='journal')

        #Window
        self.title(_title)
        self.geometry(f'{_size[0]}x{_size[1]}')
        self.minsize(_size[0], _size[1])
        self.maxsize(_size[0], _size[1])

        #Frames
        self.header = Header(self)
        self.header.pack(fill='x', anchor='n')

        self.body:Body = Body(self)
        self.body.pack(fill='both', expand=True)
    
        
class Header(tk.Frame):
    def __init__(self, master:App):
        super().__init__(master)

        #Widgets
        self.add_button:ttk.Button = ttk.Button(self, text='Add Task', command=self.add_item)        
        self.add_entry:ttk.Entry = ttk.Entry(self)
        self.clear_button:ttk.Button = ttk.Button(self, text='Clear', style=(DANGER, OUTLINE), command=lambda: self.clear())
        self.master_app:App = master

        self.add_button.pack(fill='x', side='left')
        self.add_entry.pack(expand=True, fill='x', side='left')
        self.clear_button.pack(fill='x', side='right')


    def add_item(self):
        item_text = self.master.header.add_entry.get()
        if not item_text:
            return
        self.master.header.add_entry.delete(0, END)        

        write_data(f'---{item_text}\n')
        self.master.body.load_todo_items()
    
    def clear(self):
        write_data("", write_mode='w')
        [widget.destroy() for widget in self.master_app.body.completed_tasks_list.winfo_children()]
        [widget.destroy() for widget in self.master_app.body.incomplete_tasks_list.winfo_children()]
        
        

class TodoItem(tk.Frame):
    complete_items:list[str] = []
    incomplete_items:list[str] = []

    def __init__(self, master, master_body, label_text:str, is_completed:bool = False):

        #Config
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)

        self.master_body = master_body
        self.label_text = label_text

        #Checkbutton
        self.checkbutton = ttk.Checkbutton(self, command=self.update_item_completion_status)
        self.checkbutton.invoke()

        if is_completed == False:
            self.checkbutton.invoke()
            TodoItem.incomplete_items.append(label_text)
        else:
            TodoItem.complete_items.append(label_text)

        
        #Label
        self.label = ttk.Label(self, text=label_text, wraplength=150)

        #Placement
        self.checkbutton.grid(row=0, column=0, sticky='w')
        self.label.grid(row=0, column=1, sticky='w')
    
    def update_item_completion_status(self):
        if not self.checkbutton.grid_info():
            return

        new_lines = []
        for line in read_data():

            clean_line = line.removeprefix("+++").removeprefix("---").rstrip()
            if not clean_line:
                continue
            if clean_line == self.label_text:
                
                if 'selected' in self.checkbutton.state():
                    line = f'+++{clean_line}\n'
                    TodoItem.incomplete_items.remove(clean_line)
                else:
                    line = f'---{clean_line}\n'
                    TodoItem.complete_items.remove(clean_line)

                
            new_lines.append(line)

        write_data(''.join(new_lines), 'w')
        self.master_body.load_todo_items()
        self.destroy()        

class TasksList(tk.LabelFrame):
    def __init__(self, master, label_text:str):
        super().__init__(master, text=label_text, labelanchor='n', pady=8)
        self.pack_propagate(False)
        
        

class Body(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background='red')

        self.completed_tasks_list:TasksList = TasksList(self, 'Completed Tasks')
        self.incomplete_tasks_list:TasksList = TasksList(self, 'Incomplete Tasks')
        
        self.incomplete_tasks_list.pack(side='right', expand=True, fill='both', pady=16)
        self.completed_tasks_list.pack(side='left', expand=True, fill='both', pady=16)
        
    def load_todo_items(self):
        items = read_data()

        #Placing TodoItems
        for item in items:
            item = item.rstrip()

            #Completed Tasks
            if item.startswith("+++"):
                item = item.removeprefix("+++")

                if item in TodoItem.complete_items:
                    continue

                todo_item = TodoItem(self.completed_tasks_list, self,item, is_completed=True)
                todo_item.pack(anchor='n', fill='x', padx=32)
            
            #Incomplete Tasks
            elif item.startswith("---"):
                item = item.removeprefix("---")


                if item in TodoItem.incomplete_items:
                    continue
                    

                todo_item = TodoItem(self.incomplete_tasks_list, self,item, is_completed=False)
                todo_item.pack(anchor='n', fill='x', padx=32)


application = App('World\'s greatest Todo App', (500,500))
application.body.load_todo_items()
application.mainloop()