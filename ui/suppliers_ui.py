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

        if not validate_mobileNo(contactNo):
            message_box('Error', 'Check the contact number')
            return

        if not validate_date(startDealing):
            message_box('Error', 'Invalid date format.')
            return

        # Send data to supplier.py
        add_supplier(supplierName, business, contactNo, email, address, startDealing, supplierLevel)
        message_box('Success', 'New supplier added successfully.')
        self.suppliers_screen.populate_suppliers()

    def dismiss_popup(self, instance):
        self.suppliers_screen.dismiss_popup(self.popup)


class ViewSupPopup(GridLayout):
    def __init__(self, suppliers_screen, suppliers_id, **kwargs):
        super().__init__(**kwargs)
        self.suppliers_id = suppliers_id
        self.populate_view()
        self.suppliers_screen = suppliers_screen

    # Populate PopUp Window
    def populate_view(self):
        # Get the suppliers data from the DB
        supplier = get_supplier(self.suppliers_id)
        # Assign
        self.ids.supplierName.text = supplier["supplierName"]
        self.ids.business.text = supplier["business"]
        self.ids.address.text = supplier["address"]
        self.ids.email.text = supplier["email"]
        self.ids.contactNo.text = supplier["contactNo"]
        self.ids.startDealing.text = supplier["startDealing"]
        self.ids.supplierLevel.text = supplier["supplierLevel"]

    # Edit Supplier
    def editSupplier(self, supplierName, business, contactNo, email, address, startDealing, supplierLevel):
        if confirm_box('Edit Supplier', 'Do you want to save changes ?') == 'yes':
            if delete_supplier(self.suppliers_id):
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

                if not validate_mobileNo(contactNo):
                    message_box('Error', 'Check the contact number')
                    return

                if not validate_date(startDealing):
                    message_box('Error', 'Invalid date format.')
                    return

                # Send data to suppliers.py
                edit_supplier(self.suppliers_id, supplierName, business, contactNo, email, address, startDealing,
                              supplierLevel)

                message_box('Success', 'Supplier modified successfully.')
            else:
                message_box('Error', 'Not saved !')
            self.suppliers_screen.populate_suppliers()
            self.suppliers_screen.dismiss_popup(self.popup)

    # Open Reports Popup Window
    def reports_popup(self):
        pass

    # Delete Supplier
    def deleteSupplier(self):
        if confirm_box('Delete Supplier', 'Do you want to delete supplier ?') == 'yes':
            if delete_supplier(self.suppliers_id):
                message_box('Success', 'Supplier deleted successfully.')
                self.suppliers_screen.populate_suppliers()
                self.suppliers_screen.dismiss_popup(self.popup)
            else:
                message_box('Error', 'Delete failed !')
        else:
            message_box('Error', 'Delete Canceled.')

    def dismiss_popup(self, instance):
        instance.dismiss()


# Suppliers Main UI (Accessed by main.py)
class SuppliersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_suppliers()

    # Button Click Event Handler
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add New Supplier':
            self.add_popup()

    def populate_suppliers(self):
        # Get the suppliers from the database
        suppliers = load_suppliers()

        # Clear the existing widgets in the ScrollView
        self.ids.Supplier_list.clear_widgets()

        # Headers
        headers = ['Business', 'Owner', 'Contact', 'Level']
        grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
        for header in headers:
            grid.add_widget(CButton(text=header, bold=True))
        self.ids.Supplier_list.add_widget(grid)
        for supplier in suppliers:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
            button = Button(text=supplier["business"],
                            on_release=partial(self.view_suppliers, supplier["id"]),
                            background_normal='', font_size='20sp',
                            background_color=(0.1, 0.1, 0.1, 0.0),
                            font_name='Roboto',
                            color=(1, 1, 1, 1),
                            bold=True)
            grid.supplier = supplier
            grid.add_widget(button)
            grid.add_widget(CLabel(text=supplier["supplierName"]))
            grid.add_widget(CLabel(text=supplier["contactNo"]))
            grid.add_widget(CLabel(text=supplier["supplierLevel"]))
            self.ids.Supplier_list.add_widget(grid)

    def view_suppliers(self, suppliers_id, instance):
        viewPop = CPopup(title='View Supplier', content=ViewSupPopup(self, suppliers_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    # Open to supplier add popup window
    def add_popup(self):
        addPop = CPopup(title='Add Supplier', content=AddSupPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    def dismiss_popup(self, instance):
        instance.dismiss()
