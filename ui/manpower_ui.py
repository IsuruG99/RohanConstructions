from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import functions.manpower as manpower
from utils import message_box


class ManpowerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_manpower(0)

    def set_screen_manager(self, screen_manager):
        self.screen_manager = screen_manager

    def populate_manpower(self, status):
        # Get the employees from the database
        employees = manpower.load_manpower()

        # Clear the existing widgets in the ScrollView
        self.ids.manpower_list.clear_widgets()

        if status == 0:
            for emp in employees:
                grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
                button = Button(text=emp.get("name", ""), on_release=partial(self.view_emp, emp["id"]),
                                background_normal='',
                                background_color=(1, 1, 1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
                grid.emp = emp
                grid.add_widget(button)
                grid.add_widget(Label(text=emp.get("role", "")))
                grid.add_widget(Label(text=emp.get("email", "")))
                delete_button = Button(text='Delete', on_release=partial(self.delete_employee, emp["id"]))
                grid.add_widget(delete_button)
                self.ids.manpower_list.add_widget(grid)

    def back_to_main_screen(self, instance):
        if self.screen_manager:
            self.screen_manager.current = "main"

    def view_emp(self, emp_id):
        viewPop = Popup(title='View Employee', content=ViewManpower(emp_id), size_hint=(0.5, 0.8))
        viewPop.open()

    def add_manpower_popup(self):
        addPop = AddManpowerPopup(title='Add Employee', screen_manager=self)
        addPop.bind(on_dismiss=self.populate_manpower)  # Refresh the manpower list after adding
        addPop.open()

    def delete_employee(self, emp_id, instance=None):
        confirm_box = self.confirm_box("Confirmation", "Are you sure you want to delete this employee?", emp_id)

    def perform_delete(self, emp_id):
        if manpower.delete_employee(emp_id):
            self.populate_manpower(0)
            success_popup = Popup(title='Success', content=Label(text='Employee deleted successfully.'),
                                  size_hint=(None, None), size=(400, 200))
            success_popup.open()
        else:
            error_popup = Popup(title='Error', content=Label(text='Failed to delete employee.'), size_hint=(None, None),
                                size=(400, 200))
            error_popup.open()

    def confirm_box(self, title, message, emp_id):
        confirm_popup_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        confirm_popup_content.add_widget(Label(text=message))
        button_layout = BoxLayout(spacing=10)

        def on_confirm(instance):
            self.perform_delete(emp_id)
            confirm_popup.dismiss()

        def on_cancel(instance):
            confirm_popup.dismiss()

        confirm_button = Button(text="Confirm")
        cancel_button = Button(text="Cancel")

        confirm_button.bind(on_release=on_confirm)
        cancel_button.bind(on_release=on_cancel)

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        confirm_popup_content.add_widget(button_layout)

        confirm_popup = Popup(title=title, content=confirm_popup_content, size_hint=(0.5, 0.5))
        confirm_popup.open()
        confirm_popup.bind(on_dismiss=lambda instance: setattr(self, "confirm_response", "no"))

        return confirm_popup


class AddManpowerPopup(Popup):
    def __init__(self, **kwargs):
        self.screen_manager = kwargs.pop('screen_manager', None)  # Get screen_manager from kwargs
        super().__init__(**kwargs)
        self.create_content()

    def create_content(self):
        layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(Label(text='Name', size_hint=(None, None), size=(100, 40)))
        self.name_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.name_input)

        layout.add_widget(Label(text='Role', size_hint=(None, None), size=(100, 40)))
        self.role_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.role_input)

        layout.add_widget(Label(text='Email', size_hint=(None, None), size=(100, 40)))
        self.email_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.email_input)

        layout.add_widget(Label(text='Phone', size_hint=(None, None), size=(100, 40)))
        self.phone_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.phone_input)

        layout.add_widget(Label(text='Status', size_hint=(None, None), size=(100, 40)))
        self.status_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.status_input)

        layout.add_widget(Label(text='Projects', size_hint=(None, None), size=(100, 40)))
        self.projects_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 40))
        layout.add_widget(self.projects_input)

        submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 40))
        submit_button.bind(on_press=self.submit)
        layout.add_widget(submit_button)

        # Add back button
        back_button = Button(text='Back', size_hint=(None, None), size=(100, 40))
        back_button.bind(on_press=self.dismiss)
        layout.add_widget(back_button)

        self.content = layout

    def submit(self, instance):
        name = self.name_input.text
        role = self.role_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        status = self.status_input.text
        projects = self.projects_input.text
        if manpower.add_employee(name, role, email, phone, status, projects):
            self.dismiss()  # Dismiss the popup after successfully adding an employee
            if self.screen_manager:
                self.screen_manager.populate_manpower(0)  # Update the manpower list
        else:
            message_box('Error', 'Failed to add employee')


class ViewManpower(BoxLayout):
    def __init__(self, emp_id, **kwargs):
        super().__init__(**kwargs)
        self.emp_id = emp_id
        employee = manpower.get_employee(emp_id)
        if employee:
            self.ids.viewPop_name.text = employee.get('name', '')
            self.ids.viewPop_role.text = employee.get('role', '')
            self.ids.viewPop_email.text = employee.get('email', '')
            self.ids.viewPop_phone.text = employee.get('phone_number', '')
            self.ids.viewPop_status.text = employee.get('employment_status', '')
            self.ids.viewPop_projects.text = ', '.join(employee.get('project_assignments', []))
