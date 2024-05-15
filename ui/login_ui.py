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
    def __init__(self, mainScreen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.mainScreen = mainScreen
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def login(self, email: str, password: str) -> None:
        email, password = str(email), str(password)
        if not validate_string(email, password):
            self.mainScreen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        if not checkCredentials(email, password):
            self.mainScreen.CMessageBox('Error', 'Invalid email or password.', 'Message')
            return

        app = App.get_running_app()
        app.set_accessLV(getAccessLV(email))
        app.set_accessName(getAccessName(email))
        update_last_login(email)
        self.mainScreen.CMessageBox('Success', f'Welcome {email}', 'Message')
        self.popup.dismiss()
        self.mainScreen.loggedIn(email)

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


# Add User Popup
class AddUserPopup(GridLayout):
    def __init__(self, main_screen: Screen, adminControls: GridLayout, popup, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.adminControls = adminControls
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def add_user(self, requestType: str = "Submit") -> None:
        try:
            email = str(self.ids.add_user_email.text)
            password = str(self.ids.add_user_password.text)
            access = int(self.ids.add_user_access.text)
        except ValueError:
            self.main_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        if not validate_string(email, password, str(access)) or not (
                0 <= access <= 3) or access >= App.get_running_app().get_accessLV():
            self.main_screen.CMessageBox('Error', 'Invalid input.', 'Message')
            return

        if not validate_email(email):
            self.main_screen.CMessageBox('Error', 'Invalid email.', 'Message')
            return

        if requestType == "Validate":
            if check_unique_email(email, "New"):
                self.main_screen.CMessageBox('Confirm', 'Are you sure you want to add this user?', 'Confirm', 'Yes',
                                             'No', self.add_user)
            else:
                self.main_screen.CMessageBox('Error', 'Email already exists.', 'Message')
        elif requestType == "Submit" and add_user(email, password, access):
            self.main_screen.CMessageBox('Success', 'User added successfully.', 'Message')
            self.adminControls.populate_users(load_users(0))
        else:
            self.main_screen.CMessageBox('Error', 'User could not be added.', 'Message')

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


class EditUserPopup(GridLayout):
    def __init__(self, main_screen: Screen, adminControls: GridLayout, popup, user_id, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.adminControls = adminControls
        self.popup = popup
        self.cols = 1
        self.rows = 1
        self.user_id = user_id
        self.populate_view()

    def populate_view(self):
        user = get_user(self.user_id)
        self.ids.edit_user_email.text = user['email']
        self.ids.edit_user_password.text = str(user['password'])
        self.ids.edit_user_access.text = str(user['access'])
        if user['last_login'] == "None":
            self.ids.edit_user_last_login.text = "Never Logged In"
        else:
            self.ids.edit_user_last_login.text = SimplifyTime(user['last_login'])

    def edit_user(self, requestType: str = "Submit") -> None:
        try:
            email = str(self.ids.edit_user_email.text)
            password = str(self.ids.edit_user_password.text)
            access = int(self.ids.edit_user_access.text)
        except (AttributeError, ValueError):
            self.main_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        if not validate_string(email, password, str(access)) or access not in range(4):
            self.main_screen.CMessageBox('Error', 'Invalid input.', 'Message')
            return

        if not validate_email(email):
            self.main_screen.CMessageBox('Error', 'Invalid email.', 'Message')
            return

        if access < App.get_running_app().get_accessLV():
            self.main_screen.CMessageBox('Error', 'You cannot edit a user with higher access level than yours.',
                                         'Message')
            return

        if requestType == "Validate":
            self.main_screen.CMessageBox('Update User', 'Are you sure you want to update this user?', 'Confirm', 'Yes', 'No',
                                         self.edit_user)
        elif requestType == "Submit" and edit_user(email, password, access):
            self.main_screen.CMessageBox('Success', 'User edited successfully.', 'Message')
            if email == App.get_running_app().get_accessName():
                App.get_running_app().set_accessLV(access)
            self.adminControls.populate_users(load_users(0))

    def delete_user(self, requestType: str = "Submit") -> None:
        email = str(self.ids.edit_user_email.text)
        if email:
            if App.get_running_app().get_accessLV() <= getAccessLV(email):
                if requestType == "Validate":
                    self.main_screen.CMessageBox('Delete User', 'Are you sure you want to delete this user?', 'Confirm',
                                                 'Yes', 'No', self.delete_user)
                elif requestType == "Submit":
                    delete_user(email)
                    self.main_screen.CMessageBox('Success', 'User deleted successfully.', 'Message')
                    self.adminControls.populate_users(load_users(0))
                else:
                    self.main_screen.CMessageBox('Error',
                                                 'You cannot delete a user with higher access level than yours.',
                                                 'Message')
            else:
                self.main_screen.CMessageBox('Error', 'Invalid user.', 'Message')

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


# Admin Panel
class AdminControls(GridLayout):
    def __init__(self, main_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.popup = popup
        self.populate_users(load_users(0))
        self.cols = 1
        self.rows = 1

    def populate_users(self, users: list = load_users(0), headers: list = None) -> None:
        self.ids.current_user.text = f'Current User: {App.get_running_app().get_accessName()}'
        self.ids.account_list.clear_widgets()
        self.ids.account_headers.clear_widgets()

        headers = headers or ['Email', 'Password', 'Access', 'Status']
        size_hints = [4, 3, 1, 2]

        for header in headers:
            self.ids.account_headers.add_widget(CButton(text=header,
                                                        bold=True,
                                                        padding=(10, 10),
                                                        size_hint_x=size_hints[headers.index(header)],
                                                        on_release=partial(self.sort_users, users, header)))

        for user in users:
            if user["access"] == 0 and App.get_running_app().get_accessLV() == 1:
                continue

            time = "Online" if user["email"] == App.get_running_app().get_accessName() else "Never" if user[
                                                                                                           "last_login"] == "None" else TimeDiff(
                user["last_login"])

            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            grid.user = user
            button = Button(text=user["email"],
                            on_release=partial(self.edit_user_popup, user["id"]),
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

    def sort_users(self, users: list, header: str, instance) -> None:
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

    def add_user_popup(self) -> None:
        temp_addPop_popup = Popup()
        addPop_popup = AddUserPopup(self.main_screen, self, temp_addPop_popup)
        addPop = RPopup(title='Create User Account', content=addPop_popup, size_hint=(0.45, 0.55))
        addPop_popup.popup = addPop
        addPop.open()

    def edit_user_popup(self, user_id: str, instance) -> None:
        temp_editPop_popup = Popup()
        editPop_popup = EditUserPopup(self.main_screen, self, temp_editPop_popup, user_id)
        editPop = RPopup(title='Edit User Account', content=editPop_popup, size_hint=(0.45, 0.65))
        editPop_popup.popup = editPop
        editPop.open()

    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == 'Log Out':
            self.main_screen.openLogPopup('LogOut')
            self.popup.dismiss()

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()
