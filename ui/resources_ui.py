from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from functions.projects import load_project_names
from functions.resources import *
from functions.suppliers import load_supplier_names
from functools import partial

from utils import *


class ViewResource(GridLayout):
    def __init__(self, res_screen, res_id, **kwargs):
        super().__init__(**kwargs)
        self.res_id = res_id
        self.populate_view()
        self.res_screen = res_screen

    def populate_view(self):
        # Get the resource data from the DB
        res = get_res(self.res_id)
        # Assign
        self.ids.viewPop_name.text = res["name"]
        self.ids.viewPop_qty.text = str(res["quantity"])
        self.ids.viewPop_status.text = res["status"]
        self.ids.viewPop_supplier.text = res["supplier_name"]
        self.ids.viewPop_cost.text = str(res["unit_cost"])

        # we have this in JSON for firebase, 'resource_assignments': [{"amount": "", "project": ""}]
        # we need to parse this and display it in the ScrollView named viewRes_projects
        for assignment in res["resource_assignments"]:
            grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)
            grid.add_widget(CLabel(text=assignment["project"], size_hint_x=0.4))
            grid.add_widget(CLabel(text=assignment["amount"], size_hint_x=0.4))
            grid.add_widget(
                CButton(text='X', size_hint_x=0.05, on_release=partial(self.reload, assignment["amount"],
                                                                           assignment["project"], "Remove")))
            self.ids.viewRes_projects.add_widget(grid)

    def reload(self, amount, project_name, action, instance):
        resource_assignment(self.res_id, amount, project_name, action)
        self.ids.viewRes_projects.clear_widgets()
        self.populate_view()

    def editRes(self, name, qty, status, supplier, cost):
        # Stringify inputs (Including Dates)
        name = str(name)
        qty = str(qty)
        supplier = str(supplier)
        cost = str(cost)

        # Validate inputs
        if not validate_string(name, supplier):
            message_box('Error', 'All fields are required.')
            return
        if not validate_currency(qty):
            message_box('Error', 'Invalid Amount.')
            return
        # Send data to edit_res function in resources.py
        if confirm_box('Edit Resource', 'Are you sure you want to edit this resource?') == 'yes':
            if update_res(self.res_id, name, qty, status, supplier, cost):
                message_box('Success', 'Resource updated successfully.')
                self.res_screen.populate_res(load_resources(0))
                self.res_screen.ids.resource_filter.text = 'Filter: All'
                self.dismiss_popup(self.popup)

    def deleteRes(self):
        # Send res_id to resources.py and it will delete the entity
        if confirm_box('Delete Resource', 'Are you sure you want to delete this resource?') == 'yes':
            if delete_res(self.res_id):
                message_box('Success', 'Resource deleted successfully.')
            else:
                message_box('Error', 'Failed to delete.')
            self.res_screen.populate_res(load_resources(0))
            self.res_screen.ids.resource_filter.text = 'Filter: All'
            self.dismiss_popup(self.popup)

    def load_suppliers(self):
        return load_supplier_names()

    def load_projects(self):
        return load_project_names()

    def reportRes(self):
        reportPop = CPopup(title='Report Resource', content=ReportResource(self.res_id), size_hint=(0.5, 0.8))
        reportPop.open()
        reportPop.content.popup = reportPop

    def dismiss_popup(self, instance):
        instance.dismiss()


class ReportResource(GridLayout):
    # Report Popup, you will see an overview of the resource, that is all
    def __init__(self, res_id, **kwargs):
        super().__init__(**kwargs)
        self.res_id = res_id
        self.populate_report()

    def populate_report(self):
        res = get_res(self.res_id)
        self.ids.reportRes_name.text = res["name"]
        self.ids.reportRes_qty.text = str(res["quantity"])
        self.ids.reportRes_status.text = res["status"]
        self.ids.reportRes_supplier.text = res["supplier_name"]
        self.ids.reportRes_cost.text = str(res["unit_cost"])

        for assignment in res["resource_assignments"]:
            grid = GridLayout(cols=2, size_hint_y=None, height=60)
            grid.add_widget(CLabel(text=assignment["project"], size_hint_x=0.8))
            grid.add_widget(CLabel(text=assignment["amount"], size_hint_x=0.2))
            self.ids.assigned_projects.add_widget(grid)

    def dismiss_popup(self, instance):
        instance.dismiss()


