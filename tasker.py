import json
import os

# the file everything lives in
TASKS_FILE = "tasks.json"
# what a brand new file should contain
EMPTY_DATA = {"nextId": 1, "tasks": []}

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

if __name__ == "__main__":
    # temporary test code — delete once step 1 starts
    data = load_tasks()
    print(data)