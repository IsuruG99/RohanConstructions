from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from custom import *
from main import MainScreen

from functions.login import *
from utils import *

# Main Login Screen


class LogInPopUp(GridLayout):
    def __init__(self, mainScreen, **kwargs):
        super().__init__(**kwargs)
        self.mainScreen = mainScreen

    def login(self, email, password):
        email = str(email)
        password = str(password)
        # Validate inputs
        if not validate_string(email, password):
            message_box('Error', 'All fields are required.')
            return
            # Check if the user is valid
        if checkCredentials(email, password):
            app = App.get_running_app()
            app.set_accessLV(getAccessLV(email))
            app.set_accessName(getAccessName(email))
            message_box('Success', 'Welcome, ' + email)
            self.dismiss_popup()
            self.mainScreen.loggedIn(email)
        else:
            message_box('Error', 'Invalid credentials.')

    def dismiss_popup(self):
        self.popup.dismiss()
