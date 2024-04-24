# Task manager program for a small business.

from datetime import date  # get current date to use for automation later.
today = date.today()
todays_date_formatted = today.strftime("%d %b %Y")  # Format to match file.

log_in_data = {}

try:
    # Store the usernames and passwords as key, value pairs from external file.
    with open("user.txt", "r", encoding="utf-8") as f:  # File 1.
        for content in f:
            key, value = content.rstrip("\n").split(", ")
            log_in_data[key] = value.split()
            
    admin_password = log_in_data["admin"]  # Store admin password for later.
    
except FileNotFoundError:
    print("Make sure the user.txt file exists and is in the right folder.")
    exit()  # exit app if the file storing usernames and passwords doesn't exist.

while True:  # If user.txt file exists, the app runs. 
    username = input("Please enter your username: ")
    if username in log_in_data.keys():
        password = input("Please enter your password: ")
        
    if username in log_in_data.keys() and password in log_in_data[username]:
        print(f"\nHello, {username}.")
        break
    else:
        print("Those log in details are incorrect!") 

while True:
    menu = input('''\nPlease select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
e - exit
''')
    
    if menu == "r":
        admin_priviledges = input("Enter the password: ")
        if admin_priviledges in admin_password:  # Accessible only by admin password.
            admin_options = input('''\nSelect one of the following options:
                                  ru - register a new user
                                  ds - display statistics
                                  ''')
            if admin_options == "ru":  # New user written to file only if password matches
                register_user_name = input("\nEnter the new username to add: ")
                register_user_password = input("\nWhat will their password be?: ")
                confirm_user_password = input("\nPlease confirm the password: ")
                if confirm_user_password == register_user_password: # If not return to menu.
                    with open("user.txt", "a+", encoding="utf-8") as f:  # Add new user.
                        f.seek(0)  # Set cursor to start of file.
                        f.write("\n")
                        f.write(f"{register_user_name}, {register_user_password}")
                        print("\nThe new user has been successfully added!")
 
            elif admin_options == "ds":  # Gather and display stats.
                with open("user.txt", "r", encoding="utf-8") as f:
                    num_of_users = f.readlines()
                    user_count = len(num_of_users)
                    print(f"Current total users: {user_count}.")

                try:
                    with open("tasks.txt", "r", encoding="utf-8") as f_2:  # File 2.
                     num_of_tasks = f_2.readlines()
                     task_count = len(num_of_tasks)
                     print(f"Total number of tasks: {task_count}.")  
                except FileNotFoundError:  # If user gets stats but tasks.txt doesn't exist
                   print("\nEnsure tasks.txt file exists and is in the same folder.") 
                   
        else:  # The admin-specific menu can't be accessed without the admin password. 
            print("\nThat doesn't match!")
    
    elif menu == "a":
        try:
            with open("user.txt", "r", encoding="utf-8") as f:
                for content in f:  # Enables adding tasks for new user without restarting app.
                   key, val = content.rstrip("\n").split(", ")
                   log_in_data[key] = val.split()
            whose_task = input("Who are you assigning this task to?: ")
            if whose_task not in log_in_data:  # tasks can only be assigned to users.
             raise ValueError("That's an error")
            task = input("Enter a title for the task: ")
            if not task:  # If nothing is entered, user sent back to menu. 
             raise ValueError
            task_description = input("Describe the task: ")
            if not task_description:  # Same as above. User can't enter nothing. 
             raise ValueError
            date_of_task_assignment = input("Enter 'd' to set today as assignment date: ")
            date_of_task_assignment == todays_date_formatted  # Automate today's date.
            if date_of_task_assignment !="d":
             raise ValueError  # User returns to menu if 'd' isn't entered.
            task_due_date = input("When is this task due? (i.e. 01 Feb 2024): ")
            if len(task_due_date.split()) <= 2:
             raise ValueError  # Correct date format needs two spaces.
            task_completion_status = input("Has this task been completed? (yes or no): ")
            if len(task_completion_status) > 3:
             raise ValueError  # Input cannot be greater than 3 characters or 'yes'.
        except ValueError:
          print("\nThat's invalid!")
          continue  # Return to menu upon error messages.

        with open("tasks.txt", "a+", encoding="utf-8") as f_2:  # Add task if no errors. 
         f_2.seek(0)
         f_2.write("\n")
         f_2.write(f"{whose_task.rstrip()}, ")  # Remove space for writing to new line.
         f_2.write(f"{task}, ")
         f_2.write(f"{task_description}, ")
         f_2.write(f"{todays_date_formatted}, ")
         f_2.write(f"{task_due_date}, ")
         f_2.write(f"{task_completion_status}")
        print("\nThe new task has been added!")
                             
    elif menu == "va":
        try:
          with open("tasks.txt", "r", encoding="utf-8") as f_2:
            lines = f_2.readlines()
            content_first_line = 1
            for rows in lines:
                contents = rows.split(", ")
                print(content_first_line, end=" ")
                content_first_line +=1  # Increment line by line to read content of tasks.txt
                print(f"\nAssigned to:      {contents[0]}")
                print(f"Task:      {contents[1]}")
                print(f"Task description:     {contents[2]}")
                print(f"Date assigned:     {contents[3]}")
                print(f"Due date:     {contents[4]}")
                print(f"Task complete? {contents[5]}")
                print("\n")
        except FileNotFoundError:
           print("\nEnsure original tasks.txt file exists and in right folder.")
        except IndexError:  # Error shown if tasks.txt doesn't exist.
           print("Ensure original tasks.txt file exists and is in same folder.")
           continue  # Give user the chance to put tasks.txt in correct folder.

    elif menu == "vm":
        try:
            with open("tasks.txt", "r", encoding="utf-8") as f_2:
              specific_user_tasks = f_2.readlines()
              specific_task_content = 1
            for i in specific_user_tasks:
                specific_tasks = i.split(", ")
                if username == specific_tasks[0]:
                    print(specific_task_content, end=" ")
                    specific_task_content +=1  # Increment line by line only for logged in user.
                    print(f"\nAssigned to:      {specific_tasks[0]}")
                    print(f"Task:      {specific_tasks[1]}")
                    print(f"Task description:     {specific_tasks[2]}")
                    print(f"Date assigned:     {specific_tasks[3]}")
                    print(f"Due date:     {specific_tasks[4]}")
                    print(f"Task complete? {specific_tasks[5]}")
                    print("\n")
        except FileNotFoundError:
           print("\nEnsure original tasks.txt file exists and is in same folder.")
           continue  # Return to menu
           
    elif menu == "e":
        print("\nYou have successfully logged off.")
        exit()

    else:
        print("That's an invalid input!")
        
