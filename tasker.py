import json
import os
import sys
from pathlib import Path
from datetime import datetime

# the file everything lives in
TASKS_FILE = Path(__file__).parent / "tasks.json"
# what a brand new file should contain
EMPTY_DATA = {"nextId": 1, "tasks": []}

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

def main():
    # no command given at all
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]   # everything after the command

    if command == "add":
        if len(sys.argv) < 2:
                print_help()
                return
        add_task(args[0])
        print("Task added sucessfully!")
        pass

    elif command == "list":
        list_all_tasks()
        pass

    elif command == "help":
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()