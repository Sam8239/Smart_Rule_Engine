
# TCS Smart Rules Engine

It is a Smart Rule Engine which takes data in a hierarchical way to define rules on differnt characteristics and executes them on the given input by the user to extract required information based on defined rules
## Features

- Login (Authentication to enter this application)
- Master (Adding appropriate data)
    - Role Master (Create Users)
    - Parameter Definition (Define Parameters)
    - Character Definition (Define Characteristics)
    - Assign Character Definition (Define Assigned Character)
    - Configuration Setup
- Character Mapping (Mapping of data in particular Hierarchy)
- Rules Definition (Define Rules For Each Characteristics)
- Rules Execution (Execute Defined Rules)
- Logout (Logout from the application)

  
## Deployment

- Download and install postgreSQL
- Create Database 
- Import demo data **sre_data.tar** on pdAdmin:
    - Open **pgAdmin**
    - Right click on the new database just created
    - Click on **Restore** option
    - In the **Filename** field select the **sre_data.tar** and click **Restore**
- Open Django File and go to terminal
- Run this command to install all the required libraries
```bash
  pip install -r requirements.txt
```
- Run these commands to migrate and run locally
 ```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```
- Default Admin Details
    - User Id: admin
    - User Password: admin
Note :- After login with default details please create a new user

### Create User  
- Go to Role Master page and create new users

### Define Parameters  
- Go to Parameter Definition page and define required parameters to be dynamically added in the form on Character Mapping page while definig Characteristics

### Define Characteristics
- Go to Character Definition page and define Characteristics in a particular hierarchy

### Define Assigned Character
- Go to Assigned Character page and define Assigned Characteristics

### Mapping of data in a particular Hierarchy
- Go to Character Mapping page and map Assigned Characteristics to a particular hierarchy created in Character Definition page

### Define Rules For Each Characteristics
- Go to Rules Definition page, select the hierarchy and proceed
- Then define rules for each assigned characteristics

### Execute Defined Rules
- Go to Rules Execution page
- Select the appropriate hierarchy
- Input text for rule execution and proceed to get the respective results