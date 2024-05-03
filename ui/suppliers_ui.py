from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from functions.resources import load_resources
from functions.suppliers import *
from functools import partial

from pieChart import PieChart
from utils import *
from custom import *
from validation import *


class AddSupPopup(GridLayout):
    def __init__(self, suppliers_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.suppliers_screen = suppliers_screen
        self.popup = popup
        self.validCheck = 0
        self.cols = 1
        self.rows = 1

    def add_Supplier(self, requestType: str = "Submit") -> None:
        supplierName = str(self.ids.supplierName.text)
        business = str(self.ids.business.text)
        contactNo = str(self.ids.contactNo.text)
        email = str(self.ids.email.text)
        address = str(self.ids.address.text)
        startDealing = str(self.ids.startDealing.text)
        supplierLevel = str(self.ids.supplierLevel.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(supplierName, contactNo, email, address):
                self.suppliers_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return

            if not validate_mobileNo(contactNo):
                self.suppliers_screen.CMessageBox('Error', 'Invalid contact number.', 'Message')
                return

            if not validate_date(startDealing):
                self.suppliers_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            # Ask confirm
            self.suppliers_screen.CMessageBox('Add Supplier', 'Do you want to add supplier ?', 'Confirm', 'Yes', 'No',
                                              self.add_Supplier)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                # Send data to supplier.py
                add_supplier(supplierName, business, contactNo, email, address, startDealing, supplierLevel)
                self.suppliers_screen.CMessageBox('Success', 'Supplier added successfully.', 'Message')
                self.validCheck = 0
                self.suppliers_screen.populate_suppliers(load_suppliers())

    def dismiss_popup(self, instance) -> None:
        self.suppliers_screen.dismiss_popup(self.popup)


class ViewSupPopup(GridLayout):
    def __init__(self, suppliers_screen: Screen, suppliers_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.suppliers_id = suppliers_id
        self.populate_view()
        self.popup = popup
        self.suppliers_screen = suppliers_screen
        self.validCheck = 0
        self.cols = 1
        self.rows = 1

    # Populate PopUp Window
    def populate_view(self) -> None:
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
    def editSupplier(self, requestType: str = "Submit") -> None:
        # Stringify inputs (Including Dates)
        supplierName = str(self.ids.supplierName.text)
        business = str(self.ids.business.text)
        email = str(self.ids.email.text)
        contactNo = str(self.ids.contactNo.text)
        startDealing = str(self.ids.startDealing.text)
        supplierLevel = str(self.ids.supplierLevel.text)
        address = str(self.ids.address.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(supplierName, business, contactNo, email, address, startDealing, supplierLevel):
                self.suppliers_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return

            if not validate_mobileNo(contactNo):
                self.suppliers_screen.CMessageBox('Error', 'Invalid contact number.', 'Message')
                return

            if not validate_date(startDealing):
                self.suppliers_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            self.suppliers_screen.CMessageBox('Edit Supplier', 'Do you want to save changes ?', 'Confirm', 'Yes',
                                              'No', self.editSupplier)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                # Send data to suppliers.py
                if edit_supplier(self.suppliers_id, supplierName, business, contactNo, email, address, startDealing,
                                 supplierLevel):
                    self.suppliers_screen.CMessageBox('Success', 'Supplier edited successfully.', 'Message')
                else:
                    self.suppliers_screen.CMessageBox('Error', 'Edit failed !')
                self.validCheck = 0
                self.suppliers_screen.populate_suppliers(load_suppliers())
                self.suppliers_screen.dismiss_popup(self.popup)

    # Delete Supplier
    def deleteSupplier(self, requestType: str = "Submit") -> None:
        if requestType == "Validate":
            self.suppliers_screen.CMessageBox('Confirm', 'Do you want to delete supplier ?', 'Confirm', 'Yes', 'No',
                                              self.deleteSupplier)
        elif requestType == "Submit":
            if delete_supplier(self.suppliers_id):
                self.suppliers_screen.CMessageBox('Success', 'Supplier deleted successfully.', 'Message')
                self.suppliers_screen.populate_suppliers(load_suppliers())
                self.validCheck = 0
                self.suppliers_screen.dismiss_popup(self.popup)
            else:
                self.suppliers_screen.CMessageBox('Error', 'Delete failed !')
            self.validCheck = 0

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()


class ReportSupPopup(GridLayout):
    def __init__(self, suppliers_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.suppliers_screen = suppliers_screen
        self.popup = popup
        self.populate_supplierOverview()
        self.cols = 1
        self.rows = 1

    def populate_supplierOverview(self, supplierName: str = None) -> None:
        self.ids.reportSupplier_headers.clear_widgets()
        self.ids.reportSupplier_resList.clear_widgets()
        self.ids.reportSupplier_pieChart.clear_widgets()

        suppliers: list = load_suppliers()
        res: list = load_resources()
        resList: list = []

        self.ids.reportSupplier_supplierCount.text = "Total Suppliers : " + str(len(suppliers))
        self.ids.reportSupplier_resCount.text = "Total Resource Types : " + str(len(res))

        headers = GridLayout(cols=2, size_hint_y=None, height=40)
        headers.add_widget(CLabel(text='Resource', bold=True))
        headers.add_widget(CLabel(text='Quantity', bold=True))
        self.ids.reportSupplier_headers.add_widget(headers)
        if supplierName is not None:

            for resource in res:
                grid = GridLayout(cols=2, size_hint_y=None, height=40)
                if resource["supplier_name"] == supplierName:
                    grid.add_widget(CLabel(text=resource["name"]))
                    grid.add_widget(CLabel(text=str(resource["quantity"])))
                    resList.append({"name": resource["name"], "status": resource["status"]})
                    self.ids.reportSupplier_resList.add_widget(grid)
            self.populate_pieChart(resList)

    def populate_pieChart(self, resList: list) -> None:
        if resList is None or len(resList) == 0:
            data = {"No Data": 1}
        else:
            data = {"In Stock": 0, "Out of Stock": 0}
            for res in resList:
                if res["status"] == "In Stock":
                    data["In Stock"] += 1
                else:
                    data["Out of Stock"] += 1

        grid = GridLayout(cols=1, size_hint_y=None, height=200)
        chart = PieChart(data=data, position=(1, 1),
                         size=(150, 150), legend_enable=True)
        grid.add_widget(chart)
        self.ids.reportSupplier_pieChart.add_widget(grid)


    def load_suppliers(self) -> None:
        return load_supplier_names()

    def dismiss_popup(self, instance) -> None:
        self.suppliers_screen.dismiss_popup(instance)


# Suppliers Main UI (Accessed by main.py)
class SuppliersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_suppliers(load_suppliers())

    def populate_suppliers(self, suppliers: list = load_suppliers(), headers: list = None) -> None:
        # Clear the existing widgets in the ScrollView & Headers
        self.ids.Supplier_list.clear_widgets()
        self.ids.Supplier_headers.clear_widgets()

        # Header Default Set
        if headers is None:
            headers = ['Business', 'Owner', 'Contact', 'Level']
        # Fill header list (Made to rewrite [A] [D] Sorting Header custom names in sorting)
        size_hints = [4, 3, 2, 1]
        for header in headers:
            self.ids.Supplier_headers.add_widget(CButton(text=header,
                                                         bold=True,
                                                         padding=(10, 10),
                                                         size_hint_x=size_hints[headers.index(header)],
                                                         on_release=partial(self.sort_suppliers, suppliers, header)))

        # Fill the grid with Supplier Data
        for supplier in suppliers:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            button = Button(text=supplier["business"],
                            on_release=partial(self.view_suppliers, supplier["id"]),
                            background_normal='', font_size='20sp',
                            background_color=(0.1, 0.1, 0.1, 0.0),
                            font_name='Roboto', size_hint_x=4,
                            color=(1, 1, 1, 1),
                            bold=True)
            grid.supplier = supplier
            grid.add_widget(button)
            grid.add_widget(CLabel(text=supplier["supplierName"], size_hint_x=3))
            grid.add_widget(CLabel(text=supplier["contactNo"], size_hint_x=2))
            grid.add_widget(CLabel(text=supplier["supplierLevel"], size_hint_x=1))
            self.ids.Supplier_list.add_widget(grid)

    # Main Sorting Function, take header list, supplier list, call populate function with sorted supplier list
    def sort_suppliers(self, suppliers: list, header: str, instance) -> None:
        if header == 'Business' or header == 'Business [D]':
            suppliers = sorted(suppliers, key=lambda x: x['business'])
            self.populate_suppliers(suppliers, headers=['Business [A]', 'Owner', 'Contact', 'Level'])
        elif header == 'Owner' or header == 'Owner [D]':
            suppliers = sorted(suppliers, key=lambda x: x['supplierName'])
            self.populate_suppliers(suppliers, headers=['Business', 'Owner [A]', 'Contact', 'Level'])
        elif header == 'Level' or header == 'Level [D]':
            suppliers = sorted(suppliers, key=lambda x: str(x['supplierLevel']))
            self.populate_suppliers(suppliers, headers=['Business', 'Owner', 'Contact', 'Level [A]'])
        elif header == 'Business [A]':
            suppliers = sorted(suppliers, key=lambda x: x['business'], reverse=True)
            self.populate_suppliers(suppliers, headers=['Business [D]', 'Owner', 'Contact', 'Level'])
        elif header == 'Owner [A]':
            suppliers = sorted(suppliers, key=lambda x: x['supplierName'], reverse=True)
            self.populate_suppliers(suppliers, headers=['Business', 'Owner [D]', 'Contact', 'Level'])
        elif header == 'Level [A]':
            suppliers = sorted(suppliers, key=lambda x: str(x['supplierLevel']), reverse=True)
            self.populate_suppliers(suppliers, headers=['Business', 'Owner', 'Contact', 'Level [D]'])

    # Search Function, take search text, call populate function with filtered supplier list
    def searchSuppliers(self, search_text: str) -> None:
        search_text = search_text.lower()
        suppliers = load_suppliers()
        suppliers = [supplier for supplier in suppliers if
                     search_text in supplier['business'].lower() or
                     search_text in supplier['supplierName'].lower() or
                     search_text in supplier['contactNo'].lower() or
                     search_text in supplier['email'].lower() or
                     search_text in supplier['startDealing'].lower()]
        self.populate_suppliers(suppliers)

    def view_suppliers(self, suppliers_id: str, instance) -> None:
        temp_viewPop_popup = Popup()
        viewPop_popup = ViewSupPopup(self, suppliers_id, temp_viewPop_popup)
        viewPop = RPopup(title='View Supplier', content=viewPop_popup, size_hint=(0.45, 0.8))
        viewPop_popup.popup = viewPop
        viewPop.open()

    def overview_suppliers(self):
        temp_overview_popup = Popup()
        overviewPop_popup = ReportSupPopup(self, temp_overview_popup)
        overviewPop = RPopup(title='Supplier Overview', content=overviewPop_popup, size_hint=(0.6, 0.95))
        overviewPop_popup.popup = overviewPop
        overviewPop.open()

    # Open to supplier add popup window
    def add_popup(self) -> None:
        temp_addPop_popup = Popup()
        addPop_popup = AddSupPopup(self, temp_addPop_popup)
        addPop = RPopup(title='Add Supplier', content=addPop_popup, size_hint=(0.45, 0.8))
        addPop_popup.popup = addPop
        addPop.open()

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'None',
                    btn1: str = 'Ok', btn2: str = 'Cancel', btn1click=None, btn2click=None) -> None:
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

    # Button Click Event Handler
    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == 'Back':
            self.parent.current = 'main'
        elif txt == 'Add New Supplier':
            self.add_popup()
        # Categorization, All, Level 1, Level 2, Level 3, each calls populate function to regenerate data
        elif txt == 'Filter: All' or txt == 'Filter: Level 1' or txt == 'Filter: Level 2' or txt == 'Filter: Level 3':
            if txt == 'Filter: All':
                self.populate_suppliers(load_suppliers(1))
                self.ids.supplierFilter.text = 'Filter: Level 1'
                self.ids.search.text = ''
            elif txt == 'Filter: Level 1':
                self.populate_suppliers(load_suppliers(2))
                self.ids.supplierFilter.text = 'Filter: Level 2'
                self.ids.search.text = ''
            elif txt == 'Filter: Level 2':
                self.populate_suppliers(load_suppliers(3))
                self.ids.supplierFilter.text = 'Filter: Level 3'
                self.ids.search.text = ''
            elif txt == 'Filter: Level 3':
                self.populate_suppliers(load_suppliers(0))
                self.ids.supplierFilter.text = 'Filter: All'
                self.ids.search.text = ''

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()
