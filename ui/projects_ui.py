from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import *
from functools import partial
import datetime

from utils import *
from custom import *


# Add Project Popup Window
class AddPopup(GridLayout):
    def __init__(self, projects_screen, **kwargs):
        super().__init__(**kwargs)
        self.projects_screen = projects_screen

    def addProj(self, name, description, start_date, end_date, client_name, budget):
        name = str(name)
        description = str(description)
        start_date = str(start_date)
        end_date = str(end_date)
        client_name = str(client_name)
        budget = str(budget)
        # Validate inputs
        if not validate_string(name, description, client_name, budget):
            message_box('Error', 'All fields are required.')
            return
        if not validate_date(start_date, end_date):
            message_box('Error', 'Invalid date format.')
            return
        if name_unique_check('add', name) is False:
            message_box('Error', 'Project name must be unique.')
            return
        # Send data to projects.py
        add_project(name, description, start_date, end_date, client_name, budget, "In Progress")
        message_box('Success', 'Project added successfully.')
        self.projects_screen.populate_projects()
        self.projects_screen.ids.projects_filter.text = 'In Progress'
        self.projects_screen.dismiss_popup(self.popup)


# View Project Popup Window
class ViewPopup(GridLayout):
    def __init__(self, projects_screen, project_id, **kwargs):
        super().__init__(**kwargs)
        self.project_id = project_id
        self.populate_view()
        self.projects_screen = projects_screen

    # Populate PopUp Window
    def populate_view(self):
        # Get the project data from the DB
        project = get_project(self.project_id)
        # Assign
        self.ids.viewPop_name.text = project["name"]
        self.ids.viewPop_desc.text = project["description"]
        self.ids.viewPop_startDate.text = project["start_date"]
        self.ids.viewPop_endDate.text = project["end_date"]
        self.ids.viewPop_client.text = project["client_name"]
        self.ids.viewPop_budget.text = str(project["budget"])
        self.ids.viewPop_status.text = project["status"]

    # Edit Project
    def editProj(self, name, description, start_date, end_date, client_name, budget, status):
        # Stringify inputs (Including Dates)
        name = str(name)
        description = str(description)
        start_date = str(start_date)
        end_date = str(end_date)
        client_name = str(client_name)
        budget = str(budget)
        status = str(status)

        # Validate inputs
        if not validate_string(name, description, client_name, budget, status):
            message_box('Error', 'All fields are required.')
            return
        if not validate_date(start_date, end_date):
            message_box('Error', 'Invalid date format.')
            return
        if name_unique_check('update', name, self.project_id) is False:
            message_box('Error', 'Project name must be unique.')
            return
        # Send data to projects.py
        if confirm_box('Update Project', 'Are you sure you want to update this project?') == 'yes':
            if update_project(self.project_id, name, description, start_date, end_date, client_name, budget, status):
                message_box('Success', 'Project updated successfully.')
                self.projects_screen.populate_projects()
                self.projects_screen.ids.projects_filter.text = 'In Progress'
                self.projects_screen.dismiss_popup(self.popup)
            else:
                message_box('Failed', 'Failed to update project.')

    # Open Reports Popup Window
    def reports_popup(self):
        self.projects_screen.dismiss_popup(self.popup)
        reportsPop = Popup(title='Project Reports', content=ReportsPopup(self, self.project_id), size_hint=(0.6, 0.95))
        reportsPop.open()
        reportsPop.content.popup = reportsPop

    # Delete Project
    def deleteProj(self):
        # Send project_id to projects.py
        if confirm_box('Delete Project', 'Are you sure you want to delete this project?') == 'yes':
            if delete_project(self.project_id):
                message_box('Success', 'Project deleted successfully.')
            else:
                message_box('Error', 'Failed to delete project.')
            self.projects_screen.populate_projects()
            self.projects_screen.ids.projects_filter.text = 'In Progress'
            self.projects_screen.dismiss_popup(self.popup)

    def dismiss_popup(self, instance):
        self.projects_screen.dismiss_popup(self.popup)


