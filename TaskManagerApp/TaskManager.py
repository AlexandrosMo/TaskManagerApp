import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
from pathlib import Path
from datetime import datetime

# Task class to represent each task
class Task:
    def __init__(self, name, priority, due_date=None, is_completed=False):
        self.name = name           # Name of the task
        self.priority = priority   # Priority (high, medium, low)
        self.due_date = due_date   # Due date in "YYYY-MM-DD" format
        self.is_completed = is_completed  # Whether the task is completed or not

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"  # Task status
        deadline = f" | Due: {self.due_date}" if self.due_date else ""  # Due date string
        return f"{self.name} - {self.priority.capitalize()} Priority - {status}{deadline}"

    # Convert the task object to a dictionary for saving to JSON
    def to_dict(self):
        return {
            "name": self.name,
            "priority": self.priority,
            "due_date": self.due_date,
            "is_completed": self.is_completed,
        }

    # Create a Task object from a dictionary (used for loading from JSON)
    @staticmethod
    def from_dict(data):
        return Task(data["name"], data["priority"], data.get("due_date"), data["is_completed"])

# The main class that manages the task list and GUI
class TaskManagerApp:
    def __init__(self, root):
        self.tasks = []            # List to hold tasks
        self.data_file = Path("tasks.json")  # Path to the JSON file for saving/loading tasks
        self.load_tasks()  # Load any existing tasks from the file

        # Main Window Setup
        self.root = root
        self.root.title("Task Manager")

        # Task Listbox to display tasks
        self.task_listbox = tk.Listbox(root, width=60, height=15)
        self.task_listbox.pack(pady=10)

        # Button to add a new task
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task, width=15)
        self.add_task_button.pack(pady=5)

        # Button to edit a selected task
        self.edit_task_button = tk.Button(root, text="Edit Task", command=self.edit_task, width=15)
        self.edit_task_button.pack(pady=5)

        # Button to delete a selected task
        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task, width=15)
        self.delete_task_button.pack(pady=5)

        # Button to mark a task as completed
        self.mark_complete_button = tk.Button(root, text="Mark as Completed", command=self.mark_task_as_completed, width=15)
        self.mark_complete_button.pack(pady=5)

        # Filter dropdown menu to filter tasks by status
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ttk.Combobox(root, textvariable=self.filter_var, values=["All", "Pending", "Completed"], state="readonly")
        self.filter_menu.pack(pady=5)
        self.filter_menu.bind("<<ComboboxSelected>>", lambda e: self.refresh_task_list())

        # Button to refresh the task list
        self.refresh_button = tk.Button(root, text="Refresh Task List", command=self.refresh_task_list, width=15)
        self.refresh_button.pack(pady=5)

        # Initially refresh the task list to display any existing tasks
        self.refresh_task_list()

    # Save the tasks to the JSON file
    def save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    # Load tasks from the JSON file if it exists
    def load_tasks(self):
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                self.tasks = [Task.from_dict(data) for data in json.load(f)]

    # Method to add a new task
    def add_task(self):
        name = simpledialog.askstring("Add Task", "Enter task name:")
        if not name:
            return

        priority = simpledialog.askstring(
            "Add Task", "Enter task priority (High/Medium/Low):"
        )
        if priority is None or priority.lower() not in ("high", "medium", "low"):
            messagebox.showerror("Invalid Input", "Priority must be High, Medium, or Low.")
            return

        due_date = simpledialog.askstring("Add Task", "Enter due date (YYYY-MM-DD) or leave blank:")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
            except ValueError:
                messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
                return

        # Add the new task to the list
        self.tasks.append(Task(name, priority.lower(), due_date))
        self.save_tasks()  # Save to file
        messagebox.showinfo("Task Added", f"Task '{name}' added successfully!")
        self.refresh_task_list()  # Refresh the list display

    # Method to edit an existing task
    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return

        selected_task = self.tasks[selected_index[0]]
        new_name = simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=selected_task.name)
        if not new_name:
            return

        new_priority = simpledialog.askstring(
            "Edit Task", "Enter new task priority (High/Medium/Low):", initialvalue=selected_task.priority.capitalize()
        )
        if new_priority is None or new_priority.lower() not in ("high", "medium", "low"):
            messagebox.showerror("Invalid Input", "Priority must be High, Medium, or Low.")
            return

        new_due_date = simpledialog.askstring("Edit Task", "Enter new due date (YYYY-MM-DD) or leave blank:", initialvalue=selected_task.due_date)
        if new_due_date:
            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
                return

        # Update the selected task
        selected_task.name = new_name
        selected_task.priority = new_priority.lower()
        selected_task.due_date = new_due_date
        self.save_tasks()  # Save the updated task list
        messagebox.showinfo("Task Edited", f"Task '{new_name}' updated successfully!")
        self.refresh_task_list()  # Refresh the list display

    # Method to delete a selected task
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        selected_task = self.tasks[selected_index[0]]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_task.name}'?")
        if confirm:
            self.tasks.pop(selected_index[0])  # Remove the task from the list
            self.save_tasks()  # Save the updated task list
            messagebox.showinfo("Task Deleted", f"Task '{selected_task.name}' deleted successfully!")
            self.refresh_task_list()  # Refresh the list display

    # Method to mark a selected task as completed
    def mark_task_as_completed(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to mark as completed.")
            return

        selected_task = self.tasks[selected_index[0]]
        if selected_task.is_completed:
            messagebox.showinfo("Already Completed", "Task is already marked as completed.")
        else:
            selected_task.is_completed = True  # Mark the task as completed
            self.save_tasks()  # Save the updated task list
            messagebox.showinfo("Task Completed", f"Task '{selected_task.name}' marked as completed!")
        self.refresh_task_list()  # Refresh the list display

    # Method to refresh the task list display
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)  # Clear the current list

        filter_option = self.filter_var.get()  # Get the selected filter option
        filtered_tasks = self.tasks
        if filter_option == "Pending":
            filtered_tasks = [task for task in self.tasks if not task.is_completed]  # Show only pending tasks
        elif filter_option == "Completed":
            filtered_tasks = [task for task in self.tasks if task.is_completed]  # Show only completed tasks

        today = datetime.now().date()
        for task in filtered_tasks:
            # Determine task's due date and set color based on priority and due date
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date() if task.due_date else None
            color = "black"
            if due_date and due_date < today:
                color = "red"  # Overdue tasks are red
            elif task.priority == "high":
                color = "orange"
            elif task.priority == "medium":
                color = "blue"
            elif task.priority == "low":
                color = "green"

            # Insert task into the listbox with the appropriate color
            self.task_listbox.insert(tk.END, str(task))
            self.task_listbox.itemconfig(self.task_listbox.size() - 1, {'fg': color})

# Main application execution
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = TaskManagerApp(root)  # Initialize the TaskManagerApp
    root.mainloop()  # Start the Tkinter event loop
