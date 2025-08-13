import os
import json
import csv
import argparse
from datetime import datetime

# File to store tasks
FILE_NAME = "tasks.txt"

# Load tasks from file
def load_tasks():
    tasks = {}
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(" | ")
                if len(parts) == 5:
                    task_id, title, status, deadline, priority = parts
                else:
                    task_id, title, status = parts
                    deadline, priority = "", ""
                tasks[int(task_id)] = {
                    "title": title,
                    "status": status,
                    "deadline": deadline,
                    "priority": priority
                }
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for task_id, task in tasks.items():
            file.write(f"{task_id} | {task['title']} | {task['status']} | {task['deadline']} | {task['priority']}\n")

# Add a new task
def add_task(tasks, title=None, deadline=None, priority=None):
    if not title:
        title = input("Enter task title: ")
    if not deadline:
        deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ")
    if not priority:
        priority = input("Enter priority (High/Medium/Low) or leave blank: ")

    task_id = max(tasks.keys(), default=0) + 1
    tasks[task_id] = {
        "title": title,
        "status": "incomplete",
        "deadline": deadline,
        "priority": priority
    }
    print(f"Task '{title}' added.")

# View all tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
    else:
        for task_id, task in tasks.items():
            print(f"[{task_id}] {task['title']} - {task['status']} "
                  f"(Deadline: {task['deadline']}, Priority: {task['priority']})")

# Mark task as complete
def mark_task_complete(tasks, task_id=None):
    if task_id is None:
        task_id = int(input("Enter task ID to mark as complete: "))
    if task_id in tasks:
        tasks[task_id]["status"] = "complete"
        print(f"Task '{tasks[task_id]['title']}' marked as complete.")
    else:
        print("Task ID not found.")

# Delete a task
def delete_task(tasks, task_id=None):
    if task_id is None:
        task_id = int(input("Enter task ID to Delete: "))
    if task_id in tasks:
        deleted_task = tasks.pop(task_id)
        print(f"Task '{deleted_task['title']}' deleted.")
    else:
        print("Task ID not found.")

# Export tasks to JSON
def export_to_json(tasks, filename="tasks.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)
    print(f"Tasks exported to {filename}")

# Export tasks to CSV
def export_to_csv(tasks, filename="tasks.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "Status", "Deadline", "Priority"])
        for task_id, task in tasks.items():
            writer.writerow([task_id, task["title"], task["status"], task["deadline"], task["priority"]])
    print(f"Tasks exported to {filename}")

# Main Menu
def main():
    parser = argparse.ArgumentParser(description="Task Manager with Extra Features")
    parser.add_argument("--add", nargs="+", help="Add a new task: title [deadline priority]")
    parser.add_argument("--complete", type=int, help="Mark a task complete by ID")
    parser.add_argument("--delete", type=int, help="Delete a task by ID")
    parser.add_argument("--view", action="store_true", help="View all tasks")
    parser.add_argument("--export-json", action="store_true", help="Export tasks to JSON")
    parser.add_argument("--export-csv", action="store_true", help="Export tasks to CSV")
    args = parser.parse_args()

    tasks = load_tasks()

    # Command-line mode
    if args.add:
        title = args.add[0]
        deadline = args.add[1] if len(args.add) > 1 else ""
        priority = args.add[2] if len(args.add) > 2 else ""
        add_task(tasks, title, deadline, priority)

    if args.complete is not None:
        mark_task_complete(tasks, args.complete)

    if args.delete is not None:
        delete_task(tasks, args.delete)

    if args.view:
        view_tasks(tasks)

    if args.export_json:
        export_to_json(tasks)

    if args.export_csv:
        export_to_csv(tasks)

    # Save changes if any CLI actions were performed
    if any([args.add, args.complete is not None, args.delete is not None]):
        save_tasks(tasks)

    # Interactive menu if no CLI args
    if not any(vars(args).values()):
        while True:
            print("\nTask Manager Menu:")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as complete")
            print("4. Delete Task")
            print("5. Export to JSON")
            print("6. Export to CSV")
            print("7. Save & Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                view_tasks(tasks)
            elif choice == "3":
                mark_task_complete(tasks)
            elif choice == "4":
                delete_task(tasks)
            elif choice == "5":
                export_to_json(tasks)
            elif choice == "6":
                export_to_csv(tasks)
            elif choice == "7":
                save_tasks(tasks)
                print("Goodbye")
                break
            else:
                print("Invalid Choice. Please try again")

if __name__ == "__main__":
    main()
