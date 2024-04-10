from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from functions.finances import *
from functions.projects import load_projects
from utils import *
from custom import *
import datetime


class AddLogPopup(GridLayout):
    def __init__(self, finances_screen, **kwargs):
        super().__init__(**kwargs)
        self.finances_screen = finances_screen
        self.populate_projectNames()

    def populate_projectNames(self):
        self.ids.addLog_project.values = []
        projects = load_projects()
        project_names = []
        for project in projects:
            project_names.append(project["name"])
        self.ids.addLog_project.values = project_names

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
        self.finances_screen.populate_logs(load_all_finances(0))
        self.finances_screen.ids.finances_filter.text = 'All'
        self.finances_screen.dismiss_popup(self.popup)


class ViewLogPopup(GridLayout):
    def __init__(self, finances_screen, fin_id, **kwargs):
        super().__init__(**kwargs)
        self.fin_id = fin_id
        self.populate_view()
        self.finances_screen = finances_screen

    # Populate PopUp Window
    def populate_view(self):
        # Populate the project names Spinner
        self.ids.viewLog_project.values = []
        projects = load_projects()
        project_names = []
        for project in projects:
            project_names.append(project["name"])
        self.ids.viewLog_project.values = project_names

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
        if confirm_box('Edit', 'Are you sure you want to edit this log?') == 'yes':
            if edit_log(self.fin_id, fin_type, amount, date, desc, entity, project, category):
                message_box('Success', 'Log edited successfully.')
                self.finances_screen.populate_logs(load_all_finances(0))
                self.finances_screen.ids.finances_filter.text = 'All'
                self.finances_screen.dismiss_popup(self.popup)
            else:
                message_box('Error', 'Failed to edit log.')

    def delete_log(self):
        if confirm_box('Delete', 'Are you sure you want to delete this log?') == 'yes':
            if delete_log(self.fin_id):
                message_box('Success', 'Log deleted successfully.')
                self.finances_screen.populate_logs(load_all_finances(0))
                self.finances_screen.ids.finances_filter.text = 'All'
                self.finances_screen.dismiss_popup(self.popup)
            else:
                message_box('Error', 'Failed to delete log.')
                self.finances_screen.dismiss_popup(self.popup)


# Financial Section Main UI (Opens this from main.py)
class FinancesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_logs()

    # Populate the ScrollView with the finances
    def populate_logs(self, financeList=load_all_finances(), headers=None):
        # Clear the existing widgets in the ScrollView
        self.ids.finances_list.clear_widgets()
        self.ids.finance_headers.clear_widgets()

        # Headers
        if headers is None:
            headers = ["Amount", "Category", "Date"]
        # Dynamically regenerate headers, made for Sorting name changes
        for header in headers:
            self.ids.finance_headers.add_widget(CButton(text=header, bold=True, padding=(10, 10),
                                                        on_release=partial(self.sort_logs, header, financeList)))

        for log in financeList:
            if log["type"] == "Expense":
                # Readable Lighter Red
                cl = (1, 0.5, 0.5, 1)
            else:
                cl = (0.5, 1, 0.5, 1)

            grid = GridLayout(cols=4, size_hint_y=None, height=50)
            button = Button(text=convert_currency(log["amount"]), on_release=partial(self.view_log, log["id"]),
                            background_normal='', font_size='20sp',
                            background_color=(0.1, 0.1, 0.1, 0.0), font_name='Roboto', color=cl, bold=True)
            grid.finance = log
            grid.add_widget(button)
            grid.add_widget(CLabel(text=log["category"]))
            grid.add_widget(CLabel(text=convert_date(log["date"])))
            self.ids.finances_list.add_widget(grid)

    def sort_logs(self, header, finances, instance):
        # Sort by header
        if header == "Amount" or header == "Amount [D]":
            finances = sorted(finances, key=lambda x: currencyStringToFloat(x["amount"]))
            self.populate_logs(finances, headers=['Amount [A]', 'Category', 'Date'])

        elif header == "Category" or header == "Category [D]":
            finances = sorted(finances, key=lambda x: x["category"])
            self.populate_logs(finances, headers=['Amount', 'Category [A]', 'Date'])
        elif header == "Date" or header == "Date [D]":
            finances = sorted(finances, key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'))
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date [A]'])
        elif header == "Amount [A]":
            finances = sorted(finances, key=lambda x: currencyStringToFloat(x["amount"]), reverse=True)
            self.populate_logs(finances, headers=['Amount [D]', 'Category', 'Date'])
        elif header == "Category [A]":
            finances = sorted(finances, key=lambda x: x["category"], reverse=True)
            self.populate_logs(finances, headers=['Amount', 'Category [D]', 'Date'])
        elif header == "Date [A]":
            finances = sorted(finances, key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'), reverse=True)
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date [D]'])

    def searchLogs(self, searchValue):
        if not searchValue == '':
            searchValue = searchValue.lower()
            finances = load_all_finances()
            searchResults = []
            for log in finances:
                if (searchValue in log['project_name'].lower() or searchValue in str(log['amount']).lower() or
                        searchValue in log['date'].lower()):
                    searchResults.append(log)
            self.populate_logs(searchResults)

    def view_log(self, fin_id, instance):
        # Message Box to display the finance id
        viewPop = CPopup(title='View Finance Log', content=ViewLogPopup(self, fin_id), size_hint=(0.5, 0.8))
        viewPop.open()
        viewPop.content.popup = viewPop

    def add_log_popup(self):
        addPop = CPopup(title='Add Finance Log', content=AddLogPopup(self), size_hint=(0.5, 0.8))
        addPop.open()
        addPop.content.popup = addPop

    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add':
            self.add_log_popup()
        elif instance.text == 'All' or instance.text == 'Income' or instance.text == 'Expense':
            if self.ids.finances_filter.text == 'All':
                self.populate_logs(load_all_finances(1))
                self.ids.finances_filter.text = 'Income'
            elif self.ids.finances_filter.text == 'Income':
                self.populate_logs(load_all_finances(2))
                self.ids.finances_filter.text = 'Expense'
            elif self.ids.finances_filter.text == 'Expense':
                self.populate_logs(load_all_finances(0))
                self.ids.finances_filter.text = 'All'

    def dismiss_popup(self, instance):
        instance.dismiss()
