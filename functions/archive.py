from utils import *
from kivy.app import App
from functions.projects import load_projects, delete_project, load_res_list, load_members_list
from functions.resources import load_resources, calc_resourcesCost
from functions.manpower import load_manpower, calc_manpowerCost

# Load all archive data from Database
def load_all_archives(status: int = 0) -> list:
    ref = database.get_ref('archive')
    if ref is not None:
        archives = []
        for archive_id, archive in ref.get().items():
            if archive_id == 'arZero':
                continue
            archive['id'] = archive_id
            archives.append(archive)
        if status == 0:
            archives = archives
        return archives
    else:
        return []


# Get a single archive by ID
def get_archive(archive_id: str) -> dict:
    ref = database.get_ref('archive')
    if ref is not None:
        return ref.child(archive_id).get()
    return {}


# Convert a completed project into an Archive Object
def convert_project(project: str) -> bool:
    # {
    #   "archive": {
    #     "arZero": {
    #       "budget": "None",
    #       "client_name": "None",
    #       "description": "None",
    #       "end_date": "None",
    #       "manpowerCost": "None",
    #       "name": "None",
    #       "netProfit": "None",
    #       "resourceCost": "None",
    #       "start_date": "None",
    #       "user": "None"
    #     },
    #     "archive1": {
    #       "budget": "10000",
    #       "client_name": "ABC Company",
    #       "description": "Project Black is a test  project",
    #       "employee_allocations": [
    #         {
    #           "count": "3",
    #           "role": "Master Mason"
    #         },
    #         {
    #           "count": "1",
    #           "role": "Project Manager"
    #         }
    #       ],
    #       "end_date": "2022-05-11",
    #       "manpowerCost": "250500",
    #       "name": "Project Black",
    #       "netProfit": "569500",
    #       "resourceCost": "180000",
    #       "resource_allocations": [
    #         {
    #           "amount": "10",
    #           "resource": "ABC Equipment"
    #         },
    #         {
    #           "amount": "50",
    #           "resource": "Concrete"
    #         }
    #       ],
    #       "start_date": "2010-2-11",
    #       "user": "a"
    #     },

    # find if project exists in projects, the project variable is actually the project's 'name'
    projects = load_projects(3)
    for proj in projects:
        if proj['name'] == project:
            project_data = proj
            break
    else:
        return False

    manpower_alloc = load_members_list(project) if len(load_members_list(project)) > 0 else [{"count": "", "role": ""}]
    resources_alloc = load_res_list(project) if len(load_res_list(project)) > 0 else [{"amount": "", "resource": ""}]
    manpower_cost = calc_manpowerCost(project)
    resource_cost = calc_resourcesCost(project)

    # Input data related to project according to above json structure into archives
    ref = database.get_ref('archive')
    if ref is None:
        return False
    archive_project = ref.push()
    archive_project.set({
        'name': project_data['name'],
        'description': project_data['description'],
        'client_name': project_data['client_name'],
        'start_date': project_data['start_date'],
        'end_date': project_data['end_date'],
        'budget': project_data['budget'],
        'employee_allocations': manpower_alloc,
        'resource_allocations': resources_alloc,
        'manpowerCost': str(manpower_cost),
        'resourceCost': str(resource_cost),
        'netProfit': str(int(project_data['budget']) - manpower_cost - resource_cost),
        'user': App.get_running_app().get_accessName()
    })
    print(manpower_alloc)

    # Delete the project from projects
    if delete_project(project_data['id']):
        return True
    return False











