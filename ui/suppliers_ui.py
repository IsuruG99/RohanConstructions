from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.suppliers import *
from functools import partial

from utils import *
from custom import *


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
            message_box('Error', 'You missed some information !')
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


class ViewSupPopup(GridLayout):
    def __init__(self, sup_screen, sup_id, **kwargs):
        super().__init__(**kwargs)
        self.sup_id = sup_id
        self.populate_view()
        self.sup_screen = sup_screen

    # Populate PopUp Window
    def populate_view(self):
        # Get the suppliers data from the DB
        sp = get_supplier(self.sup_id)
        # Assign
        self.ids.supplierName.text = sp["supplierName"]
        self.ids.business.text = sp["business"]
        self.ids.address.text = sp["address"]
        self.ids.email.text = sp["email"]
        self.ids.contactNo.text = sp["contactNo"]
        self.ids.startDealing.text = sp["startDealing"]
        self.ids.supplierLevel.text = sp["supplierLevel"]

    # Edit Supplier
    def editSupplier(self, supplierName, business, contactNo, email, address, startDealing, supplierLevel):
        # Stringify inputs (Including Dates)
        supplierName = str(supplierName)
        business = str(business)
        email = str(email)
        contactNo = str(contactNo)
        startDealing = str(startDealing)
        supplierLevel = str(supplierLevel)
        address = str(address)

        # Validate inputs
        if not validate_string(supplierName, business, contactNo, email, address, startDealing, supplierLevel):
            message_box('Error', 'You missed some information !')
            return
        if not validate_date(startDealing):
            message_box('Error', 'Invalid date format.')
            return
        # Send data to suppliers.py
        edit_supplier(self.sup_id, supplierName, business, contactNo, email, address, startDealing, supplierLevel)
        self.sup_screen.populate_suppliers(0)
        self.dismiss_popup(self.popup)

    # Open Reports Popup Window
    def reports_popup(self):
        pass

    # Delete Project
    def deleteSupplier(self):
        delete_supplier(self.sup_id)
        self.sup_screen.populate_suppliers(0)
        self.dismiss_popup(self.popup)

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

        # Headers
        grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
        headers = ['Business', 'Owner', 'Contact', 'Level']
        for header in headers:
            grid.add_widget(CLabel(text=header, bold=True, padding=(10, 10)))
        self.ids.Supplier_list.add_widget(grid)

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
        viewPop = Popup(title='View Supplier', content=ViewSupPopup(self, sup_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Open to supplier add popup window
    def add_popup(self):
        addPop = Popup(title='Add Supplier', content=AddSupPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop


