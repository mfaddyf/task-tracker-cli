import json
import os
import sys
from pathlib import Path
from datetime import datetime

# the file everything lives in
TASKS_FILE = Path(__file__).parent / "tasks.json"
# what a brand new file should contain
EMPTY_DATA = {"nextId": 1, "tasks": []}
# the three valid statuses 
STATUSES = ["to-do", "in-progress", "done"]

# ---
# ADD 
# ___

def add_task(description):
    """create a new task and save it, return the new task's id."""
    data = load_tasks()
    now = datetime.now().isoformat()

    task = {
        "id": data["nextId"],
        "description": description,
        "note": "",
        "status": "to-do",
        "taskType": "general",
        "createdAt": now,
        "updatedAt": now,
        "dueDate": None,
    }

    # 1. append the task to data["tasks"]
    # 2. increment data["nextId"]
    # 3. save data
    # 4. return the id you just used
    data["tasks"].append(task)
    data["nextId"] += 1
    save_tasks(data)
    return task["id"]

# ---
# DELETE 
# ___

def delete_task(task_id):
    """remove a task from the file."""
    data = load_tasks()
    task = find_task(data["tasks"], task_id)

    # if task is none, print an error and return
    if task is None:
        print(f"Error: no task with id {task_id}.")
        return

    # otherwise:
    # 1. remove it from data["tasks"]
    # 2. save data
    # 3. print a confirmation
    data["tasks"].remove(task)
    save_tasks(data)
    print("Task sucessfully deleted!")
    pass

# ---
# UPDATE 
# ___

def update_task(task_id, new_description):
    """change a task's description."""
    data = load_tasks()
    task = find_task(data["tasks"], task_id)

    if task is None:
        print(f"Error: no task with id {task_id}.")
        return

    task["description"] = new_description
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(data)
    print(f"Task {task_id} updated.")

# ---
# LISTING
# ___

def list_all_tasks():
    """print every task in the file."""
    data = load_tasks()
    tasks = data["tasks"]

    # nothing to show, say so and stop
    if not tasks:
        print("No tasks yet. Add one with: add \"your task\"")
        return

    for task in tasks:
        print(f"{task['id']} | {task['description']} > [{task['status']}]")

# ---
# SEARCHING
# ___

def find_task(tasks, task_id):
    """return the task with this id, or none if there isn't one."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# ---
# EDITING
# ___

"""editing status"""
def mark_task(task_id, new_status):
    """change a task's status and update its timestamp."""
    data = load_tasks()
    task = find_task(data["tasks"], task_id)

    if task is None:
        print(f"Error: no task with id {task_id}.")
        return

    if new_status not in STATUSES:
        print(f"Error: status must be one of: {', '.join(STATUSES)}")
        return

    task["status"] = new_status
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(data)
    print(f"Task {task_id} marked as {new_status}.")

# ---
# SAVING & LOADING
# ___

def load_tasks():
    """read the JSON file and return the data as a dict.
    creates the file first if it doesn't exist."""
    # 1. if the file doesn't exist, save EMPTY_DATA to it
    # 2. open the file for reading
    # 3. use json.load to turn it into a dict
    # 4. return the dict
    if not os.path.exists(TASKS_FILE):
        save_tasks(EMPTY_DATA)
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        save_tasks(EMPTY_DATA)
        return EMPTY_DATA.copy()
        
    pass

def save_tasks(data):
    """write the whole data dict back to the JSON file."""
    # 1. open the file for writing
    # 2. use json.dump to write data into it
    # indent = 2 makes the file readable when you open it yourself
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent = 2)
    pass

# ---
# HELP COMMAND
# ___

def print_help():
    """show the available commands."""
    print("Usage:")
    print("  add \"description\"   add a new task")
    print("  list                 list all tasks")
    print("  help                 show this message")

# ---
# TO RUN APP
# ___

def parse_id(text):
    """turn a command line argument into an id, or none if it isn't a number."""
    try:
        return int(text)
    except ValueError:
        print("Error: id must be a number.")
        return None


def print_help():
    """show the available commands."""
    print("Usage:")
    print("  add \"description\"    add a new task")
    print("  mark ID status       set a task's status (to-do, in-progress, done)")
    print("  list                 list all tasks")
    print("  help                 show this message")


def main():
    # no command given at all
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]   # everything after the command

    # adding a task
    if command == "add":
        if not args:
            print("Error: add needs a description.")
            return
        new_id = add_task(args[0])
        print(f"Task added successfully (ID: {new_id})")

    # changing the status
    elif command == "mark":
        if len(args) < 2:
            print("Error: mark needs an id and a status.")
            print("  e.g. mark 1 done")
            return
        task_id = parse_id(args[0])
        if task_id is None:
            return
        mark_task(task_id, args[1])

    # listing all tasks
    elif command == "list":
        list_all_tasks()

    # listing all commands
    elif command == "help":
        print_help()

    # updating the task
    elif command == "update":
        if len(args) < 2:
                print("Error: update needs //example//.")
                print("  e.g. //")
                return
        task_id = parse_id(args[0])
        if task_id is None:
                return
        update_task(task_id, args[1])

    # deleting the task
    elif command == "delete":
        task_id = parse_id(args[0])
        if task_id is None:
            return
        delete_task(task_id)
        pass

    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()