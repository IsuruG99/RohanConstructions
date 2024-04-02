from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.suppliers import *
from functools import partial

from utils import *


class AddSupPopup(GridLayout):
    def __init__(self, suppliers_screen, **kwargs):
        super().__init__(**kwargs)
        self.suppliers_screen = suppliers_screen

    def add_Supplier(self, supplierName, business, contactNo, email, address, startDealing, supplierLevel):
        supplierName = str(supplierName)
        business = str(business)
        contactNo = str(contactNo)
        email = str(email)
        address = str(address)
        startDealing = str(startDealing)
        supplierLevel = str(supplierLevel)

        # Validate inputs
        if not validate_string(supplierName, contactNo, email, address):
            message_box('Error', 'All fields are required.')
            return
        if not validate_date(startDealing):
            message_box('Error', 'Invalid date format.')
            return

        # Send data to supplier.py
        add_supplier(supplierName, business, contactNo, email, address, startDealing, supplierLevel)
        message_box('Success', 'New supplier added successfully.')
        self.suppliers_screen.populate_suppliers(0)

    def dismiss_popup(self, instance):
        instance.dismiss()


# Suppliers Main UI (Accessed by main.py)
class SuppliersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_suppliers(0)

    # Button Click Event Handler
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add New Supplier':
            self.add_popup()

    def populate_suppliers(self, status):
        # Get the suppliers from the database
        suppliers = load_suppliers()

        # Clear the existing widgets in the ScrollView
        self.ids.Supplier_list.clear_widgets()

        if status == 0:
            for supplier in suppliers:
                grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
                button = Button(text=supplier["business"], on_release=partial(self.view_suppliers, supplier["id"]),
                                background_normal='',
                                background_color=(1, 1, 1, 0), font_name='Roboto', color=(1, 1, 1, 1), bold=True)
                grid.supplier = supplier
                grid.add_widget(button)
                grid.add_widget(Label(text=supplier["supplierName"]))
                grid.add_widget(Label(text=supplier["contactNo"]))
                grid.add_widget(Label(text=supplier["supplierLevel"]))
                self.ids.Supplier_list.add_widget(grid)

    def view_suppliers(self, sup_id, instance):
        pass

    # Open to supplier add popup window
    def add_popup(self):
        addPop = Popup(title='Add Supplier', content=AddSupPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop
