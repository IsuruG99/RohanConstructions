from kivy.app import App
from functions.projects import add_project

from utils import *


def add(name, description, start_date, end_date, client_id, budget, status):
    # Validating Inputs
    if not validate_string(name, description, start_date, end_date, client_id, budget, status):
        messagebox('Error', 'All fields are required.')
        return
    add_project(name, description, start_date, end_date, client_id, budget, status)
