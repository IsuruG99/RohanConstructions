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
from validation import *


class ViewResource(GridLayout):
    def __init__(self, res_screen: Screen, res_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.res_id = res_id
        self.populate_view()
        self.res_screen = res_screen
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_view(self) -> None:
        # Get the resource data from the DB
        res = get_res(self.res_id)
        # Assign
        self.ids.viewPop_name.text = res["name"]
        self.ids.viewPop_qty.text = str(res["quantity"])
        self.ids.viewPop_status.text = res["status"]
        self.ids.viewPop_supplier.text = res["supplier_name"]
        self.ids.viewPop_cost.text = str(res["unit_cost"])

        # res assignment format in DB, ('resource_assignments': [{"amount": "", "project": ""}])
        for assignment in res["resource_assignments"]:
            grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)
            grid.add_widget(CLabel(text=assignment["project"], size_hint_x=0.4))
            grid.add_widget(CLabel(text=assignment["amount"], size_hint_x=0.4))
            grid.add_widget(
                CButton(text='X', size_hint_x=0.05, on_release=partial(self.reload, assignment["amount"],
                                                                       assignment["project"], "Remove")))
            self.ids.viewRes_projects.add_widget(grid)

    def reload(self, amount: str, project_name: str, action: str, instance) -> None:
        if project_name == "":
            self.res_screen.CMessageBox('Error', 'Project Name is required.', 'Message')
            return
        if amount == "" or amount == "0":
            self.res_screen.CMessageBox('Error', 'Specify the Quantity', 'Message')
        else:
            if (int(get_res(self.res_id)["quantity"]) - int(amount)) < 0:
                self.res_screen.CMessageBox('Error', 'Out of Stock', 'Message')
                return
            else:
                resource_assignment(self.res_id, amount, project_name, action)
                self.ids.viewRes_projects.clear_widgets()
                self.populate_view()

    def editRes(self, requestType: str = "Submit") -> None:
        # Stringify inputs (Including Dates)
        name = str(self.ids.viewPop_name.text)
        qty = str(self.ids.viewPop_qty.text)
        status = self.ids.viewPop_status.text
        supplier = str(self.ids.viewPop_supplier.text)
        cost = str(self.ids.viewPop_cost.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(name, supplier):
                self.res_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_currency(qty):
                self.res_screen.CMessageBox('Error', 'Invalid Quantity.', 'Message')
                return
            self.res_screen.CMessageBox('Edit Resource', 'Are you sure you want to edit this resource?', 'Confirm',
                                        'Yes', 'No', self.editRes)
            self.validCheck = 1
        # Send data to edit_res function in resources.py
        elif requestType == "Submit":
            if self.validCheck == 1:
                if update_res(self.res_id, name, qty, status, supplier, cost):
                    self.res_screen.CMessageBox('Success', 'Resource edited successfully.', 'Message')
                    self.res_screen.populate_res(load_resources(0))
                    self.validCheck = 0
                    self.res_screen.ids.resource_filter.text = 'Filter: All'
                    self.dismiss_popup(self.popup)
                else:
                    self.res_screen.CMessageBox('Error', 'Failed to edit resource.', 'Message')


    def deleteRes(self, requestType: str = "Submit") -> None:
        # Send res_id to resources.py and it will delete the entity
        if requestType == "Validate":
            self.res_screen.CMessageBox('Delete Resource', 'Are you sure you want to delete this resource?', 'Confirm',
                                        'Yes', 'No', self.deleteRes)
            self.validCheck = 1
        elif requestType == "Submit":
            if delete_res(self.res_id):
                self.res_screen.CMessageBox('Success', 'Resource deleted successfully.', 'Message')
            else:
                self.res_screen.CMessageBox('Error', 'Failed to delete resource.', 'Message')
            self.validCheck = 0
            self.res_screen.populate_res(load_resources(0))
            self.res_screen.ids.resource_filter.text = 'Filter: All'
            self.dismiss_popup(self.popup)

    def load_suppliers(self) -> list:
        return load_supplier_names()

    def load_projects(self) -> list:
        return load_project_names()

    def reportRes(self) -> None:
        temp_reportPop_popup = Popup()
        reportPop_popup = ReportResource(self.res_id, temp_reportPop_popup)
        reportPop = RPopup(title='Report Resource', content=reportPop_popup, size_hint=(0.5, 0.9))
        reportPop_popup.popup = reportPop
        reportPop.open()

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


class ReportResource(GridLayout):
    # Report Popup, you will see an overview of the resource, that is all
    def __init__(self, res_id, popup, **kwargs):
        super().__init__(**kwargs)
        self.res_id = res_id
        self.popup = popup
        self.populate_report()
        self.cols = 1
        self.rows = 1

    def populate_report(self) -> None:
        res = get_res(self.res_id)
        self.ids.reportRes_name.text = res["name"]
        self.ids.reportRes_qty.text = str(res["quantity"])
        self.ids.reportRes_status.text = res["status"]
        self.ids.reportRes_supplier.text = res["supplier_name"]
        self.ids.reportRes_cost.text = str(res["unit_cost"])

        for assignment in res["resource_assignments"]:
            if not assignment["project"] == "":
                grid = GridLayout(cols=2, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=assignment["project"], size_hint_x=0.8))
                grid.add_widget(CLabel(text=assignment["amount"], size_hint_x=0.2))
                self.ids.assigned_projects.add_widget(grid)

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


