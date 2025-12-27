import os
import json
import datetime
from time import sleep

def main():
    
    create_file()
    print("-"*60)
    print("- Please, choose an option below")
    options = ["1. Create new task",
               "2. Update a task",
               "3. Delete a task",
               "4. List tasks",
               "5. Exit"]
    
    for option in options:
        print(option)

    selected_option = int(input("- Type the chosen option number: "))
    print("-"*60)

    match selected_option:
        case 1:
            create_task()
        case 2:
            update_task()
        case 3:
            delete_task()
        case 4:
            list_options = {
                      1: None,
                      2: "Done",
                      3: "In progress",
                      4: "To do"
                     }

            print("Which type of tasks you want to list?")
            print("1. All tasks \n2. Tasks done \n3. Tasks in progress \n4. Tasks to do")
            selected_status = int(input("- Type the chosen option number: "))

            if selected_status not in list_options.keys():
                selected_status = 1

            list_tasks(list_options[selected_status])        
        case 5:
            return print("Bye! See you later \n")
        case _:
            print("- The selected option was not found, please choose a new one.")
            sleep(1)
            return main()
    
def greetings():
    return print("- Welcome to your task manager")

def create_file():
    """ Checks if tasks.json exists, if not exists, creates it with
    an empty list """

    if not os.path.exists("tasks.json"):
        with open("tasks.json", "w+", encoding="utf-8") as f:
            f.write(json.dumps([], ensure_ascii=False, indent=4))

def read_json():
    """ Reads tasks.json and returns a python list """

    with open("tasks.json", "r", encoding="utf-8") as f:
        tasks_list = json.load(f)
        return tasks_list
    
def write_json(data):
    """ Receives a json data and writes into tasks.json """

    with open("tasks.json", "w+", encoding="utf-8") as f:
        f.write(data)

def create_task():
    """ Receives a new task and create a new json object that will be
    appended into json list of all tasks"""

    task = str(input("- Type the task name: "))
    
    tasks_list = read_json()
    new_task = {
            'id': len(tasks_list) + 1,
            'description': task,
            'status': 'To do',
            'createdAt': datetime.datetime.now().strftime("%d/%m/%Y - %X"),
            'updatedAt': datetime.datetime.now().strftime("%d/%m/%Y - %X")
        }
    
    tasks_list.append(new_task)
    json_tasks = json.dumps(tasks_list, indent=4, ensure_ascii=False)
    
    try:
        write_json(json_tasks)
    except:
        print("Something went wrong \n")

    print("- New task successfully added! \n")

    sleep(1)
    return main()

def update_task():
    """ Updates a task by its id """

    status = [
        "Done",
        "In progress",
        "To do"
    ]

    task_id = int(input("- Type the id of the task you want to update: "))
    selected_status = int(input("""Choose a new status for your tasks:  
    1. Done  
    2. In progress  
    3. To do\n"""))

    new_status = status[selected_status-1]

    tasks_list = read_json()
    for task in tasks_list:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.datetime.now().strftime("%d/%m/%Y - %X")
            found = True
            break

        found = False

    if not found:
        print(f"- The #{task_id} task does not exists, please type a valid one \n")
        return update_task()

    json_tasks = json.dumps(tasks_list, indent=4, ensure_ascii=False)
    write_json(json_tasks)

    print(f"- The #{task_id} task was sucessfully updated \n")

    sleep(1)
    return main()

def delete_task():
    task_id = int(input("- Type the id of the task you want to delete: "))
    tasks_list = read_json()

    for key, task in enumerate(tasks_list):
        if task['id'] == task_id:
            tasks_list.pop(key)
            found = True
            break
        found = False

    if not found:
        print(f"- The #{task_id} task does not exists, please type a valid one \n")
        return delete_task()

    json_tasks = json.dumps(tasks_list, indent=4, ensure_ascii=False)
    write_json(json_tasks)

    print(f"- The #{task_id} task was deleted! \n")

    sleep(1)
    return main()

def list_tasks(status):
    tasks_list = read_json()
    columns = {
                " Task ID": 8, "Description": 28, "Status": 12, "Created At": 22, "Updated At": 22
            }

    header = "|"
    for task in columns.keys():
        width = columns[task]
        header += f"{task.center(width)} |" 

    print("-"*103)
    print(header)
    print("-"*103)

    for task in tasks_list:
        row = "|"
        row += f"# {task['id']}".center(9) + "|"
        row += f" {task['description']}".ljust(28) + " |"
        row += f"{task['status']}".center(13) + "|"
        row += f" {task['createdAt']} |"
        row += f" {task['updatedAt']} |"
        
        if task['status'] == status:
            print(row)
        elif status == None:
            print(row)

    print("-"*103 + "\n")
    sleep(1)
    return main()

if __name__ == "__main__":
    greetings()
    main()