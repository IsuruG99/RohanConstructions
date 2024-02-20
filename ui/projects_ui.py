from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import add_project, load_projects

from utils import *


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
            messagebox('Error', 'All fields are required.')
            return
        if not validate_date(start_date, end_date):
            messagebox('Error', 'Invalid date format.')
            return
        # Send data to projects.py
        add_project(name, description, start_date, end_date, client_name, budget, "In Progress")
        self.projects_screen.populate_projects()
        self.dismiss_popup(self.popup)

    def dismiss_popup(self, instance):
        instance.dismiss()


# Projects Main UI (Accessed by main.py)
class ProjectsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_projects()

    def populate_projects(self):
        # Get the projects from the database
        projects = load_projects()

        # Clear the existing widgets in the ScrollView
        self.ids.projects_list.clear_widgets()

        for project in projects:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
            button = Button(text=project["name"], on_release=self.view_project, background_normal='',
                            background_color=(1, 1, 1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
            grid.project = project
            grid.add_widget(button)
            grid.add_widget(Label(text=project["client_name"]))
            grid.add_widget(Label(text=project["end_date"]))
            grid.add_widget(Label(text=project["status"]))
            self.ids.projects_list.add_widget(grid)

    def view_project(self, instance):
        # Get the project data from the instance
        project = instance.parent.project

        # Display the project data in a message box
        messagebox('Project Details',
                   f'Name: {project["name"]}\nClient: {project["client_name"]}\nDeadline: {project["end_date"]}'
                   f'\nStatus: {project["status"]}')

    def btn_click(self, instance):
        if instance.text == 'Add':
            self.add_popup()
        elif instance.text == 'Edit':
            messagebox('Error', 'Edit project screen not implemented yet.')
        elif instance.text == 'Delete':
            messagebox('Error', 'Delete project screen not implemented yet.')
        elif instance.text == 'Back':
            self.parent.current = 'main'

    def add_popup(self):
        addPop = Popup(title='Add Project', content=AddPopup(self), size_hint=(0.8, 0.7))
        addPop.open()
        addPop.content.popup = addPop




