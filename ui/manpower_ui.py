from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from functools import partial
from functions.manpower import *
from functions.projects import load_project_names
import datetime
from utils import *
from custom import *


class AddManpower(GridLayout):
    def __init__(self, manpower_screen, **kwargs):
        super().__init__(**kwargs)
        self.manpower_screen = manpower_screen

    def add_employee(self, name, email, phone_number, role, employment_status, salary):
        # Stringify
        name = str(name)
        email = str(email)
        phone_number = str(phone_number)
        role = str(role)
        status = str(employment_status)
        salary = str(salary)

        # Check if all fields are full, except assignments
        if name == '' or email == '' or phone_number == '' or role == '' or status == '' or salary == '':
            message_box('Error', 'All fields are required.')
            return
        if not validate_email(email):
            message_box('Error', 'Invalid email.')
            return
        if not validate_mobileNo(phone_number):
            message_box('Error', 'Invalid phone number.')
            return
        if confirm_box('Add Employee', 'Are you sure you want to add employee ' + name + '?') == 'yes':
            if add_employee(name, role, email, phone_number, status, [""], salary):
                message_box('Success', 'Employee added successfully.')
                self.manpower_screen.populate_manpower(load_manpower(0))
                self.popup.dismiss()
            else:
                message_box('Error', 'Failed to add Employee.')


class ViewManpower(GridLayout):
    def __init__(self, manpower_screen, emp_id, **kwargs):
        super().__init__(**kwargs)
        self.emp_id = emp_id
        self.manpower_screen = manpower_screen
        self.populateEmp()

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
            grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)
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

    def edit_employee(self, name, email, phone_number, role, employment_status, salary):
        # Project assignments is a list of projects
        # Stringify inputs
        name = str(name)
        email = str(email)
        phone_number = str(phone_number)
        role = str(role)
        status = str(employment_status)
        salary = str(salary)

        # Check if all fields are full, except assignments
        if name == '' or email == '' or phone_number == '' or role == '' or status == '' or salary == '':
            message_box('Error', 'All fields are required.')
            return
        if not validate_email(email):
            message_box('Error', 'Invalid email.')
            return
        if not validate_mobileNo(phone_number):
            message_box('Error', 'Invalid phone number.')
            return
        if confirm_box('Edit Employee', 'Are you sure you want to edit employee ' + name + '?') == 'yes':
            if update_employee(self.emp_id, name, role, email, phone_number, status, salary):
                message_box('Success', 'Employee edited successfully.')
                self.manpower_screen.populate_manpower(load_manpower(0))
                self.popup.dismiss()
            else:
                message_box('Error', 'Failed to edit Employee.')

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
        for header in headers:
            self.ids.manpower_headers.add_widget(CButton(text=header, bold=True, padding=(10, 10),
                                                         on_release=partial(self.sort_manpower, employees, header)))

        for emp in employees:
            grid = GridLayout(cols=5, spacing=10, size_hint_y=None, height=50)
            grid.add_widget(CLabel(text=emp["name"]))
            grid.add_widget(CLabel(text=emp["role"]))
            grid.add_widget(CLabel(text=emp["email"]))
            grid.add_widget(Button(text='View', on_release=partial(self.view_emp, emp["id"]),
                                   background_normal='', font_size='20sp',
                                   background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1),
                                   bold=True))
            grid.add_widget(Button(text='Delete', on_release=partial(self.delete_employee, emp["id"]),
                                   background_normal='', font_size='20sp',
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

    def delete_employee(self, emp_id, instance):
        if confirm_box('Delete Employee', 'Are you sure you want to delete employee ' + emp_id + '?') == 'yes':
            delete_employee(emp_id)
            self.populate_manpower(load_manpower(0))
            self.ids.manpower_filter.text = 'All'
        else:
            message_box('Error', 'Failed to delete Employee.')

    def btn_click(self, instance):
        text = instance.text
        if text == 'Back':
            self.parent.current = 'main'
        elif text == 'Add':
            self.add_emp()
        elif text == 'All' or text == 'Perm' or text == 'Temp':
            if text == 'All':
                self.populate_manpower(load_manpower(1))
                self.ids.manpower_filter.text = 'Perm'
            elif text == 'Perm':
                self.populate_manpower(load_manpower(2))
                self.ids.manpower_filter.text = 'Temp'
            elif text == 'Temp':
                self.populate_manpower(load_manpower(0))
                self.ids.manpower_filter.text = 'All'

    def dismiss_popup(self, instance):
        instance.dismiss