# Manpower Main UI (Opens this from main.py)
class ResourcesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_res(load_resources(0))

    # Populate the ScrollView with the resources
    def populate_res(self, resources=load_resources(0), headers=None):
        # Clear the existing widgets in the ScrollView
        self.ids.resources_list.clear_widgets()
        self.ids.resource_headers.clear_widgets()

        # headers
        if headers is None:
            headers = ['Name', 'Status', 'Supplier', 'Stock']
        for header in headers:
            self.ids.resource_headers.add_widget(CButton(text=header, bold=True, padding=(10, 10),
                                                         on_release=partial(self.sort_resources, resources, header)))

        # Fill Data into ScrollView
        for res in resources:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
            button = Button(text=res["name"], on_release=partial(self.view_res, res["id"]),
                            background_normal='', font_size='20sp',
                            background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
            grid.res = res
            grid.add_widget(button)
            grid.add_widget(CLabel(text=res["status"]))
            grid.add_widget(CLabel(text=res["supplier_name"]))
            grid.add_widget(CLabel(text=str(res["quantity"])))
            self.ids.resources_list.add_widget(grid)

    def sort_resources(self, resources, header, instance):
        if header == 'Name' or header == 'Name [D]':
            resources = sorted(resources, key=lambda x: x['name'])
            self.populate_res(resources, ['Name [A]', 'Status', 'Supplier', 'Stock'])
        elif header == 'Name [A]':
            resources = sorted(resources, key=lambda x: x['name'], reverse=True)
            self.populate_res(resources, ['Name [D]', 'Status', 'Supplier', 'Stock'])
        elif header == 'Status' or header == 'Status [D]':
            resources = sorted(resources, key=lambda x: x['status'])
            self.populate_res(resources, ['Name', 'Status [A]', 'Supplier', 'Stock'])
        elif header == 'Status [A]':
            resources = sorted(resources, key=lambda x: x['status'], reverse=True)
            self.populate_res(resources, ['Name', 'Status [D]', 'Supplier', 'Stock'])
        elif header == 'Supplier' or header == 'Supplier [D]':
            resources = sorted(resources, key=lambda x: x['supplier_name'])
            self.populate_res(resources, ['Name', 'Status', 'Supplier [A]', 'Stock'])
        elif header == 'Supplier [A]':
            resources = sorted(resources, key=lambda x: x['supplier_name'], reverse=True)
            self.populate_res(resources, ['Name', 'Status', 'Supplier [D]', 'Stock'])
        elif header == 'Stock' or header == 'Stock [D]':
            resources = sorted(resources, key=lambda x: x['quantity'])
            self.populate_res(resources, ['Name', 'Status', 'Supplier', 'Stock [A]'])
        elif header == 'Stock [A]':
            resources = sorted(resources, key=lambda x: x['quantity'], reverse=True)
            self.populate_res(resources, ['Name', 'Status', 'Supplier', 'Stock [D]'])

    def search_res(self, search_text):
        if not search_text == '':
            resources = load_resources(0)
            results = []
            for res in resources:
                if search_text.lower() in res["name"].lower() or search_text.lower() in res["supplier_name"].lower():
                    results.append(res)
            self.populate_res(results)

    # Triggers the ViewResource PopUp Window
    def view_res(self, res_id, instance):
        viewPop = CPopup(title='View Resource', content=ViewResource(self, res_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Triggers the AddResourcePopup Window
    def add_resource_popup(self):
        addPop = CPopup(title='Add Resource', content=AddResource(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    # Button Click goes back to Main UI
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add':
            self.add_resource_popup()
        elif instance.text == 'Filter: All' or instance.text == 'Filter: In Stock' or instance.text == 'Filter: Out of Stock':
            if instance.text == 'Filter: All':
                self.ids.resource_filter.text = 'Filter: In Stock'
                self.populate_res(load_resources(1))
            elif instance.text == 'Filter: In Stock':
                self.ids.resource_filter.text = 'Filter: Out of Stock'
                self.populate_res(load_resources(2))
            elif instance.text == 'Filter: Out of Stock':
                self.ids.resource_filter.text = 'Filter: All'
                self.populate_res(load_resources(3))

    def dismiss_popup(self, instance):
        instance.dismiss()


class AddResource(GridLayout):
    def __init__(self, res_screen, **kwargs):
        super().__init__(**kwargs)
        self.res_screen = res_screen

    def add_resource(self, name, qty, status, supplier, cost):
        # Stringify inputs (Including Dates)
        name = str(name)
        qty = str(qty)
        supplier = str(supplier)
        cost = str(cost)

        # Validate inputs
        if not validate_string(name, supplier, qty, status):
            message_box('Error', 'All fields are required.')
            return
        if not validate_currency(qty):
            message_box('Error', 'Invalid Amount.')
            return
        if not validate_currency(cost):
            message_box('Error', 'Invalid Cost.')
            return

        # Add data to DB
        if confirm_box('Add Resource', 'Are you sure you want to add this resource?') == 'yes':
            if add_res(name, qty, status, supplier, cost):
                message_box('Success', 'Resource added successfully.')
                # Refresh the resources display
                self.res_screen.populate_res(load_resources(0))
                self.res_screen.ids.resource_filter.text = 'Filter: All'
                self.dismiss_popup(self.popup)
            else:
                message_box('Error', 'Failed to add resource.')

    def load_suppliers(self):
        return load_supplier_names()

    def dismiss_popup(self, instance):
        instance.dismiss()
