from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from functions.login import *
from utils import *

# Main Login Screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self, email, password):
        email = str(email)
        password = str(password)
        # Validate inputs
        if not validate_string(email, password):
            message_box('Error', 'All fields are required.')
            return
        # Check if the user is valid
        if checkCredentials(email, password):
            self.manager.current = 'main'
        else:
            message_box('Error', 'Invalid credentials.')
            return


