from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from functools import partial
from functions.manpower import *
from functions.projects import load_project_names
import datetime
from utils import *
from custom import *
from validation import *


class AddManpower(GridLayout):
    def __init__(self, manpower_screen, **kwargs):
        super().__init__(**kwargs)
        self.manpower_screen = manpower_screen
        self.validCheck = 0

    def add_employee(self, requestType="Submit"):
        # Stringify
        name = str(self.ids.addEmp_name.text)
        email = str(self.ids.addEmp_email.text)
        phone_number = str(self.ids.addEmp_phone.text)
        role = str(self.ids.addEmp_role.text)
        status = str(self.ids.addEmp_status.text)
        salary = str(self.ids.addEmp_salary.text)

        # Check if all fields are full, except assignments
        if requestType == "Validate":
            if name == '' or email == '' or phone_number == '' or role == '' or status == '' or salary == '':
                self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_email(email):
                self.manpower_screen.CMessageBox('Error', 'Invalid email.', 'Message')
                return
            if not validate_mobileNo(phone_number):
                self.manpower_screen.CMessageBox('Error', 'Invalid phone number.', 'Message')
                return
            self.manpower_screen.CMessageBox('Add Employee', str('Are you sure you want to add employee ' + name + '?'), 'Confirm', 'Yes', 'No', self.add_employee)
            self.validCheck = 1
        if requestType == "Submit" and self.validCheck == 1:
            if add_employee(name, role, email, phone_number, status, [""], salary):
                self.manpower_screen.CMessageBox('Success', 'Employee added successfully.', 'Message')
                self.validCheck = 0
                self.manpower_screen.populate_manpower(load_manpower(0))
                self.popup.dismiss()
            else:
                self.manpower_screen.CMessageBox('Error', 'Failed to add Employee.', 'Message')
                self.validCheck = 0


class ViewManpower(GridLayout):
    def __init__(self, manpower_screen, emp_id, **kwargs):
        super().__init__(**kwargs)
        self.emp_id = emp_id
        self.manpower_screen = manpower_screen
        self.populateEmp()
        self.validCheck = 0

    def populateEmp(self):
        emp = get_employee(self.emp_id)

        self.ids.viewEmp_name.text = emp["name"]
        self.ids.viewEmp_role.text = emp["role"]
        self.ids.viewEmp_status.text = emp["employment_status"]
        self.ids.viewEmp_salary.text = emp["salary"]
        self.ids.viewEmp_email.text = emp["email"]
        self.ids.viewEmp_phone.text = emp["phone_number"]

        # emp["project_assignments"] is a list of projects, we display them in ScrollView named viewEmp_projects
        for project in emp["project_assignments"]:
            # there is one blank project assignment, where project: "", skip it
            if not project == "":
                grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=project, size_hint_x=0.8))
                grid.add_widget(
                    Button(text='X', background_normal='', background_color=(0.1, 0.1, 0.1, 0), font_size='20sp', bold=True,
                           font_name='Roboto', size_hint_x=0.2, on_release=partial(self.reload, project, "Remove")))
                self.ids.viewEmp_projects.add_widget(grid)

    def reload(self, project_name, action, instance):
        print(project_name, action)
        project_assignment(self.emp_id, project_name, action)
        # Clear all widgets from viewEmp_projects
        self.ids.viewEmp_projects.clear_widgets()
        self.populateEmp()

    def edit_employee(self, requestType="Submit"):
        # Project assignments is a list of projects
        # viewEmp_name.text, viewEmp_email.text, viewEmp_phone.text, viewEmp_role.text, viewEmp_status.text, viewEmp_salary.text
        # Stringify inputs
        name = str(self.ids.viewEmp_name.text)
        email = str(self.ids.viewEmp_email.text)
        phone_number = str(self.ids.viewEmp_phone.text)
        role = str(self.ids.viewEmp_role.text)
        status = str(self.ids.viewEmp_status.text)
        salary = str(self.ids.viewEmp_salary.text)

        if requestType == "Validate":
            # Check if all fields are full, except assignments
            if name == '' or email == '' or phone_number == '' or role == '' or status == '' or salary == '':
                self.manpower_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_email(email):
                self.manpower_screen.CMessageBox('Error', 'Invalid email.', 'Message')
                return
            if not validate_mobileNo(phone_number):
                self.manpower_screen.CMessageBox('Error', 'Invalid Mobile No.', 'Message')
                return
            self.manpower_screen.CMessageBox('Edit Employee', 'Are you sure you want to edit employee ' + name + '?', 'Confirm', 'Yes', 'No', self.edit_employee)
            self.validCheck = 1
        if requestType == "Submit":
            if self.validCheck == 1:
                if update_employee(self.emp_id, name, role, email, phone_number, status, salary):
                    self.manpower_screen.CMessageBox('Success', 'Employee edited successfully.', 'Message')
                    self.validCheck = 0
                    self.manpower_screen.populate_manpower(load_manpower(0))
                    self.popup.dismiss()
                else:
                    self.manpower_screen.CMessageBox('Error', 'Failed to edit Employee.', 'Message')
                    self.validCheck = 0

    def load_projects(self):
        return load_project_names()

    def dismiss_popup(self, instance):
        instance.dismiss


class ManpowerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_manpower(load_manpower(0))

    def populate_manpower(self, employees=load_manpower(0), headers=None):
        # Clear the existing widgets in the ScrollView
        self.ids.manpower_list.clear_widgets()
        self.ids.manpower_headers.clear_widgets()

        # headers
        if headers is None:
            headers = ['Name', 'Role', 'Email', '', '']
        size_hints = [0.3, 0.2, 0.3, 0.1, 0.1]
        for header in headers:
            self.ids.manpower_headers.add_widget(CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
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
            grid.add_widget(Button(text='Delete', on_release=partial(self.delete_employee, emp["id"], requestType="Validate"),
                                   background_normal='', font_size='20sp', size_hint_x=0.1,
                                   background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1),
                                   bold=True))
            grid.emp = emp
            self.ids.manpower_list.add_widget(grid)

    def sort_manpower(self, manpower, header, instance):
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

    def search_manpower(self, search_text):
        if not search_text == '':
            manpower = load_manpower(0)
            results = []
            for emp in manpower:
                if (search_text.lower() in emp['name'].lower() or search_text.lower() in emp[
                    'role'].lower() or search_text.lower() in emp['email'].lower() or search_text.lower()
                        in emp['phone_number'].lower()):
                    results.append(emp)
            self.populate_manpower(results)

    def view_emp(self, emp_id, instance):
        viewEmp = CPopup(title='View Employee', content=ViewManpower(self, emp_id), size_hint=(0.6, 0.8))
        viewEmp.open()
        viewEmp.content.popup = viewEmp

    def add_emp(self):
        addEmp = CPopup(title='Add Employee', content=AddManpower(self), size_hint=(0.5, 0.8))
        addEmp.open()
        addEmp.content.popup = addEmp

    def delete_employee(self, emp_id, requestType, instance):
        if requestType == "Validate":
            self.CMessageBox('Delete Employee', 'Are you sure you want to delete employee ' + emp_id + '?', 'Confirm', 'Yes', 'No',
                             partial(self.delete_employee, emp_id, "Delete"))
        else:
            delete_employee(emp_id)
            self.populate_manpower(load_manpower(0))
            self.ids.manpower_filter.text = 'Filter: All'

    def CMessageBox(self, title='Message', content='Message Content', context='None', btn1='Ok', btn2='Cancel', btn1click=None, btn2click=None):
        if context == 'Message':
            msgPopUp = CPopup(title=title, content=MsgPopUp(self, content, context, btn1, btn1click), size_hint=(0.35, 0.3))
            msgPopUp.open()
            msgPopUp.content.popup = msgPopUp
        if context == 'Confirm':
            cfmPopUp = CPopup(title=title, content=CfmPopUp(self, content, context, btn1, btn2, btn1click, btn2click), size_hint=(0.35, 0.3))
            cfmPopUp.open()
            cfmPopUp.content.popup = cfmPopUp

    def btn_click(self, instance):
        text = instance.text
        if text == 'Back':
            self.parent.current = 'main'
        elif text == 'Add':
            self.add_emp()
        elif text == 'Filter: All' or text == 'Filter: Perm' or text == 'Filter: Temp':
            if text == 'Filter: All':
                self.populate_manpower(load_manpower(1))
                self.ids.manpower_filter.text = 'Filter: Perm'
            elif text == 'Filter: Perm':
                self.populate_manpower(load_manpower(2))
                self.ids.manpower_filter.text = 'Filter: Temp'
            elif text == 'Filter: Temp':
                self.populate_manpower(load_manpower(0))
                self.ids.manpower_filter.text = 'Filter: All'

    def dismiss_popup(self, instance):
        instance.dismiss
