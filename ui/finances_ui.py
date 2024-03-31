from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from functions.finances import *
from utils import *


class AddLogPopup(GridLayout):
    def __init__(self, finances_screen, **kwargs):
        super().__init__(**kwargs)
        self.finances_screen = finances_screen

    def addLog(self, fin_type, amount, date, desc, entity, project, category):
        fin_type = str(fin_type)
        amount = str(amount)
        date = str(date)
        desc = str(desc)
        entity = str(entity)
        project = str(project)
        category = str(category)
        # Validate inputs
        if not validate_string(fin_type, amount, date, desc, entity, project, category):
            message_box('Error', 'All fields are required.')
            return
        if not validate_date(date):
            message_box('Error', 'Invalid date format.')
            return
        if fin_type != "Income" and fin_type != "Expense":
            message_box('Error', 'Invalid type.')
            return
        if category != "Materials" and category != "PayRoll" and category != "Contract" and category != "Misc":
            message_box('Error', 'Invalid category.')
            return
        if validate_currency(amount) is False:
            message_box('Error', 'Invalid amount.')
            return
        # Send data to finances.py
        add_log(fin_type, amount, date, desc, entity, project, category)
        message_box('Success', 'Log added successfully.')
        self.finances_screen.populate_logs(0)

    def dismiss_popup(self, instance):
        instance.dismiss()


class ViewLogPopup(GridLayout):
    def __init__(self, finances_screen, fin_id, **kwargs):
        super().__init__(**kwargs)
        self.fin_id = fin_id
        self.populate_view()
        self.finances_screen = finances_screen

    # Populate PopUp Window
    def populate_view(self):
        # Get the finance log data from the DB
        log = get_log(self.fin_id)
        # Assign type, amount, date, description, related_entity, project_name, category
        self.ids.viewLog_type.text = log["type"]
        self.ids.viewLog_amount.text = log["amount"]
        self.ids.viewLog_date.text = str(log["date"])
        self.ids.viewLog_desc.text = log["description"]
        self.ids.viewLog_entity.text = log["related_entity"]
        self.ids.viewLog_project.text = log["project_name"]
        self.ids.viewLog_category.text = log["category"]


    def edit_log(self, fin_type, amount, date, desc, entity, project, category):
        fin_type = str(fin_type)
        amount = str(amount)
        date = str(date)
        desc = str(desc)
        entity = str(entity)
        project = str(project)
        category = str(category)
        # Validate inputs
        if not validate_string(fin_type, amount, date, desc, entity, project, category):
            message_box('Error', 'All fields are required.')
            return
        if not validate_date(date):
            message_box('Error', 'Invalid date format.')
            return
        if fin_type != "Income" and fin_type != "Expense":
            message_box('Error', 'Invalid type.')
            return
        if category != "Materials" and category != "PayRoll" and category != "Contract" and category != "Misc":
            message_box('Error', 'Invalid category.')
            return
        # Send data to finances.py
        edit_log(self.fin_id, fin_type, amount, date, desc, entity, project, category)
        message_box('Success', 'Log edited successfully.')
        self.finances_screen.populate_logs(0)


    def delete_log(self):
        if confirm_box('Delete', 'Are you sure you want to delete this log?') == 'yes':
            if delete_log(self.fin_id):
                message_box('Success', 'Log deleted successfully.')
                self.finances_screen.populate_logs(0)
                self.dismiss_popup(self.popup)
            else:
                message_box('Error', 'Failed to delete log.')
                self.dismiss_popup(self.popup)

    def dismiss_popup(self, instance):
        instance.dismiss()


# Manpower Main UI (Opens this from main.py)
class FinancesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_logs(0)

    # Button Click goes back to Main UI
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'

    # Populate the ScrollView with the finances
    def populate_logs(self, status):
        # Get the finances from the database
        financeList = load_all_finances()

        # Clear the existing widgets in the ScrollView
        self.ids.finances_list.clear_widgets()

        if status == 0:
            for log in financeList:
                if log["type"] == "Expense":
                    # Readable Lighter Red
                    cl = (1, 0.5, 0.5, 1)
                else:
                    cl = (0.5, 1, 0.5, 1)
                grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=50)
                button = Button(text=convert_currency(log["amount"]), on_release=partial(self.view_log, log["id"]),
                                background_normal='',
                                background_color=(1, 1, 1, 0), font_name='Roboto', color=cl, bold=True)
                grid.finance = log
                grid.add_widget(button)
                grid.add_widget(Label(text=log["category"]))
                grid.add_widget(Label(text=convert_date(log["date"])))
                self.ids.finances_list.add_widget(grid)

    def view_log(self, fin_id, instance):
        # Message Box to display the finance id
        viewPop = Popup(title='View Finance Log', content=ViewLogPopup(self, fin_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    def add_log_popup(self):
        addPop = Popup(title='Add Finance Log', content=AddLogPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add':
            self.add_log_popup()
        elif instance.text == 'Filter':
            message_box('Filter', 'Filtering by Expense')


