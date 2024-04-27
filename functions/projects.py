from kivy.app import App

from utils import *
from functions.finances import add_log
from functions.resources import load_resources


# Add a new project
def add_project(name: str, description: str, start_date: str, end_date: str, client_name: str, budget: str,
                status: str) -> bool:
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
        return True

    else:
        message_box('Error', 'Failed to add project: "projects" reference not found.')
        return False


# Get all projects
def load_projects(status: int = 2) -> list:
    # Get a reference to DB
    ref = database.get_ref('projects')

    # Retrieve all projects as a list of dictionaries
    projects = []
    for project_id, project in ref.get().items():
        if project_id == 'pjZero':
            continue
        project['id'] = project_id
        projects.append(project)

    # Status 1 = In Progress, 2 = Completed, 0 = All
    if status == 0:
        projects = [project for project in projects if project['status'] == 'In Progress']
    elif status == 1:
        projects = [project for project in projects if project['status'] == 'Completed']
    elif status == 2:
        projects = projects

    return projects


# Get a single project by ID
def get_project(proj_id: str) -> dict:
    # Get a reference to DB
    ref = database.get_ref('projects')

    # Retrieve the project data as a dictionary
    project = ref.child(proj_id).get()

    return project


# Take a dictionary with relevant unique key and update the project
def update_project(project_id: str, name: str, description: str, start_date: str, end_date: str, client_name: str,
                   budget: str, status: str):
    # Get a reference to DB
    ref = database.get_ref('projects')

    if status == 'Completed':
        # Ask to add a note to finances
        if confirm_box('Project Completed', 'Would you like to add a note to the finances?') == 'yes':
            # Add a log to finances (fin_type, amount, date, desc, entity, project, category)
            add_log('Income', budget, end_date, 'Project Completion', client_name, name, 'Contract',
                    App.get_running_app().get_accessName())

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
        return True

    else:
        message_box('Error', 'Failed to update project: "projects" reference not found.')
        return False


# Delete a project by ID
def delete_project(project_id: str) -> bool:
    # Get a reference to DB
    ref = database.get_ref('projects')

    if ref is not None:
        # Delete the project
        ref.child(project_id).delete()
    else:
        message_box('Error', 'Failed to delete project: "projects" reference not found.')

    print("Project deleted successfully.")
    return True


# Check if the project name is unique with an exception to the current project id
def name_unique_check(status: str, name: str, proj_id: str = None) -> bool:
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
def load_manpower() -> list:
    # Get a reference to DB
    ref = database.get_ref('manpower')

    # Retrieve all manpower as a list of dictionaries
    manpower_list = []
    for manpower_id, manpower in ref.get().items():
        if manpower_id == 'empZero':
            continue
        manpower['id'] = manpower_id
        manpower_list.append(manpower)

    return manpower_list


# Output Roles - Count style List from manpower
def load_members(project_name: str) -> dict:
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


# Output Resource - Count style list from Resources
def load_res(project_name: str) -> dict:
    resources = load_resources(0)
    resource_list = {}
    for resource in resources:
        for assignment in resource['resource_assignments']:
            if project_name in assignment['project']:
                if resource['name'] in resource_list:
                    resource_list[resource['name']] += int(assignment['amount'])
                else:
                    resource_list[resource['name']] = int(assignment['amount'])

    return resource_list


# For other functions, export a list of project names
def load_project_names() -> list:
    projects = load_projects(2)
    project_names = []
    for project in projects:
        project_names.append(project['name'])
    return project_names


# For other functions, export a list of project names matching client
def load_project_list(self, client_name: str) -> list:
    if client_name is not None:
        projectList = []
        projects = load_projects(2)
        for project in projects:
            if project['client_name'] == client_name:
                projectList.append(project['name'])
        return projectList
