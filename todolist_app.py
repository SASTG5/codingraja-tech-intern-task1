#!/usr/bin/env python
# coding: utf-8

# In[37]:


import tkinter as tk
from tkinter import messagebox
from datetime import datetime,date
import sys
import requests


class TodoList:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    task_data = line.strip().split('|')
                    task = {
                        "text": task_data[0],
                        "priority": task_data[1],
                        "due_date": datetime.strptime(task_data[2], "%Y-%m-%d").date() if task_data[2] != "None" else None,
                        "completed": bool(int(task_data[3]))
                    }
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        with open(self.filename, "w") as file:
            for task in self.tasks:
                due_date_str = task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else "None"
                file.write(f"{task['text']}|{task['priority']}|{due_date_str}|{int(task['completed'])}\n")

    def add_task(self, task_text, priority, due_date=None):
        task = {"text": task_text, "priority": priority, "due_date": due_date, "completed": False}
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        del self.tasks[index]
        self.save_tasks()

    def mark_as_completed(self, index):
        self.tasks[index]["completed"] = True
        self.save_tasks()

    def get_task_list(self):
        return self.tasks

class TodoListApp:
    def __init__(self, master, todo_list):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("500x700")
        self.todo_list = todo_list
        self.create_widgets()

    def create_widgets(self):
        # Task input
        self.task_entry = tk.Entry(self.master, width=30)
        self.task_entry.pack(pady=10)

        # Priority dropdown
        self.priority_var = tk.StringVar()
        self.priority_var.set("Low")
        priority_options = ["Low", "Medium", "High"]
        self.priority_dropdown = tk.OptionMenu(self.master, self.priority_var, *priority_options)
        self.priority_dropdown.pack(pady=10)

        # Due date input
        self.due_date_entry = tk.Entry(self.master, width=30)
        self.due_date_entry.insert(0, "YYYY-MM-DD")  # Placeholder text
        self.due_date_entry.pack(pady=10)

        # Add task button
        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        # Task list
        self.task_listbox = tk.Listbox(self.master, height=15, width=50)
        self.task_listbox.pack(pady=10)
        self.update_task_listbox()

        # Remove task button
        self.remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=10)

        # Mark as completed button
        self.complete_button = tk.Button(self.master, text="Mark as Completed", command=self.mark_as_completed)
        self.complete_button.pack(pady=10)

    def add_task(self):
        task_text = self.task_entry.get()
        priority = self.priority_var.get()
        due_date_str = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str != "None" else None
        except ValueError:
            due_date = None

        if task_text:
            self.todo_list.add_task(task_text, priority, due_date)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            self.todo_list.remove_task(selected_index[0])
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def mark_as_completed(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            self.todo_list.mark_as_completed(selected_index[0])
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list.get_task_list():
            status = "[X]" if task["completed"] else "[ ]"
            due_date_str = task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else "No due date"
            task_text = f"{status} {task['text']} - Priority: {task['priority']} - Due Date: {due_date_str}"
            self.task_listbox.insert(tk.END, task_text)

def main():
    root = tk.Tk()
    todo_list = TodoList()
    app = TodoListApp(root, todo_list)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




