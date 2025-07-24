import tkinter as tk
from tkinter import messagebox
import json

# Load tasks from file
def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

# Classify task based on Eisenhower Matrix
def classify_task(urgent, important):
    if urgent and important:
        return "Do First"
    elif not urgent and important:
        return "Schedule"
    elif urgent and not important:
        return "Delegate"
    else:
        return "Eliminate"

# Add task
def add_task():
    def submit_task():
        task_name = entry_task.get()
        urgent = var_urgent.get()
        important = var_important.get()
        time_required = entry_time.get()

        if not task_name:
            messagebox.showwarning("Input Error", "Task name cannot be empty.")
            return

        try:
            time_required = float(time_required)
        except ValueError:
            messagebox.showwarning("Input Error", "Time required must be a number.")
            return

        category = classify_task(urgent, important)
        task = {
            "task": task_name,
            "urgent": urgent,
            "important": important,
            "category": category,
            "time": time_required,
            "done": False
        }
        tasks.append(task)
        rearrange_tasks()
        save_tasks()
        refresh_display()
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Add Task")
    popup.geometry("300x250")

    tk.Label(popup, text="Task:").pack(pady=5)
    entry_task = tk.Entry(popup, width=30)
    entry_task.pack(pady=5)

    var_urgent = tk.BooleanVar()
    var_important = tk.BooleanVar()

    tk.Checkbutton(popup, text="Urgent", variable=var_urgent).pack()
    tk.Checkbutton(popup, text="Important", variable=var_important).pack()

    tk.Label(popup, text="Estimated Time (hrs):").pack(pady=5)
    entry_time = tk.Entry(popup, width=10)
    entry_time.pack(pady=5)

    tk.Button(popup, text="Add", command=submit_task).pack(pady=10)

# Mark task as completed
def complete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]["done"] = True
        save_tasks()
        refresh_display()

# Delete task
def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        save_tasks()
        refresh_display()

# Rearrange tasks by custom priority (urgent, important, time)
def rearrange_tasks():
    def task_priority(t):
        # Binary weights for 3-bit sorting
        urgency = 1 if t["urgent"] else 0
        importance = 1 if t["important"] else 0
        return (-importance, -urgency, t.get("time", 9999))  # default high time for old tasks

    tasks.sort(key=task_priority)

# Refresh display
def refresh_display():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✓" if task["done"] else "✗"
        entry = f"[{status}] ({task.get('category', 'Uncategorized')}) {task.get('task', 'Unnamed')} - {task.get('time', '?')} hrs"

        listbox.insert(tk.END, entry)

# Main GUI setup
tasks = load_tasks()
rearrange_tasks()

root = tk.Tk()
root.title("To-Do List - Eisenhower Matrix")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

listbox = tk.Listbox(frame, width=80, height=15)
listbox.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Task", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Complete Task", command=complete_task).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Task", command=delete_task).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Save", command=save_tasks).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(button_frame, text="Exit", command=root.quit).grid(row=1, column=2, pady=5)

refresh_display()
root.mainloop()