class ReportsPopup(GridLayout):
    def __init__(self, projects_screen, proj_id, **kwargs):
        super().__init__(**kwargs)
        self.projects_screen = projects_screen
        self.populate_reports(proj_id)

    # We have the Proj_ID, populate the fields
    def populate_reports(self, pid):
        # Get the project data from the DB
        project = get_project(pid)

        # Assign
        self.ids.proj_id.text = pid
        self.ids.proj_name.text = project["name"]
        self.ids.proj_desc.text = project["description"]
        self.ids.proj_start.text = project["start_date"]
        self.ids.proj_end.text = project["end_date"]
        self.ids.proj_client.text = project["client_name"]
        self.ids.proj_budget.text = str(project["budget"])
        # Get relevant manpower data (manpower role, count)
        roles = load_members(project["name"])
        for role, count in roles.items():
            grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)
            grid.add_widget(CLabel(text=role, label_font_size='15sp'))
            grid.add_widget(CLabel(text=str(count), label_font_size='15sp'))
            self.ids.assigned_manpower.add_widget(grid)

    def dismiss_popup(self, instance):
        self.projects_screen.dismiss_popup(self.popup)


# Projects Main UI (Accessed by main.py)
class ProjectsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_projects()

    # Populate the ScrollView with the projects
    def populate_projects(self, projects=load_projects(), headers=None):
        # Clear the ScrollView
        self.ids.projects_list.clear_widgets()

        # Create Headers
        if headers is None:
            headers = ['Project Name', 'Client', 'End Date', 'Status']
        grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
        for header in headers:
            grid.add_widget(CButton(text=header, bold=True, padding=(10, 10),
                                    on_release=partial(self.sort_projects, header, projects)))
        self.ids.projects_list.add_widget(grid)

        # Fill the Grid with Project Data
        for project in projects:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
            button = Button(text=project["name"], on_release=partial(self.view_project, project["id"]),
                            background_normal='', font_size='20sp',
                            background_color=(0.1, 0.1, 0.1, 0.0), font_name='Roboto', color=(1, 1, 1, 1),
                            bold=True)
            grid.project = project
            grid.add_widget(button)
            grid.add_widget(CLabel(text=project["client_name"]))
            grid.add_widget(CLabel(text=project["end_date"]))
            grid.add_widget(CLabel(text=project["status"]))
            self.ids.projects_list.add_widget(grid)

    def sort_projects(self, header, projects, instance):
        # Sort by header
        if header == 'Project Name' or header == 'Project Name [D]':
            projects = sorted(projects, key=lambda x: x['name'])
            self.populate_projects(projects, headers=['Project Name [A]', 'Client', 'End Date', 'Status'])
        elif header == 'Client' or header == 'Client [D]':
            projects = sorted(projects, key=lambda x: x['client_name'])
            self.populate_projects(projects, headers=['Project Name', 'Client [A]', 'End Date', 'Status'])
        elif header == 'End Date' or header == 'End Date [D]':
            projects = sorted(projects, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'))
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date [A]', 'Status'])
        elif header == 'Status' or header == 'Status [D]':
            projects = sorted(projects, key=lambda x: x['status'])
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date', 'Status [A]'])
        elif header == 'Project Name [A]':
            projects = sorted(projects, key=lambda x: x['name'], reverse=True)
            self.populate_projects(projects, headers=['Project Name [D]', 'Client', 'End Date', 'Status'])
        elif header == 'Client [A]':
            projects = sorted(projects, key=lambda x: x['client_name'], reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client [D]', 'End Date', 'Status'])
        elif header == 'End Date [A]':
            projects = sorted(projects, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'),
                              reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date [D]', 'Status'])
        elif header == 'Status [A]':
            projects = sorted(projects, key=lambda x: x['status'], reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date', 'Status [D]'])


    # Open View Popup Window
    def view_project(self, project_id, instance):
        # The project_id is passed to the ViewPopup Window
        viewPop = CPopup(title='View Project', content=ViewPopup(self, project_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Open Add Popup Window
    def add_popup(self):
        addPop = CPopup(title='Add Project', content=AddPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    # Button Click Event Handler
    def btn_click(self, instance):
        txt = instance.text
        if txt == 'Add':
            self.add_popup()
        elif txt == 'All' or txt == 'In Progress' or txt == 'Completed':
            if txt == 'In Progress':
                self.populate_projects(load_projects(1))
                self.ids.projects_filter.text = 'Completed'
            elif txt == 'Completed':
                self.populate_projects(load_projects(2))
                self.ids.projects_filter.text = 'All'
            elif txt == 'All':
                self.populate_projects()
                self.ids.projects_filter.text = 'In Progress'
        elif txt == 'Back':
            self.parent.current = 'main'

    # Font Size Adjustment Test
    def fontSizer(self, instance):
        for grid in self.ids.projects_list.children:
            for child in grid.children:
                if isinstance(child, (Label, Button)):
                    if instance.text == '+':
                        child.font_size += 5
                    else:
                        child.font_size -= 5
                    child.size_hint_y = None
                    child.texture_update()
                    child.size = child.texture_size

    def dismiss_popup(self, instance):
        instance.dismiss()
