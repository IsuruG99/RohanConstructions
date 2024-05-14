from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from functions.clients import *
from functions.projects import load_project_names
from functools import partial
from kivy.uix.screenmanager import Screen

from functions.projects import load_projects

from custom import *
from pieChart import PieChart
from utils import *
from validation import *


# Manages user access to most functions. (Implemented by project leader)
def AccessControl(func):
    def wrapper(self, *args, **kwargs):
        # function validate_access in validation.py takes function's name (string) and returns True/False
        from kivy.app import App
        if App.get_running_app().get_accessLV() is not None:
            accessLV = App.get_running_app().get_accessLV()
            blockList = []
            if accessLV in [2,3]:
                blockList = ['add_client_popup', 'edit_client', 'delete_client']
                # If lv3 add 'reports_clients'
                if accessLV == 3:
                    blockList.append('report_clients')
            if validate_access(accessLV, func.__name__, blockList):
                return func(self, *args, **kwargs)
            else:
                try:
                    self.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
                except AttributeError:
                    self.clients_screen.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
    return wrapper


# add a popup window to insert client data to the database
class AddClientPopup(GridLayout):
    def __init__(self, clients_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.clients_screen = clients_screen
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def add_client(self, requestType: str = "Submit") -> None:
        # add_client_name.text, add_client_phone_number.text, add_client_email.text, add_client_address.text
        try:
            name = str(self.ids.add_client_name.text)
            phone_number = str(self.ids.add_client_phone_number.text)
            email = str(self.ids.add_client_email.text)
            address = str(self.ids.add_client_address.text)
        except AttributeError:
            return
        except ValueError:
            self.clients_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        # Validate and Confirm First, then recursively call Submit
        if requestType == "Validate":
            if not validate_string(name, phone_number, email, address):
                self.clients_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_mobileNo(phone_number):
                self.clients_screen.CMessageBox('Error', 'Invalid phone number.', 'Message')
                return
            if not validate_email(email):
                self.clients_screen.CMessageBox('Error', 'Invalid email address.', 'Message')
                return
            self.clients_screen.CMessageBox('Confirm', 'Are you sure you want to add this client?', 'Confirm', 'Yes',
                                            'No', self.add_client)
            self.validCheck = 1
        # Send the data to clients.py
        elif requestType == "Submit":
            if self.validCheck == 1:
                if add_client(name, phone_number, email, address):
                    self.clients_screen.CMessageBox('Success', 'Client added successfully.', 'Message')
                    self.clients_screen.populate_clients(load_clients(0))
                    self.validCheck = 0
                    self.dismiss_popup(self.popup)
                else:
                    self.clients_screen.CMessageBox('Error', 'Failed to add client.', 'Message')
                    self.validCheck = 0

    def load_project_list(self) -> list:
        return load_project_names()

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


# view clients via popup window
class ViewClientPopup(GridLayout):
    def __init__(self, clients_screen: Screen, client_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.clients_screen = clients_screen
        self.populate_view()
        self.validCheck = 0
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_view(self) -> None:
        # Get the client data from the database
        client = get_client(self.client_id)
        # Populate View
        self.ids.view_client_name.text = client['name']
        self.ids.view_client_phone_number.text = str(client['phone_number'])
        self.ids.view_client_email.text = client['email']
        self.ids.view_client_address.text = client['address']

    @AccessControl
    def edit_client(self, requestType: str = "Submit") -> None:
        # Get the data from the text inputs
        try:
            name = str(self.ids.view_client_name.text)
            phone_number = str(self.ids.view_client_phone_number.text)
            email = str(self.ids.view_client_email.text)
            address = str(self.ids.view_client_address.text)
        except (AttributeError, ValueError):
            self.clients_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        # Validate and Confirm First, then recursively call Submit
        if requestType == "Validate":
            if not all([validate_string(name, phone_number, email, address),
                        validate_mobileNo(phone_number),
                        validate_email(email)]):
                self.clients_screen.CMessageBox('Error', 'Invalid input.', 'Message')
                return
            self.clients_screen.CMessageBox('Update Client', 'Are you sure you want to save changes?', 'Confirm', 'Yes',
                                            'No', self.edit_client)
            self.validCheck = 1

        # Send the data to clients.py
        elif requestType == "Submit" and self.validCheck == 1:
            if update_client(self.client_id, name, phone_number, email, address):
                self.clients_screen.CMessageBox('Success', 'Client updated successfully.', 'Message')
                self.clients_screen.populate_clients(load_clients(0))
                self.validCheck = 0
                self.dismiss_popup(self.popup)
            else:
                self.clients_screen.CMessageBox('Error', 'Failed to update client.', 'Message')
                self.validCheck = 0

    @AccessControl
    def delete_client(self, requestType: str = "Submit") -> None:
        # Validate and Confirm First, then recursively call Submit
        if requestType == "Validate":
            self.clients_screen.CMessageBox('Delete Client', 'Are you sure you want to delete this client?', 'Confirm', 'Yes',
                                            'No', self.delete_client)
        # Send the data to clients.py
        elif requestType == "Submit" and delete_client(self.client_id):
            self.clients_screen.CMessageBox('Success', 'Client deleted successfully.', 'Message')
            self.clients_screen.populate_clients(load_clients(0))
            self.dismiss_popup(self.popup)
        else:
            self.clients_screen.CMessageBox('Error', 'Failed to delete client.', 'Message')

    def dismiss_popup(self, instance) -> None:
        self.popup.dismiss()


# below is client's main ui
class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_clients()
        self.add_client_popup_instance = None

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()

    # Open Message/Confirm Popup Window (Custom Widget implemented by Project Leader)
    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'Message',
                    btn1: str = 'OK', btn2: str = 'Cancel', btn1click=None, btn2click=None) -> None:
        if context == 'Message':
            msg_popup = MsgPopUp(self, content, context, btn1, btn1click)
            popup = RPopup(title=title, content=msg_popup, size_hint=(0.35, 0.3))
            msg_popup.popup = popup
            popup.open()
        elif context == 'Confirm':
            cfm_popup = CfmPopUp(self, content, context, btn1, btn2, btn1click, btn2click)
            popup = RPopup(title=title, content=cfm_popup, size_hint=(0.35, 0.3))
            cfm_popup.popup = popup
            popup.open()

    def populate_clients(self, clients: list = load_clients(0), headers: list = None) -> None:
        # Clear the existing clients
        self.ids.clients_list.clear_widgets()
        self.ids.clients_headers.clear_widgets()

        # Headers
        if headers is None:
            headers = ['Name', 'Phone Number', 'Email']
        size_hints = [0.5, 0.2, 0.3]
        for header in headers:
            self.ids.clients_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_clients, clients, header)))

        # Add the clients to the ScrollView # Only name, phone_number and email are shown
        for client in clients:
            grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=40)
            grid.client = client
            grid.add_widget(Button(text=client['name'], on_release=partial(self.view_client, client['id']),
                                   size_hint_x=0.5, background_normal='', font_name='Roboto',
                                   background_color=(0.1, 0.1, 0.1, 0), font_size='20sp', bold=True))
            grid.add_widget(CLabel(text=client['phone_number'], size_hint_x=0.2))
            grid.add_widget(CLabel(text=client['email'], size_hint_x=0.3))
            self.ids.clients_list.add_widget(grid)

    # Sorts Table Headers like a Table Column (It is not actually a Table but a ScrollView)
    # Clients Sorting Function, takes headers, clients List and calls populate function with sorted clients list
    def sort_clients(self, clients: list, header: str, instance) -> None:
        if header == 'Name' or header == 'Name [D]':
            clients = sorted(clients, key=lambda x: x['name'])
            self.populate_clients(clients, ['Name [A]', 'Phone Number', 'Email'])
        elif header == 'Name [A]':
            clients = sorted(clients, key=lambda x: x['name'], reverse=True)
            self.populate_clients(clients, ['Name [D]', 'Phone Number', 'Email'])
        elif header == 'Phone Number' or header == 'Phone Number [D]':
            clients = sorted(clients, key=lambda x: str(x['phone_number']))
            self.populate_clients(clients, ['Name', 'Phone Number [A]', 'Email'])
        elif header == 'Phone Number [A]':
            clients = sorted(clients, key=lambda x: str(x['phone_number']), reverse=True)
            self.populate_clients(clients, ['Name', 'Phone Number [D]', 'Email'])
        elif header == 'Email' or header == 'Email [D]':
            clients = sorted(clients, key=lambda x: x['email'])
            self.populate_clients(clients, ['Name', 'Phone Number', 'Email [A]'])
        elif header == 'Email [A]':
            clients = sorted(clients, key=lambda x: x['email'], reverse=True)
            self.populate_clients(clients, ['Name', 'Phone Number', 'Email [D]'])

    def search_clients(self, searchValue: str) -> None:  # Finish this function
        if not searchValue == '':
            clients = load_clients(0)
            clients = [client for client in clients
                       if searchValue.lower() in client['name'].lower()
                       or searchValue.lower() in client['phone_number'].lower()
                       or searchValue.lower() in client['email'].lower()]
            self.populate_clients(clients)

    @AccessControl
    def add_client_popup(self) -> None:
        temp_addClient_popup = Popup()
        addClient_popup = AddClientPopup(self, temp_addClient_popup)
        add_client_popup = RPopup(title='Add Client', content=addClient_popup, size_hint=(0.4, 0.65))
        addClient_popup.popup = add_client_popup
        add_client_popup.open()

    def view_client(self, client_id: str, instance) -> None:
        temp_viewPopup = Popup()
        viewPopup = ViewClientPopup(self, client_id, temp_viewPopup)
        view_popup = RPopup(title='View Client', content=viewPopup, size_hint=(0.4, 0.65))
        viewPopup.popup = view_popup
        view_popup.open()

    @AccessControl
    def report_clients(self) -> None:
        temp_reportPopup = Popup()
        reportPopup = ClientsReport(self, temp_reportPopup)
        report_popup = RPopup(title='Clients Report', content=reportPopup, size_hint=(0.6, 0.95))
        reportPopup.popup = report_popup
        report_popup.open()

    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == 'Add':
            self.add_client_popup()
        elif txt == 'Back':
            self.parent.current = 'main'
        elif txt == 'Refresh':
            self.populate_clients(load_clients(0))
            self.ids.search.text = ''
        elif txt == 'Overview':
            self.report_clients()


