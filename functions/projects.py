import database
from utils import message_box


# Add a new project
def add_project(name, description, start_date, end_date, client_name, budget, status):
    # Get a reference to DB
    ref = database.get_ref('projects')

    if ref is not None:
        # Generate a new unique key for the project
        new_project_ref = ref.push()

        # Set the project data under the new key
        new_project_ref.set({
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'client_name': client_name,
            'budget': budget,
            'status': status
        })

    else:
        message_box('Error', 'Failed to add project: "projects" reference not found.')


# Get all projects
def load_projects():
    # Get a reference to DB
    ref = database.get_ref('projects')

    # Retrieve all projects as a list of dictionaries
    projects = []
    for project_id, project in ref.get().items():
        project['id'] = project_id
        projects.append(project)

    return projects


# Get a single project by ID
def get_project(proj_id):
    # Get a reference to DB
    ref = database.get_ref('projects')

    # Retrieve the project data as a dictionary
    project = ref.child(proj_id).get()

    return project


# Take a dictionary with relevant unique key and update the project
def update_project(project_id, name, description, start_date, end_date, client_name, budget, status):
    # Get a reference to DB
    ref = database.get_ref('projects')

    if ref is not None:
        # Set the project data under the new key
        ref.child(project_id).update({
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'client_name': client_name,
            'budget': budget,
            'status': status
        })

    else:
        message_box('Error', 'Failed to update project: "projects" reference not found.')

    print("Project updated successfully.")
    return True


# Delete a project by ID
def delete_project(project_id):
    # Get a reference to DB
    ref = database.get_ref('projects')

    if ref is not None:
        # Delete the project
        ref.child(project_id).delete()
    else:
        message_box('Error', 'Failed to delete project: "projects" reference not found.')

    print("Project deleted successfully.")
    return True


# very specific function here
# Check if the project name is unique with an exception to the current project id
def name_unique_check(status, name, proj_id=None):
    # load all projects
    projects = load_projects()

    if status == 'add':
        for project in projects:
            if project['name'] == name:
                return False
    if status == 'update':
        for project in projects:
            if project['id'] != proj_id and project['name'] == name:
                return False
    return True


# The manpower function should contain this, but as it is not made yet i wil use this temporally
def load_manpower():
    # Get a reference to DB
    ref = database.get_ref('manpower')

    # Retrieve all manpower as a list of dictionaries
    manpower_list = []
    for manpower_id, manpower in ref.get().items():
        manpower['id'] = manpower_id
        manpower_list.append(manpower)

    return manpower_list

# now we use the manpower dictionary to get the roles and count for a specific project
# in manpower, every employee would have their assigned project name in 'project_assignments' array
# we would loop through the manpower and check if the project name matches the project we are looking for
def load_members(project_name):
    # Get a reference to DB
    manpower = load_manpower()
    roles = {}
    for employee in manpower:
        if project_name in employee['project_assignments']:
            if employee['role'] in roles:
                roles[employee['role']] += 1
            else:
                roles[employee['role']] = 1
    return roles


