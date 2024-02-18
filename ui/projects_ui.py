from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import add_project

from utils import *


# Add Project Popup Window
class AddPopup(GridLayout):
    def addProj(self, name, description, start_date, end_date, client_name, budget):
        name = str(name)
        description = str(description)
        start_date = str(start_date)
        end_date = str(end_date)
        client_name = str(client_name)
        budget = str(budget)
        # Validate inputs
        if not validate_string(name, description, start_date, end_date, client_name, budget):
            messagebox('Error', 'All fields are required.')
            return
        # Send data to projects.py
        add_project(name, description, start_date, end_date, client_name, budget, "In Progress")

    def dismiss_popup(self, instance):
        instance.dismiss()


# Projects Main UI (Accessed by main.py)
class ProjectsScreen(Screen):
    def btn_click(self, instance):
        if instance.text == 'Add Project':
            self.add_popup()
        elif instance.text == 'Edit Project':
            messagebox('Error', 'Edit project screen not implemented yet.')
        elif instance.text == 'Delete Project':
            messagebox('Error', 'Delete project screen not implemented yet.')
        elif instance.text == 'View Projects':
            messagebox('Error', 'View project screen not implemented yet.')
        elif instance.text == 'Back':
            self.parent.current = 'main'

    def add_popup(self):
        addPop = Popup(title='Add Project', content=AddPopup(), size_hint=(0.8, 0.7))
        addPop.open()
        addPop.content.popup = addPop




