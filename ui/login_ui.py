from functools import partial

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from custom import *
from main import MainScreen
from functions.projects import load_projects

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

        # if not validate_email(email):
        #  message_box('Error', 'Invalid email address.')

        if checkCredentials(email, password):
            app = App.get_running_app()
            app.set_accessLV(getAccessLV(email))
            app.set_accessName(getAccessName(email))
            update_last_login(email)
            message_box('Success', 'Welcome, ' + email)
            self.dismiss_popup()
            self.mainScreen.loggedIn(email)
        else:
            message_box('Error', 'Invalid credentials.')

    def dismiss_popup(self):
        self.popup.dismiss()


class AdminControls(GridLayout):
    def __init__(self, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.populate_users(load_users(0))

    def populate_users(self, users=load_users(0), headers=None):
        self.ids.account_list.clear_widgets()
        self.ids.account_headers.clear_widgets()
        if headers is None:
            headers = ['Email', 'Password', 'Access', 'Status']
        size_hints = [4, 3, 1, 2]
        for header in headers:
            self.ids.account_headers.add_widget(CButton(text=header,
                                                        bold=True,
                                                        padding=(10, 10),
                                                        size_hint_x=size_hints[headers.index(header)],
                                                        on_release=partial(self.sort_users, users,
                                                                           header)))
        for user in users:
             #If user access is 1, do not show access 0 users
            if user["access"] == 0 and App.get_running_app().get_accessLV() == 1:
                continue
            else:
                if user["email"] == App.get_running_app().get_accessName():
                    time = "Online"
                elif user["last_login"] == "None":
                    time = "Never"
                else:
                    time = TimeDiff(user["last_login"])

                grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
                grid.user = user
                button = Button(text=user["email"],
                                on_release=partial(self.view_user, user["id"]),
                                background_normal='', font_size='20sp',
                                background_color=(0.1, 0.1, 0.1, 0.0),
                                font_name='Roboto', size_hint_x=4,
                                color=(1, 1, 1, 1),
                                bold=True)
                grid.add_widget(button)
                grid.add_widget(CLabel(text='*' * len(user["password"]), size_hint_x=3))
                grid.add_widget(CLabel(text=str(user["access"]), size_hint_x=1))
                grid.add_widget(CLabel(text=time, size_hint_x=2))
                self.ids.account_list.add_widget(grid)

    def add_user(self, email, password, access):
        #Stringify
        email = str(email)
        password = str(password)
        access = int(access)

        if not validate_string(email, password, str(access)):
            message_box('Error', 'All fields are required.')
            return
        if not check_unique_email(email, "New"):
            message_box('Error', 'Email already exists.')
            return
        if access < 0 or access > 3:
            message_box('Error', 'Invalid access level.')
            return
        if access < App.get_running_app().get_accessLV():
            message_box('Error', 'You cannot add a user with higher access level than yours.')
            return
        if confirm_box('Add User', 'Are you sure you want to add this user?') == 'yes':
            add_user(email, password, access)
            message_box('Success', 'User added successfully.')
            self.populate_users(load_users(0))

    def edit_user(self, email, password, access):
        #Stringify
        email = str(email)
        password = str(password)
        access = str(access)
        print (email, password, access)

        if not validate_string(email, password, access):
            message_box('Error', 'All fields are required.')
            return
        # if access is 0 or 1
        if int(access) < 0 or int(access) > 3:
            message_box('Error', 'Invalid access level.')
            return
        if int(access) < App.get_running_app().get_accessLV():
            message_box('Error', 'You cannot add a user with higher access level than yours.')
            return
        if confirm_box('Edit User', 'Are you sure you want to edit this user?') == 'yes':
            if edit_user(email, password, access):
                message_box('Success', 'User edited successfully.')
                self.populate_users(load_users(0))
                if email == App.get_running_app().get_accessName():
                    App.get_running_app().set_accessLV(access)

    def sort_users (self, users, header, instance):
        if header == 'Email' or header == 'Email [D]':
            users = sorted(users, key=lambda x: x['email'])
            self.populate_users(users, ['Email [A]', 'Password', 'Access', 'Status'])
        elif header == 'Email [A]':
            users = sorted(users, key=lambda x: x['email'], reverse=True)
            self.populate_users(users, ['Email [D]', 'Password', 'Access', 'Status'])
        elif header == 'Access Level' or header == 'Access Level [D]':
            users = sorted(users, key=lambda x: x['access'])
            self.populate_users(users, ['Email', 'Password', 'Access [A]', 'Status'])
        elif header == 'Access Level [A]':
            users = sorted(users, key=lambda x: x['access'], reverse=True)
            self.populate_users(users, ['Email', 'Password', 'Access [D]', 'Status'])

    def view_user(self, user_id, instance):
        if user_id is not None:
            user = get_user(user_id)
            self.ids.edit_email.text = user['email']
            self.ids.edit_password.text = str(user['password'])
            self.ids.edit_access.text = str(user['access'])
            # if last login is None, it is none, otherwise Simplify the time
            if user['last_login'] == "None":
                self.ids.edit_status.text = "Never Logged In"
            else:
                self.ids.edit_status.text = SimplifyTime(user['last_login'])

    def btn_click(self, instance):
        txt = instance.text
        if txt == 'LogOut':
            self.main_screen.openLogPopup(txt)

    def dismiss_popup(self, instance):
        instance.dismiss()
