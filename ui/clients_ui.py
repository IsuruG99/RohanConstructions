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
from utils import *
from validation import *


# add a popup window to insert client data to the database
class AddClientPopup(GridLayout):
    def __init__(self, clients_screen, **kwargs):
        super().__init__(**kwargs)
        self.clients_screen = clients_screen

    def add_client(self, name, phone_number, email, address):
        name = str(name)
        phone_number = str(phone_number)
        email = str(email)
        address = str(address)

        if not validate_string(name, phone_number, email, address):
            self.clients_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return
        if not validate_mobileNo(phone_number):
            self.clients_screen.CMessageBox('Error', 'Invalid phone number.', 'Message')
            return
        if not validate_email(email):
            self.clients_screen.CMessageBox('Error', 'Invalid email address.', 'Message')
            return
        if add_client(name, phone_number, email, address):
            self.clients_screen.CMessageBox('Success', 'Client added successfully.', 'Message')
            self.clients_screen.populate_clients(load_clients(0))
            self.dismiss_popup(self.popup)

    def load_project_list(self):
        return load_project_names()

    def dismiss_popup(self, instance):
        instance.dismiss()


# view clients via popup window
class ViewClientPopup(GridLayout):
    def __init__(self, clients_screen, client_id, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.clients_screen = clients_screen
        self.populate_view()

    def populate_view(self):
        # Get the client data from the database
        client = get_client(self.client_id)
        # Populate View
        self.ids.view_client_name.text = client['name']
        self.ids.view_client_phone_number.text = str(client['phone_number'])
        self.ids.view_client_email.text = client['email']
        self.ids.view_client_address.text = client['address']

    def edit_client(self, name, phone_number, email, address):
        name = str(name)
        phone_number = str(phone_number)
        email = str(email)
        address = str(address)

        if not validate_string(name, phone_number, email, address):
            self.clients_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return
        if not validate_mobileNo(phone_number):
            self.clients_screen.CMessageBox('Error', 'Invalid phone number.', 'Message')
            return
        if not validate_email(email):
            self.clients_screen.CMessageBox('Error', 'Invalid email address.', 'Message')
            return

        if confirm_box('Update Client', 'Are you sure you want to update this client?') == 'yes':
            if update_client(self.client_id, name, phone_number, email, address):
                self.clients.CMessageBox('Success', 'Client updated successfully.', 'Message')
                self.clients_screen.populate_clients(load_clients(0))
                self.dismiss_popup(self.popup)
            else:
                self.clients.CMessageBox('Error', 'Failed to update client.', 'Message')

    def delete_client(self):
        if confirm_box('Delete Client', 'Are you sure you want to delete this client?') == 'yes':
            if delete_client(self.client_id):
                self.clients_screen.CMessageBox('Success', 'Client deleted successfully.', 'Message')
                self.clients_screen.populate_clients(load_clients(0))
                self.dismiss_popup(self.popup)
            else:
                self.clients_screen.CMessageBox('Error', 'Failed to delete client.', 'Message')
                self.dismiss_popup(self.popup)

    def dismiss_popup(self,instance):
        instance.dismiss()


# below is client's main ui
class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_clients()
        self.add_client_popup_instance = None

    def add_client_popup(self):
        add_client_popup = CPopup(title='Add Client', content=AddClientPopup(self), size_hint=(0.5, 0.8))
        add_client_popup.open()
        add_client_popup.content.popup = add_client_popup

    def dismiss_popup(self, instance):
        instance.dismiss()

    def CMessageBox(self, title='Message', content='Message Content', context='None', btn1='Ok', btn2='Cancel',
                    btn1click=None, btn2click=None):
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

    def populate_clients(self, clients=load_clients(0), headers=None):
        # Clear the existing clients
        self.ids.clients_list.clear_widgets()
        self.ids.clients_headers.clear_widgets()

        # Headers
        if headers is None:
            headers = ['Name', 'Phone Number', 'Email', 'Action']
        size_hints = [0.4, 0.2, 0.3, 0.1]
        for header in headers:
            self.ids.clients_headers.add_widget(CButton(text=header, bold=True, padding=(10,10), size_hint_x=size_hints[headers.index(header)],
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

    def sort_clients(self, clients, header, instance):
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

    def search_clients(self, searchValue):  # Finish this function
        if not searchValue == '':
            clients = load_clients(0)
            clients = [client for client in clients
                       if searchValue.lower() in client['name'].lower()
                       or searchValue.lower() in client['phone_number'].lower()
                       or searchValue.lower() in client['email'].lower()]
            self.populate_clients(clients)

    def view_client(self, client_id, instance):
        view_popup = CPopup(title='View Client', content=ViewClientPopup(self, client_id), size_hint=(0.5, 0.8))
        view_popup.open()
        view_popup.content.popup = view_popup

    def report_clients(self):
        report_popup = CPopup(title='Clients Report', content=ClientsReport(self), size_hint=(0.5, 0.8))
        report_popup.open()
        report_popup.content.popup = report_popup

    def btn_click(self, instance):
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
    def __init__(self, client_screen, **kwargs):
        super().__init__(**kwargs)
        self.client_screen = client_screen
        self.populate_report()

    def populate_report(self):
        # Assume the fields are in kv, populate it from the database
        clients = load_clients(0)

        # Show client count on reportClient_count
        self.ids.reportClient_count.text = "Client Count: " + str(len(clients))

    def dismiss_popup(self, instance):
        instance.dismiss()

