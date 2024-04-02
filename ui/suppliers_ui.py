from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.suppliers import *
from functools import partial

from utils import *


class AddPopup(GridLayout):
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
        if contactNo_unique_check('add', contactNo) is False:
            message_box('Error', 'Check your contact number.')
            return

    # Send data to supplier.py
        add_supplier(supplierName, business, contactNo, email, address, startDealing, supplierLevel, "In Progress")
        message_box('Success', 'New supplier added successfully.')
        self.suppliers_screen.populate_supplierss(0)

    def dismiss_popup(self, instance):
        instance.dismiss()


# Suppliers Main UI (Accessed by main.py)
class SuppliersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Button Click Event Handler
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'

        elif instance.text == 'Add New Supplier':
            self.add_popup()

    # Open to supplier add popup window
    def add_popup(self):
        addPop = Popup(title='Add Supplier', content=AddPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop