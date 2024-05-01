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
        name = str(self.ids.add_client_name.text)
        phone_number = str(self.ids.add_client_phone_number.text)
        email = str(self.ids.add_client_email.text)
        address = str(self.ids.add_client_address.text)

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
        elif requestType == "Submit":
            if self.validCheck == 1:
                if add_client(name, phone_number, email, address):
                    self.clients_screen.CMessageBox('Success', 'Client added successfully.', 'Message')
                    self.clients_screen.populate_clients(load_clients(0))
                    self.validCheck = 0
                    self.dismiss_popup(self.popup)

    def load_project_list(self) -> list:
        return load_project_names()

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()


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

    def edit_client(self, requestType: str = "Submit") -> None:
        # view_client_name.text, view_client_phone_number.text, view_client_email.text, view_client_address.text
        name = str(self.ids.view_client_name.text)
        phone_number = str(self.ids.view_client_phone_number.text)
        email = str(self.ids.view_client_email.text)
        address = str(self.ids.view_client_address.text)
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
            self.clients_screen.CMessageBox('Confirm', 'Are you sure you want to update this client?', 'Confirm', 'Yes',
                                            'No', self.edit_client)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                if update_client(self.client_id, name, phone_number, email, address):
                    self.clients_screen.CMessageBox('Success', 'Client updated successfully.', 'Message')
                    self.clients_screen.populate_clients(load_clients(0))
                    self.validCheck = 0
                    self.dismiss_popup(self.popup)
                else:
                    self.clients.CMessageBox('Error', 'Failed to update client.', 'Message')
                    self.validCheck = 0

    def delete_client(self, requestType: str = "Submit") -> None:
        if requestType == "Validate":
            self.clients_screen.CMessageBox('Confirm', 'Are you sure you want to delete this client?', 'Confirm', 'Yes',
                                            'No', self.delete_client)
        elif requestType == "Submit":
            if delete_client(self.client_id):
                self.clients_screen.CMessageBox('Success', 'Client deleted successfully.', 'Message')
                self.clients_screen.populate_clients(load_clients(0))
                self.dismiss_popup(self.popup)
            else:
                self.clients_screen.CMessageBox('Error', 'Failed to delete client.', 'Message')

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()


# below is client's main ui
class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_clients()
        self.add_client_popup_instance = None

    def add_client_popup(self) -> None:
        temp_addClient_popup = Popup()
        addClient_popup = AddClientPopup(self, temp_addClient_popup)
        add_client_popup = RPopup(title='Add Client', content=addClient_popup, size_hint=(0.5, 0.8))
        addClient_popup.popup = add_client_popup
        add_client_popup.open()

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'None',
                    btn1: str = 'Ok', btn2: str = 'Cancel',
                    btn1click: str = None, btn2click: str = None) -> None:
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

    def populate_clients(self, clients: list = load_clients(0), headers: list = None) -> None:
        # Clear the existing clients
        self.ids.clients_list.clear_widgets()
        self.ids.clients_headers.clear_widgets()

        # Headers
        if headers is None:
            headers = ['Name', 'Phone Number', 'Email', 'Action']
        size_hints = [0.4, 0.2, 0.3, 0.1]
        for header in headers:
            self.ids.clients_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_clients, clients, header)))

        # Add the clients to the ScrollView # Only name, phone_number and email are shown
        for client in clients:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            grid.client = client
            grid.add_widget(CLabel(text=client['name'], size_hint_x=0.4))
            grid.add_widget(CLabel(text=client['phone_number'], size_hint_x=0.2))
            grid.add_widget(CLabel(text=client['email'], size_hint_x=0.3))
            grid.add_widget(Button(text='View', on_release=partial(self.view_client, client['id']), size_hint_x=0.1,
                                   background_normal='', background_color=(0.1, 0.1, 0.1, 0), font_size='20sp'))

            self.ids.clients_list.add_widget(grid)

    def sort_clients(self, clients: list, header: str, instance) -> None:
        if header == 'Name' or header == 'Name [D]':
            clients = sorted(clients, key=lambda x: x['name'])
            self.populate_clients(clients, ['Name [A]', 'Phone Number', 'Email', 'Action'])
        elif header == 'Name [A]':
            clients = sorted(clients, key=lambda x: x['name'], reverse=True)
            self.populate_clients(clients, ['Name [D]', 'Phone Number', 'Email', 'Action'])
        elif header == 'Phone Number' or header == 'Phone Number [D]':
            clients = sorted(clients, key=lambda x: str(x['phone_number']))
            self.populate_clients(clients, ['Name', 'Phone Number [A]', 'Email', 'Action'])
        elif header == 'Phone Number [A]':
            clients = sorted(clients, key=lambda x: str(x['phone_number']), reverse=True)
            self.populate_clients(clients, ['Name', 'Phone Number [D]', 'Email', 'Action'])
        elif header == 'Email' or header == 'Email [D]':
            clients = sorted(clients, key=lambda x: x['email'])
            self.populate_clients(clients, ['Name', 'Phone Number', 'Email [A]', 'Action'])
        elif header == 'Email [A]':
            clients = sorted(clients, key=lambda x: x['email'], reverse=True)
            self.populate_clients(clients, ['Name', 'Phone Number', 'Email [D]', 'Action'])

    def search_clients(self, searchValue: str) -> None:  # Finish this function
        if not searchValue == '':
            clients = load_clients(0)
            clients = [client for client in clients
                       if searchValue.lower() in client['name'].lower()
                       or searchValue.lower() in client['phone_number'].lower()
                       or searchValue.lower() in client['email'].lower()]
            self.populate_clients(clients)

    def view_client(self, client_id: str, instance) -> None:
        temp_viewPopup = Popup()
        viewPopup = ViewClientPopup(self, client_id, temp_viewPopup)
        view_popup = RPopup(title='View Client', content=viewPopup, size_hint=(0.5, 0.8))
        viewPopup.popup = view_popup
        view_popup.open()

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
        elif txt == 'Overview':
            self.report_clients()