# Manpower Main UI (Opens this from main.py)
class ResourcesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_res(load_resources(0))

    # Populate the ScrollView with the resources
    def populate_res(self, resources: list = load_resources(0), headers: list = None) -> None:
        # Clear the existing widgets in the ScrollView
        self.ids.resources_list.clear_widgets()
        self.ids.resource_headers.clear_widgets()

        # headers
        if headers is None:
            headers = ['Name', 'Status', 'Supplier', 'Stock']
        size_hints = [0.4, 0.2, 0.3, 0.1]
        for header in headers:
            self.ids.resource_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_resources, resources, header)))

        # Fill Data into ScrollView
        for res in resources:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            button = Button(text=res["name"], on_release=partial(self.view_res, res["id"]),
                            background_normal='', font_size='20sp', size_hint_x=0.4,
                            background_color=(0.1, 0.1, 0.1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
            grid.res = res
            grid.add_widget(button)
            grid.add_widget(CLabel(text=res["status"], size_hint_x=0.2))
            grid.add_widget(CLabel(text=res["supplier_name"], size_hint_x=0.3))
            grid.add_widget(CLabel(text=str(res["quantity"]), size_hint_x=0.1))
            self.ids.resources_list.add_widget(grid)

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'None',
                    btn1: str = 'Ok', btn2: str = 'Cancel',
                    btn1click=None, btn2click=None) -> None:
        if context == 'Message':
            msgPopUp = CPopup(title=title, content=MsgPopUp(self, content, context, btn1, btn1click),
                              size_hint=(0.35, 0.3))
            msgPopUp.open()
            msgPopUp.content.popup = msgPopUp
        if context == 'Confirm':
            cfmPopUp = CPopup(title=title, content=CfmPopUp(self, content, context, btn1, btn2, btn1click, btn2click),
                              size_hint=(0.35, 0.3))
            cfmPopUp.open()
            cfmPopUp.content.popup = cfmPopUp

    def sort_resources(self, resources: list, header: str, instance) -> None:
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

    def search_res(self, search_text: str) -> None:
        if not search_text == '':
            resources = load_resources(0)
            results = []
            for res in resources:
                if search_text.lower() in res["name"].lower() or search_text.lower() in res["supplier_name"].lower():
                    results.append(res)
            self.populate_res(results)

    # Triggers the ViewResource PopUp Window
    def view_res(self, res_id: str, instance) -> None:
        temp_viewPop_popup = Popup()
        viewPop_popup = ViewResource(self, res_id, temp_viewPop_popup)
        viewPop = RPopup(title='View Resource', content=viewPop_popup, size_hint=(0.55, 0.9))
        viewPop_popup.popup = viewPop
        viewPop.open()

    # Triggers the AddResourcePopup Window
    def add_resource_popup(self) -> None:
        temp_addPop_popup = Popup()
        addPop_popup = AddResource(self, temp_addPop_popup)
        addPop = RPopup(title='Add Resource', content=addPop_popup, size_hint=(0.45, 0.8))
        addPop_popup.popup = addPop
        addPop.open()

    # Button Click goes back to Main UI
    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == 'Back':
            self.parent.current = 'main'
        elif txt == 'Add':
            self.add_resource_popup()
        elif txt == 'Filter: All' or txt == 'Filter: In Stock' or txt == 'Filter: Out of Stock':
            if txt == 'Filter: All':
                self.ids.resource_filter.text = 'Filter: In Stock'
                self.populate_res(load_resources(1))
            elif txt == 'Filter: In Stock':
                self.ids.resource_filter.text = 'Filter: Out of Stock'
                self.populate_res(load_resources(2))
            elif txt == 'Filter: Out of Stock':
                self.ids.resource_filter.text = 'Filter: All'
                self.populate_res(load_resources(3))

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()


class AddResource(GridLayout):
    def __init__(self, res_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.res_screen = res_screen
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def add_resource(self, requestType: str = "Submit") -> None:
        # Stringify inputs (Including Dates)
        name = str(self.ids.addRes_name.text)
        qty = str(self.ids.addRes_qty.text)
        status = self.ids.addRes_status.text
        supplier = str(self.ids.addRes_supplier.text)
        cost = str(self.ids.addRes_cost.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(name, supplier, qty, status):
                self.res_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_currency(qty):
                self.res_screen.CMessageBox('Error', 'Invalid Quantity.', 'Message')
                return
            if not validate_currency(cost):
                self.res_screen.CMessageBox('Error', 'Invalid Cost.', 'Message')
                return
            self.res_screen.CMessageBox('Add Resource', 'Are you sure you want to add this resource?', 'Confirm',
                                        'Yes', 'No', self.add_resource)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                if add_res(name, qty, status, supplier, cost):
                    self.res_screen.CMessageBox('Success', 'Resource added successfully.', 'Message')
                    self.res_screen.populate_res(load_resources(0))
                    self.res_screen.ids.resource_filter.text = 'Filter: All'
                    self.validCheck = 0
                    self.dismiss_popup(self.popup)
                else:
                    self.res_screen.CMessageBox('Error', 'Failed to add resource.', 'Message')

    def load_suppliers(self) -> list:
        return load_supplier_names()

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()
