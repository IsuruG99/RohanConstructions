from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from functions.finances import *
from functions.projects import load_projects, load_project_names

from utils import *
from custom import *
from validation import *

import datetime


class AddLogPopup(GridLayout):
    def __init__(self, finances_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.finances_screen = finances_screen
        self.populate_projectNames()
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_projectNames(self) -> None:
        self.ids.addLog_project.values = []
        projects = load_projects()
        project_names = []
        for project in projects:
            project_names.append(project["name"])
        self.ids.addLog_project.values = project_names

    def addLog(self, requestType: str = "Submit") -> None:
        fin_type = str(self.ids.addLog_type.text)
        amount = str(self.ids.addLog_amount.text)
        date = str(self.ids.addLog_date.text)
        desc = str(self.ids.addLog_desc.text)
        entity = str(self.ids.addLog_entity.text)
        project = str(self.ids.addLog_project.text)
        category = str(self.ids.addLog_category.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(fin_type, amount, date, desc, entity, project, category):
                self.finances_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_date(date):
                self.finances_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            if fin_type != "Income" and fin_type != "Expense":
                self.finances_screen.CMessageBox('Error', 'Invalid type.', 'Message')
                return
            if category != "Materials" and category != "PayRoll" and category != "Contract" and category != "Misc":
                self.finances_screen.CMessageBox('Error', 'Invalid category.', 'Message')
                return
            if validate_currency(amount) is False:
                self.finances_screen.CMessageBox('Error', 'Invalid amount.', 'Message')
                return
            # Send data to finances.py
            self.finances_screen.CMessageBox('Update Finance Log', 'Are you sure you want to add this log?', 'Confirm',
                                             'Submit', 'Cancel', self.addLog)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                add_log(fin_type, amount, date, desc, entity, project, category)
                self.finances_screen.CMessageBox('Success', 'Log added successfully.', 'Message')
                self.finances_screen.populate_logs(load_all_finances(0))
                self.validCheck = 0
                self.finances_screen.ids.finances_filter.text = 'Filter: All'
                self.finances_screen.dismiss_popup(self.popup)

    def load_project_list(self) -> list:
        return load_project_names()


class ViewLogPopup(GridLayout):
    def __init__(self, finances_screen: Screen, fin_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.fin_id = fin_id
        self.populate_view()
        self.finances_screen = finances_screen
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    # Populate PopUp Window
    def populate_view(self) -> None:
        # Populate the project names Spinner
        self.ids.viewLog_project.values = []
        projects = load_projects(2)
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

    def edit_log(self, requestType: str = "Submit") -> None:
        fin_type = str(self.ids.viewLog_type.text)
        amount = str(self.ids.viewLog_amount.text)
        date = str(self.ids.viewLog_date.text)
        desc = str(self.ids.viewLog_desc.text)
        entity = str(self.ids.viewLog_entity.text)
        project = str(self.ids.viewLog_project.text)
        category = str(self.ids.viewLog_category.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(fin_type, amount, date, desc, entity, project, category):
                self.finances_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_date(date):
                self.finances_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            if fin_type != "Income" and fin_type != "Expense":
                self.finances_screen.CMessageBox('Error', 'Invalid type.', 'Message')
                return
            if category != "Materials" and category != "PayRoll" and category != "Contract" and category != "Misc":
                self.finances_screen.CMessageBox('Error', 'Invalid category.', 'Message')
                return
            # Send data to finances.py
            self.finances_screen.CMessageBox('Update Finance Log', 'Are you sure you want to edit this log?', 'Confirm',
                                             'Submit', 'Cancel', self.edit_log)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                if edit_log(self.fin_id, fin_type, amount, date, desc, entity, project, category,
                            App.get_running_app().get_accessName()):
                    self.finances_screen.CMessageBox('Success', 'Log edited successfully.', 'Message')
                    self.finances_screen.populate_logs(load_all_finances(0))
                    self.validCheck = 0
                    self.finances_screen.ids.finances_filter.text = 'Filter: All'
                    self.finances_screen.dismiss_popup(self.popup)
                else:
                    self.finances_screen.CMessageBox('Error', 'Failed to edit log.', 'Message')
                    self.validCheck = 0

    def load_project_list(self) -> list:
        return load_project_names()

    def delete_log(self, requestType: str = "Submit") -> None:
        if requestType == "Validate":
            self.finances_screen.CMessageBox('Delete Finance Log', 'Are you sure you want to delete this log?',
                                             'Confirm',
                                             'Submit', 'Cancel', self.delete_log)
        elif requestType == "Submit":
            if delete_log(self.fin_id):
                self.finances_screen.CMessageBox('Success', 'Log deleted successfully.', 'Message')
                self.finances_screen.populate_logs(load_all_finances(0))
                self.finances_screen.ids.finances_filter.text = 'Filter: All'
                self.finances_screen.dismiss_popup(self.popup)
            else:
                self.finances_screen.CMessageBox('Error', 'Failed to delete log.', 'Message')


# Financial Section Main UI (Opens this from main.py)
class FinancesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sort_logs("Date", load_all_finances(0), None)

    # Populate the ScrollView with the finances
    def populate_logs(self, financeList: list = load_all_finances(), headers: list = None) -> None:
        # Clear the existing widgets in the ScrollView
        self.ids.finances_list.clear_widgets()
        self.ids.finance_headers.clear_widgets()

        # Headers
        if headers is None:
            headers = ["Amount", "Category", "Date", "User"]
        # Dynamically regenerate headers, made for Sorting name changes
        size_hints = [0.3, 0.2, 0.3, 0.2]
        for header in headers:
            self.ids.finance_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_logs, header, financeList)))

        for log in financeList:
            if log["type"] == "Expense":
                # Readable Lighter Red
                cl = (1, 0.5, 0.5, 1)
            else:
                cl = (0.5, 1, 0.5, 1)

            grid = GridLayout(cols=4, size_hint_y=None, height=40)
            button = Button(text=convert_currency(log["amount"]), on_release=partial(self.view_log, log["id"]),
                            background_normal='', font_size='20sp', size_hint_x=0.3,
                            background_color=(0.1, 0.1, 0.1, 0.0), font_name='Roboto', color=cl, bold=True)
            grid.finance = log
            grid.add_widget(button)
            grid.add_widget(CLabel(text=log["category"], size_hint_x=0.2))
            grid.add_widget(CLabel(text=convert_date(log["date"]), size_hint_x=0.3))
            grid.add_widget(CLabel(text=log["user"], size_hint_x=0.2))
            self.ids.finances_list.add_widget(grid)

    def sort_logs(self, header: str, finances: list, instance) -> None:
        # Sort by header
        if header == "Amount" or header == "Amount [D]":
            finances = sorted(finances, key=lambda x: currencyStringToFloat(x["amount"]))
            self.populate_logs(finances, headers=['Amount [A]', 'Category', 'Date', 'User'])
        elif header == "Category" or header == "Category [D]":
            finances = sorted(finances, key=lambda x: x["category"])
            self.populate_logs(finances, headers=['Amount', 'Category [A]', 'Date', 'User'])
        elif header == "Date" or header == "Date [D]":
            finances = sorted(finances, key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'))
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date [A]', 'User'])
        elif header == "User" or header == "User [D]":
            finances = sorted(finances, key=lambda x: x["user"])
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date', 'User [A]'])
        elif header == "Amount [A]":
            finances = sorted(finances, key=lambda x: currencyStringToFloat(x["amount"]), reverse=True)
            self.populate_logs(finances, headers=['Amount [D]', 'Category', 'Date', 'User'])
        elif header == "Category [A]":
            finances = sorted(finances, key=lambda x: x["category"], reverse=True)
            self.populate_logs(finances, headers=['Amount', 'Category [D]', 'Date', 'User'])
        elif header == "Date [A]":
            finances = sorted(finances, key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'), reverse=True)
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date [D]', 'User'])
        elif header == "User [A]":
            finances = sorted(finances, key=lambda x: x["user"], reverse=True)
            self.populate_logs(finances, headers=['Amount', 'Category', 'Date', 'User [D]'])

    def searchLogs(self, searchValue: str) -> None:
        if not searchValue == '':
            searchValue = searchValue.lower()
            finances = load_all_finances()
            searchResults = []
            for log in finances:
                if (searchValue in log['project_name'].lower() or searchValue in str(log['amount']).lower() or
                        searchValue in log['date'].lower()):
                    searchResults.append(log)
            self.populate_logs(searchResults)

    def view_log(self, fin_id: str, instance) -> None:
        temp_viewPop_popup = Popup()
        viewPop_popup = ViewLogPopup(self, fin_id, temp_viewPop_popup)
        viewPop = RPopup(title='View Finance Log', content=viewPop_popup, size_hint=(0.45, 0.85))
        viewPop_popup.popup = viewPop
        viewPop.open()


    def overview_log(self) -> None:
        temp_overview_popup = Popup()
        overviewPop_popup = FinanceOverview(self, temp_overview_popup)
        overviewPop = RPopup(title='Finance Overview', content=overviewPop_popup, size_hint=(0.45, 0.85))
        overviewPop_popup.popup = overviewPop
        overviewPop.open()

    def add_log_popup(self) -> None:
        temp_addPop_popup = Popup()
        addPop_popup = AddLogPopup(self, temp_addPop_popup)
        addPop = RPopup(title='Add Finance Log', content=addPop_popup, size_hint=(0.45, 0.85))
        addPop_popup.popup = addPop
        addPop.open()

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'None',
                    btn1: str = 'Ok', btn2: str = 'Cancel', btn1click: str = None, btn2click: str = None) -> None:
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

    def btn_click(self, instance) -> None:
        if instance.text == 'Back':
            self.parent.current = 'main'
        elif instance.text == 'Add':
            self.add_log_popup()
        elif instance.text == 'Filter: All' or instance.text == 'Filter: Income' or instance.text == 'Filter: Expense':
            if self.ids.finances_filter.text == 'Filter: All':
                self.populate_logs(load_all_finances(1))
                self.ids.finances_filter.text = 'Filter: Income'
            elif self.ids.finances_filter.text == 'Filter: Income':
                self.populate_logs(load_all_finances(2))
                self.ids.finances_filter.text = 'Filter: Expense'
            elif self.ids.finances_filter.text == 'Filter: Expense':
                self.populate_logs(load_all_finances(0))
                self.ids.finances_filter.text = 'Filter: All'

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()


class FinanceOverview(GridLayout):
    def __init__(self, finance_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.finance_screen = finance_screen
        year = str(datetime.datetime.now().year)
        month = str(convert_monthToNumber(convert_numberToMonth(datetime.datetime.now().month)))
        self.populate_overview(year, month)
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_overview(self, y: str, m: str) -> None:
        if y == '' or None:
            self.finance_screen.CMessageBox('Error', 'Year is required.', 'Message')
            return

        finances = load_all_finances(0)
        total_income = 0
        total_expense = 0
        if m == '':
            m = '00'
        else:
            m = str(convert_monthToNumber(m))
        for finance in finances:
            # Date is stored as 'YYYY-MM-DD', it is a string, and we need to extract year and month
            # 2 conditions, year and month, year only (which means all months)
            if finance['date'][:4] == y and finance['date'][5:7] == m:
                if finance['type'] == 'Income':
                    total_income += currencyStringToFloat(finance['amount'])
                else:
                    total_expense += currencyStringToFloat(finance['amount'])
            elif finance['date'][:4] == y and m == '00':
                if finance['type'] == 'Income':
                    total_income += currencyStringToFloat(finance['amount'])
                else:
                    total_expense += currencyStringToFloat(finance['amount'])

        self.ids.overview_income.text = convert_currency(total_income)
        self.ids.overview_expense.text = convert_currency(total_expense)
        self.ids.overview_balance.text = convert_currency(total_income - total_expense)

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()