class ClientsReport(GridLayout):
    def __init__(self, clients_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.clients_screen = clients_screen
        year = str(datetime.datetime.now().year)
        month = str(convert_monthToNumber(convert_numberToMonth(datetime.datetime.now().month)))
        self.populate_clientOverview(year, month)
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_clientOverview(self, y: str, m: str) -> None:
        if not y:
            self.finance_screen.CMessageBox('Error', 'Year is required.', 'Message')
            return

        m = '00' if not m else str(convert_monthToNumber(m))
        clients = load_clients(0)
        projects = load_projects()

        current_clients, current_projects, complete_projects = [], [], []
        profit = 0

        for project in projects:
            if (project['start_date'][:7] <= y + '-' + m <= project['end_date'][:7]) or (
                    m == '00' and project['start_date'][:4] <= y <= project['end_date'][:4]):
                profit += currencyStringToFloat(project['budget'])
                if project['client_name'] not in current_clients:
                    current_clients.append(project['client_name'])

                project_dict = {'name': project['name'], 'client_name': project['client_name']}
                if project['status'] == 'In Progress':
                    current_projects.append(project_dict)
                elif project['status'] == 'Completed':
                    complete_projects.append(project_dict)

        self.ids.reportClient_clientCount.text = f"Clients: {len(set(current_clients))}"
        self.ids.reportClient_projectCount.text = f"Ongoing Projects: {len(current_projects)}"
        self.ids.reportClient_profit.text = f"Total Budget: {convert_currency(profit)}"

        self.ids.ongoingProject_headers.clear_widgets()
        self.ids.completedProject_headers.clear_widgets()
        self.ids.reportClient_ongoingProjects.clear_widgets()
        self.ids.reportClient_completedProjects.clear_widgets()
        self.ids.reportClient_pieChart.clear_widgets()

        self.populate_project_list('Project', 'Client', current_projects, self.ids.ongoingProject_headers,
                                   self.ids.reportClient_ongoingProjects)
        self.populate_project_list('Project Name', 'Client Name', complete_projects, self.ids.completedProject_headers,
                                   self.ids.reportClient_completedProjects)

        self.populate_pieChart(current_projects, complete_projects)

    def populate_project_list(self, header1: str, header2: str, projects: list, header_widget, project_widget) -> None:
        headers = GridLayout(cols=2, size_hint_y=None, height=40)
        headers.add_widget(CLabel(text=header1))
        headers.add_widget(CLabel(text=header2))
        header_widget.add_widget(headers)

        for project in projects:
            grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
            grid.project = project
            grid.add_widget(CLabel(text=project['name']))
            grid.add_widget(CLabel(text=project['client_name']))
            project_widget.add_widget(grid)

    def populate_pieChart(self, ongoing: list, complete: list):
        # take count of the lists
        # each list is a list of dictionaries with name: name, client_name: client_name
        # count the number of dictionaries in the list
        ongoing_count = len(ongoing)
        complete_count = len(complete)
        if ongoing_count == 0 and complete_count == 0:
            data = {"No Data": 1}
        else:
            if ongoing_count == 0:
                data = {"Completed": complete_count}
            elif complete_count == 0:
                data = {"Ongoing": ongoing_count}
            else:
                data = {"Ongoing": ongoing_count, "Completed": complete_count}

        grid = GridLayout(cols=1, size_hint_y=None, height=200)
        chart = PieChart(data=data,position=(1, 1),
                         size=(150,150), legend_enable=True)
        grid.add_widget(chart)
        self.ids.reportClient_pieChart.add_widget(grid)
