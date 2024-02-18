from kivy.app import App
from kivy.uix.screenmanager import Screen
from functions.projects import add_project

from utils import *


def add(name, description, start_date, end_date, client_id, budget, status):
    # Validating Inputs
    if not validate_string(name, description, start_date, end_date, client_id, budget, status):
        messagebox('Error', 'All fields are required.')
        return
    add_project(name, description, start_date, end_date, client_id, budget, status)


class ProjectsScreen(Screen):
    def btn_click(self, instance):
        if instance.text == 'Add':
            messagebox('Error', 'Add project screen not implemented yet.')
        elif instance.text == 'Edit':
            messagebox('Error', 'Edit project screen not implemented yet.')
        elif instance.text == 'Delete':
            messagebox('Error', 'Delete project screen not implemented yet.')
        elif instance.text == 'View':
            messagebox('Error', 'View project screen not implemented yet.')
        elif instance.text == 'Search':
            messagebox('Error', 'Search project screen not implemented yet.')
        elif instance.text == 'Back':
            self.parent.current = 'main'
    pass