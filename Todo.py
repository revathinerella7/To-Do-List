import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = "tasks.txt"

# Color Theme
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2c2f4a"
BTN_COLOR = "#6c63ff"
DONE_COLOR = "#4caf50"
TEXT_COLOR = "#ffffff"

class TodoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("420x520")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.tasks = []

        self.create_ui()
        self.load_tasks()

    def create_ui(self):
        # Title
        tk.Label(
            self.root,
            text="📝 My To-Do List",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=15)

        # Entry
        self.task_entry = tk.Entry(
            self.root,
            font=("Segoe UI", 14),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief=tk.FLAT
        )
        self.task_entry.pack(padx=20, pady=10, fill=tk.X)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Add",
                  width=10, bg=BTN_COLOR, fg="white",
                  font=("Segoe UI", 11, "bold"),
                  command=self.add_task).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Done",
                  width=10, bg=DONE_COLOR, fg="white",
                  font=("Segoe UI", 11, "bold"),
                  command=self.mark_done).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Delete",
                  width=10, bg="#e53935", fg="white",
                  font=("Segoe UI", 11, "bold"),
                  command=self.delete_task).grid(row=0, column=2, padx=5)

        # Listbox
        self.listbox = tk.Listbox(
            self.root,
            font=("Segoe UI", 13),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            selectbackground=BTN_COLOR,
            activestyle="none",
            height=12,
            relief=tk.FLAT
        )
        self.listbox.pack(padx=20, pady=10, fill=tk.BOTH)

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        self.tasks.append(task)
        self.listbox.insert(tk.END, task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            del self.tasks[index]
            self.save_tasks()
        except:
            messagebox.showinfo("Info", "Select a task to delete")

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.tasks[index]

            if not task.startswith("✔ "):
                task = "✔ " + task
                self.tasks[index] = task
                self.listbox.delete(index)
                self.listbox.insert(index, task)
                self.listbox.itemconfig(index, fg=DONE_COLOR)

            self.save_tasks()
        except:
            messagebox.showinfo("Info", "Select a task to mark done")

    def save_tasks(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            for task in self.tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                for line in f:
                    task = line.strip()
                    self.tasks.append(task)
                    self.listbox.insert(tk.END, task)
                    if task.startswith("✔"):
                        self.listbox.itemconfig(tk.END, fg=DONE_COLOR)

if __name__ == "__main__":
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