class ClientsReport(GridLayout):
    def __init__(self, client_screen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.client_screen = client_screen
        year = str(datetime.datetime.now().year)
        month = str(convert_monthToNumber(convert_numberToMonth(datetime.datetime.now().month)))
        self.populate_clientOverview(year, month)
        self.popup = popup
        self.cols = 1
        self.rows = 1

    def populate_clientOverview(self, y: str, m: str) -> None:
        # Assume the fields are in kv, populate it from the database
        if y == '' or None:
            self.finance_screen.CMessageBox('Error', 'Year is required.', 'Message')
            return

        clients = load_clients(0)
        projects = load_projects()
        if m == '':
            m = '00'
        else:
            m = str(convert_monthToNumber(m))
        current_clients: list = []
        # current_projects must hold name and client_name in key value pairs
        current_projects: list = []
        complete_projects: list = []
        project_count: int = 0
        profit: int = 0

        for project in projects:
            # project has to be within the year and month, there is start_date and end_date
            # If project start date is lower or equal to the year and month and end date is higher or equal to the year and month
            # project start_date and end_date are stored as string in the database
            if project['start_date'][:7] <= y + '-' + m and project['end_date'][:7] >= y + '-' + m:
                profit += currencyStringToFloat(project['budget'])
                # append to current clients if not already in the list
                if project['client_name'] not in current_clients:
                    current_clients.append(project['client_name'])
                # append to current_projects if status is In-Progress, as name: project name, client_name: client name
                if project['status'] == 'In Progress':
                    current_projects.append({'name': project['name'], 'client_name': project['client_name']})
                    project_count += 1
                if project['status'] == 'Completed':
                    complete_projects.append({'name': project['name'], 'client_name': project['client_name']})
            # elif month is 00 and year is the start_date year is lower or equal, end_date year is higher or equal
            elif m == '00' and project['start_date'][:4] <= y and project['end_date'][:4] >= y:
                profit += currencyStringToFloat(project['budget'])
                if project['client_name'] not in current_clients:
                    current_clients.append(project['client_name'])
                if project['status'] == 'In Progress':
                    current_projects.append({'name': project['name'], 'client_name': project['client_name']})
                    project_count += 1
                elif project['status'] == 'Completed':
                    complete_projects.append({'name': project['name'], 'client_name': project['client_name']})
            else:
                continue

        # Show client count on reportClient_count
        self.ids.reportClient_clientCount.text = "Clients: " + str(len(set(current_clients)))
        self.ids.reportClient_projectCount.text = "Ongoing Projects: " + str(len(current_projects))
        self.ids.reportClient_profit.text = "Total Budget: " + convert_currency(profit)

        # clear the existing widgets
        self.ids.ongoingProject_headers.clear_widgets()
        self.ids.completedProject_headers.clear_widgets()
        self.ids.reportClient_ongoingProjects.clear_widgets()
        self.ids.reportClient_completedProjects.clear_widgets()
        self.ids.reportClient_pieChart.clear_widgets()

        #Adding the current_projects to reportClient_ongoingProjects
        # current_projects = [{'name': 'Project Name', 'client_name': 'Client Name'}]
        headers = GridLayout(cols=2, size_hint_y=None, height=40)
        headers.add_widget(CLabel(text='Project'))
        headers.add_widget(CLabel(text='Client'))
        self.ids.ongoingProject_headers.add_widget(headers)

        for project in current_projects:
            gridCurrent = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
            gridCurrent.project = project
            gridCurrent.add_widget(CLabel(text=project['name']))
            gridCurrent.add_widget(CLabel(text=project['client_name']))
            self.ids.reportClient_ongoingProjects.add_widget(gridCurrent)

        #Adding the complete_projects to reportClient_completedProjects
        # complete_projects = [{'name': 'Project Name', 'client_name': 'Client Name'}]
        headers = GridLayout(cols=2, size_hint_y=None, height=40)
        headers.add_widget(CLabel(text='Project Name'))
        headers.add_widget(CLabel(text='Client Name'))
        self.ids.completedProject_headers.add_widget(headers)

        for project in complete_projects:
            gridCompleted = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
            gridCompleted.project = project
            gridCompleted.add_widget(CLabel(text=project['name']))
            gridCompleted.add_widget(CLabel(text=project['client_name']))
            self.ids.reportClient_completedProjects.add_widget(gridCompleted)

        self.populate_pieChart(current_projects, complete_projects)

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


    def dismiss_popup(self, instance) -> None:
        instance.dismiss()
