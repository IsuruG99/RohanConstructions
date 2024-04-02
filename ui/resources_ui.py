from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.resources import *
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
        update_res(self.res_id, name, qty, status, supplier, cost)
        message_box('Success', 'Resource updated successfully.')
        self.res_screen.populate_res(0)
        self.dismiss_popup(self.popup)

    def deleteRes(self):
        # Send res_id to resources.py and it will delete the entity
        if confirm_box('Delete Resource', 'Are you sure you want to delete this resource?') == 'yes':
            if delete_res(self.res_id):
                message_box('Success', 'Resource deleted successfully.')
            else:
                message_box('Error', 'Failed to delete.')
            self.res_screen.populate_res(0)
            self.dismiss_popup(self.popup)

    def reportRes(self):
        message_box('Report', 'Not currently implemented.')

    def dismiss_popup(self, instance):
        instance.dismiss()


# Manpower Main UI (Opens this from main.py)
class ResourcesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_res(0)
        self.switch = 0

    # Button Click goes back to Main UI
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add':
            self.add_resource_popup()

    # Populate the ScrollView with the resources
    def populate_res(self, status):
        # Get the resources from the database
        resources = load_resources()

        # Clear the existing widgets in the ScrollView
        self.ids.resources_list.clear_widgets()

        if status == 0:
            for res in resources:
                grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)
                button = Button(text=res["name"], on_release=partial(self.view_res, res["id"]),
                                background_normal='',
                                background_color=(1, 1, 1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
                grid.res = res
                grid.add_widget(button)
                grid.add_widget(Label(text=res["status"]))
                grid.add_widget(Label(text=res["supplier_name"]))
                self.ids.resources_list.add_widget(grid)

    # Triggers the ViewResource PopUp Window
    def view_res(self, res_id, instance):
        viewPop = Popup(title='View Resource', content=ViewResource(self, res_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Triggers the AddResourcePopup Window
    def add_resource_popup(self):
        addPop = AddResourcePopup(self)
        addPop.open()

    def dismiss_popup(self, instance):
        instance.dismiss()


class AddResourcePopup(Popup):
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
        if not validate_string(name, supplier):
            message_box('Error', 'All fields are required.')
            return
        if not validate_currency(qty):
            message_box('Error', 'Invalid Amount.')
            return

        # Add resource
        if add_res(name, qty, status, supplier, cost):
            message_box('Success', 'Resource added successfully.')
            self.dismiss()
        else:
            message_box('Error', 'Failed to add resource.')
        # Refresh the resources display
        self.res_screen.populate_res(0)
        self.dismiss()
