from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import *
from functools import partial

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
        self.projects_screen.populate_projects(0)
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
        update_project(self.project_id, name, description, start_date, end_date, client_name, budget, status)
        message_box('Success', 'Project updated successfully.')
        self.projects_screen.populate_projects(0)
        self.projects_screen.ids.projects_filter.text = 'In Progress'
        self.projects_screen.dismiss_popup(self.popup)


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
            self.projects_screen.populate_projects(0)
            self.projects_screen.ids.projects_filter.text = 'In Progress'
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
            grid.add_widget(Label(text=role))
            grid.add_widget(Label(text=str(count)))
            self.ids.assigned_manpower.add_widget(grid)

    def dismiss_popup(self, instance):
        self.projects_screen.dismiss_popup(self.popup)


# Projects Main UI (Accessed by main.py)
class ProjectsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_projects(0)
        self.switch = 0

    # Populate the ScrollView with the projects
    def populate_projects(self, status):
        # Get the projects from the database
        projects = load_projects()

        # Clear the existing widgets in the ScrollView
        self.ids.projects_list.clear_widgets()
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
            if status == 0 and project["status"] == "In Progress":
                self.ids.projects_list.add_widget(grid)
            elif status == 1 and project["status"] == "Completed":
                self.ids.projects_list.add_widget(grid)
            elif status == 2:
                self.ids.projects_list.add_widget(grid)

            # Open View Popup Window with the project_id

    def view_project(self, project_id, instance):
        # ViewPopup class will be called to display the project details in a popup window
        # The project_id is passed to the ViewPopup class
        viewPop = Popup(title='View Project', content=ViewPopup(self, project_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Open Add Popup Window
    def add_popup(self):
        addPop = Popup(title='Add Project', content=AddPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    # Button Click Event Handler
    def btn_click(self, instance):
        if instance.text == 'Add':
            self.add_popup()
        elif instance.text == 'All' or instance.text == 'In Progress' or instance.text == 'Completed':
            if instance.text == 'In Progress':
                self.populate_projects(1)
                self.ids.projects_filter.text = 'Completed'
            elif instance.text == 'Completed':
                self.populate_projects(2)
                self.ids.projects_filter.text = 'All'
            elif instance.text == 'All':
                self.populate_projects(0)
                self.ids.projects_filter.text = 'In Progress'
        elif instance.text == 'Back':
            self.parent.current = 'main'

    def dismiss_popup(self, instance):
        instance.dismiss()
