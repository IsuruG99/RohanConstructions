from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from functools import partial
from functions.manpower import *
from functions.projects import load_project_names
import datetime
from utils import *
from custom import *
from validation import *


# Manages user access to most functions. (Implemented by project leader)
def AccessControl(func):
    def wrapper(self, *args, **kwargs):
        # function validate_access in validation.py takes function's name (string) and returns True/False
        from kivy.app import App
        if App.get_running_app().get_accessLV() is not None:
            accessLV = App.get_running_app().get_accessLV()
            blockList = []
            # Lv3 users cant add/edit/delete, everyone can view.
            if accessLV == 3:
                blockList = ['add_emp', 'add_employee', 'edit_employee', 'delete_employee', 'reload']
            if validate_access(accessLV, func.__name__, blockList):
                return func(self, *args, **kwargs)
            else:
                try:
                    self.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
                except AttributeError:
                    self.manpower_screen.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
    return wrapper


class AddManpower(GridLayout):
    def __init__(self, manpower_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.manpower_screen = manpower_screen
        self.popup = popup
        self.validCheck = 0
        self.cols = 1
        self.rows = 1

    @AccessControl
    def add_employee(self, requestType: str = "Submit") -> None:
        # Stringify
        try:
            name = str(self.ids.addEmp_name.text)
            email = str(self.ids.addEmp_email.text)
            phone_number = str(self.ids.addEmp_phone.text)
            role = str(self.ids.addEmp_role.text)
            status = str(self.ids.addEmp_status.text)
            contract_fee = str(self.ids.addEmp_contractFee.text)
            retainer_fee = str(self.ids.addEmp_retainerFee.text)
        except AttributeError or ValueError:
            self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        # Check if all fields are full, except assignments
        if requestType == "Validate":
            if name == '' or email == '' or phone_number == '' or role == '' or status == '' or contract_fee == '' or retainer_fee == '':
                self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_email(email):
                self.manpower_screen.CMessageBox('Error', 'Invalid email.', 'Message')
                return
            if not validate_mobileNo(phone_number):
                self.manpower_screen.CMessageBox('Error', 'Invalid phone number.', 'Message')
                return
            self.manpower_screen.CMessageBox('Add Employee', str(f'Are you sure you want to add employee {name}?'),
                                             'Confirm', 'Yes', 'No', self.add_employee)
            self.validCheck = 1
        if requestType == "Submit" and self.validCheck == 1:
            if add_employee(name, role, email, phone_number, status, [""], contract_fee, retainer_fee):
                self.manpower_screen.CMessageBox('Success', 'Employee added successfully.', 'Message')
                self.validCheck = 0
                self.manpower_screen.populate_manpower(load_manpower(0))
                self.popup.dismiss()
            else:
                self.manpower_screen.CMessageBox('Error', 'Failed to add Employee.', 'Message')
                self.validCheck = 0

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


class ViewManpower(GridLayout):
    def __init__(self, manpower_screen: Screen, emp_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.emp_id = emp_id
        self.manpower_screen = manpower_screen
        self.populateEmp()
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populateEmp(self) -> None:
        emp = get_employee(self.emp_id)

        self.ids.viewEmp_name.text = emp["name"]
        self.ids.viewEmp_role.text = emp["role"]
        self.ids.viewEmp_status.text = emp["employment_status"]
        self.ids.viewEmp_email.text = emp["email"]
        self.ids.viewEmp_phone.text = emp["phone_number"]
        self.ids.viewEmp_contractFee.text = emp["contract_fee"]
        self.ids.viewEmp_retainerFee.text = emp["retainer_fee"]

        # emp["project_assignments"] is a list of projects, we display them in ScrollView named viewEmp_projects
        for project in emp["project_assignments"]:
            # there is one blank project assignment, where project: "", skip it
            if not project == "":
                grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=project, size_hint_x=0.8))
                grid.add_widget(
                    Button(text='X', background_normal='', background_color=(0.1, 0.1, 0.1, 0), font_size='20sp',
                           bold=True,
                           font_name='Roboto', size_hint_x=0.2, on_release=partial(self.reload, project, "Remove")))
                self.ids.viewEmp_projects.add_widget(grid)

    @AccessControl
    def reload(self, project_name: Screen, action: str, instance) -> None:
        try:
            project_name = str(project_name)
            action = str(action)
        except ValueError or AttributeError:
            return
        project_assignment(self.emp_id, project_name, action)
        # Clear all widgets from viewEmp_projects
        self.ids.viewEmp_projects.clear_widgets()
        self.populateEmp()

    @AccessControl
    def edit_employee(self, requestType: str = "Submit") -> None:
        # Project assignments is a list of projects, not validating it
        # Stringify inputs
        try:
            name = str(self.ids.viewEmp_name.text)
            email = str(self.ids.viewEmp_email.text)
            phone_number = str(self.ids.viewEmp_phone.text)
            role = str(self.ids.viewEmp_role.text)
            status = str(self.ids.viewEmp_status.text)
            contract_fee = str(self.ids.viewEmp_contractFee.text)
            retainer_fee = str(self.ids.viewEmp_retainerFee.text)
        except AttributeError or ValueError:
            self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        # Validate & Confirm first, then call Submit
        if requestType == "Validate":
            # Check if all fields are full, except assignments
            if name == '' or email == '' or phone_number == '' or role == '' or status == '' or contract_fee == '' or retainer_fee == '':
                self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_email(email):
                self.manpower_screen.CMessageBox('Error', 'Invalid email.', 'Message')
                return
            if not validate_mobileNo(phone_number):
                self.manpower_screen.CMessageBox('Error', 'Invalid Mobile No.', 'Message')
                return
            self.manpower_screen.CMessageBox('Edit Employee', f'Are you sure you want to edit employee {name}?',
                                             'Confirm', 'Yes', 'No', self.edit_employee)
            self.validCheck = 1
        # Send to update_employee
        if requestType == "Submit":
            if self.validCheck == 1:
                if update_employee(self.emp_id, name, role, email, phone_number, status, contract_fee, retainer_fee):
                    self.manpower_screen.CMessageBox('Success', 'Employee edited successfully.', 'Message')
                    self.validCheck = 0
                    self.manpower_screen.populate_manpower(load_manpower(0))
                    self.popup.dismiss()
                else:
                    self.manpower_screen.CMessageBox('Error', 'Failed to edit Employee.', 'Message')
                    self.validCheck = 0

    def load_projects(self) -> list:
        return load_project_names()

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


class ManpowerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_manpower(load_manpower(0))
        self.dempID = None

    def populate_manpower(self, employees: list = load_manpower(0), headers: list = None) -> None:
        # Clear the existing widgets in the ScrollView
        self.ids.manpower_list.clear_widgets()
        self.ids.manpower_headers.clear_widgets()

        # headers
        if headers is None:
            headers = ['Name', 'Role', 'Email', '', '']
        size_hints = [0.3, 0.2, 0.3, 0.1, 0.1]
        for header in headers:
            self.ids.manpower_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_manpower, employees, header)))

        for emp in employees:
            grid = GridLayout(cols=5, spacing=10, size_hint_y=None, height=40)
            grid.add_widget(CLabel(text=emp["name"], size_hint_x=0.3))
            grid.add_widget(CLabel(text=emp["role"], size_hint_x=0.2))
            grid.add_widget(CLabel(text=emp["email"], size_hint_x=0.3))
            grid.add_widget(Button(text='View', on_release=partial(self.view_emp, emp["id"]),
                                   background_normal='', font_size='20sp', size_hint_x=0.1,
                                   background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1),
                                   bold=True))
            grid.add_widget(Button(text='Delete', on_release=partial(self.delete_employee, emp["id"]),
                                   background_normal='', font_size='20sp', size_hint_x=0.1,
                                   background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1),
                                   bold=True))
            grid.emp = emp
            self.ids.manpower_list.add_widget(grid)

    # Sorts Table Headers like a Table Column (It is not actually a Table but a ScrollView)
    # Manpower Sorting Function, takes headers, manpower List and calls populate function with sorted manpower list
    def sort_manpower(self, manpower: list, header: str, instance) -> None:
        if header == 'Name' or header == 'Name [D]':
            manpower = sorted(manpower, key=lambda x: x['name'])
            self.populate_manpower(manpower, ['Name [A]', 'Role', 'Email', '', ''])
        elif header == 'Name [A]':
            manpower = sorted(manpower, key=lambda x: x['name'], reverse=True)
            self.populate_manpower(manpower, ['Name [D]', 'Role', 'Email', '', ''])
        elif header == 'Role' or header == 'Role [D]':
            manpower = sorted(manpower, key=lambda x: x['role'])
            self.populate_manpower(manpower, ['Name', 'Role [A]', 'Email', '', ''])
        elif header == 'Role [A]':
            manpower = sorted(manpower, key=lambda x: x['role'], reverse=True)
            self.populate_manpower(manpower, ['Name', 'Role [D]', 'Email', '', ''])
        elif header == 'Email' or header == 'Email [D]':
            manpower = sorted(manpower, key=lambda x: x['email'])
            self.populate_manpower(manpower, ['Name', 'Role', 'Email [A]', '', ''])
        elif header == 'Email [A]':
            manpower = sorted(manpower, key=lambda x: x['email'], reverse=True)
            self.populate_manpower(manpower, ['Name', 'Role', 'Email [D]', '', ''])

    def search_manpower(self, search_text: str) -> None:
        if not search_text == '':
            manpower = load_manpower(0)
            results = []
            for emp in manpower:
                if (search_text.lower() in emp['name'].lower() or search_text.lower() in emp[
                    'role'].lower() or search_text.lower() in emp['email'].lower() or search_text.lower()
                        in emp['phone_number'].lower()):
                    results.append(emp)
            self.populate_manpower(results)

    def view_emp(self, emp_id: str, instance) -> None:
        temp_viewEmp_popup = Popup()
        viewEmp_popup = ViewManpower(self, emp_id, temp_viewEmp_popup)
        viewEmp = RPopup(title='View Employee', content=viewEmp_popup, size_hint=(0.6, 0.9))
        viewEmp_popup.popup = viewEmp
        viewEmp.open()

    @AccessControl
    def add_emp(self) -> None:
        temp_addEmp_popup = Popup()
        addEmp_popup = AddManpower(self, temp_addEmp_popup)
        addEmp = RPopup(title='Add Employee', content=addEmp_popup, size_hint=(0.45, 0.85))
        addEmp_popup.popup = addEmp
        addEmp.open()

    @AccessControl
    def delete_employee(self, emp_id: str, instance) -> None:
        self.dempID = emp_id
        emp = get_employee(emp_id)
        # get emp name
        emp_name = emp['name']
        self.CMessageBox('Delete Employee', f'Are you sure you want to \n delete employee {emp_name}?', 'Confirm',
                         'Yes', 'No',
                         self.confirmedDelete)

    def confirmedDelete(self, requestType: str = "Validated") -> None:
        if requestType == "Validated":
            if delete_employee(self.dempID):
                self.CMessageBox('Success', 'Employee deleted successfully.', 'Message')
                self.dempID = None
                self.populate_manpower(load_manpower(0))
                self.ids.manpower_filter.text = 'Filter: All'
            else:
                self.CMessageBox('Error', 'Failed to delete Employee.', 'Message')
                self.dempID = None
        else:
            print("illegal action")
            self.dempID = None

    # Open Message/Confirm Popup Window (Custom Widget implemented by Project Leader)
    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'Message',
                    btn1: str = 'OK', btn2: str = 'Cancel', btn1click=None, btn2click=None) -> None:
        if context == 'Message':
            msg_popup = MsgPopUp(self, content, context, btn1, btn1click)
            popup = RPopup(title=title, content=msg_popup, size_hint=(0.35, 0.3))
            msg_popup.popup = popup
            popup.open()
        elif context == 'Confirm':
            cfm_popup = CfmPopUp(self, content, context, btn1, btn2, btn1click, btn2click)
            popup = RPopup(title=title, content=cfm_popup, size_hint=(0.35, 0.3))
            cfm_popup.popup = popup
            popup.open()

    def btn_click(self, instance) -> None:
        text = instance.text
        if text == 'Back':
            self.parent.current = 'main'
        elif text == 'Add':
            self.add_emp()
        elif text == 'Refresh':
            self.populate_manpower(load_manpower(0))
            self.ids.manpower_filter.text = 'Filter: All'
            self.ids.search.text = ''
        elif text == 'Filter: All' or text == 'Filter: Perm' or text == 'Filter: Temp':
            if text == 'Filter: All':
                self.populate_manpower(load_manpower(1))
                self.ids.manpower_filter.text = 'Filter: Perm'
                self.ids.search.text = ''
            elif text == 'Filter: Perm':
                self.populate_manpower(load_manpower(2))
                self.ids.manpower_filter.text = 'Filter: Temp'
                self.ids.search.text = ''
            elif text == 'Filter: Temp':
                self.populate_manpower(load_manpower(0))
                self.ids.manpower_filter.text = 'Filter: All'
                self.ids.search.text = ''

    def dismiss_popup(self, instance) -> None:
        instance.dismiss
