from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from functions.clients import *
from functools import partial
from kivy.uix.screenmanager import Screen
from utils import *

# add a popup window to insert client data to the database
class AddClientPopup(GridLayout):
    def __init__(self, clients_screen, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.clients_screen = clients_screen

    def add_client(self, name, phone_number, email, address, project_name, project_duration, project_status):
        name = str(name)
        phone_number = str(phone_number)
        email = str(email)
        address = str(address)
        project_name = str(project_name)
        project_duration = str(project_duration)
        project_status = str(project_status)

        if not validate_string(name, phone_number, email, address, project_name, project_duration, project_status):
            message_box('Error', 'All fields are required.')
            return

        add_client(name, phone_number, email, address, project_name, project_duration, project_status)
        self.show_success_popup()

    def show_success_popup(self):
        content = GridLayout(cols=1)
        content.add_widget(Label(text='Client added successfully.'))
        okay_button = Button(text='Okay', size_hint_y=None, height=40)
        okay_button.bind(on_release=self.dismiss_popups)
        content.add_widget(okay_button)

        popup = Popup(title='Success', content=content, size_hint=(None, None), size=(400, 200))
        self.success_popup = popup
        popup.open()

    def dismiss_popups(self, instance):
        if hasattr(self, 'success_popup'):
            self.success_popup.dismiss()
        if hasattr(self, 'clients_screen'):
            self.clients_screen.dismiss_popup()
            self.clients_screen.populate_clients()


# view clients via popup window
class ViewClientPopup(GridLayout):
    def __init__(self, clients_screen, client_id, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.clients_screen = clients_screen
        self.populate_view()

    def populate_view(self):
        client = get_client(self.client_id)

        self.ids.view_name.text = client['name']
        self.ids.view_phone_number.text = client['phone_number']
        self.ids.view_email.text = client['email']
        self.ids.view_address.text = client['address']
        self.ids.view_project_name.text = client['project_name']
        self.ids.view_project_duration.text = client['project_duration']
        self.ids.view_project_status.text = client['project_status']

    def edit_client(self, name, phone_number, email, address, project_name, project_duration, project_status):
        name = str(name)
        phone_number = str(phone_number)
        email = str(email)
        address = str(address)
        project_name = str(project_name)
        project_duration = str(project_duration)
        project_status = str(project_status)

        if not validate_string(name, phone_number, email, address, project_name, project_duration, project_status):
            message_box('Error', 'All fields are required.')
            return

        update_client(self.client_id, name, phone_number, email, address, project_name, project_duration, project_status)
        message_box('Success', 'Client updated successfully.')
        self.clients_screen.populate_clients()

    def delete_client(self):
        if confirm_box('Delete Client', 'Are you sure you want to delete this client?') == 'yes':
            if delete_client(self.client_id):
                message_box('Success', 'Client deleted successfully.')
            else:
                message_box('Error', 'Failed to delete client.')
            self.clients_screen.populate_clients()
            self.dismiss_popup()

    def dismiss_popup(self):
        self.clients_screen.dismiss_popup()


# below is client's main ui
class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_clients()
        self.add_client_popup_instance = None

    def add_client_popup(self):
        add_popup = Popup(title='Add Client', content=AddClientPopup(self), size_hint=(0.5, 0.8))
        add_popup.open()
        self.add_client_popup_instance = add_popup

    def dismiss_popup(self):
        if self.add_client_popup_instance:
            self.add_client_popup_instance.dismiss()
            self.add_client_popup_instance = None

    def populate_clients(self):
        # Get all clients from the database as a list
        clients = load_clients()

        # Clear the existing clients
        self.ids.clients_list.clear_widgets()

        #make a header row


        # Add the clients to the ScrollView # Only name, phone_number and email are shown
        for client in clients:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            grid.add_widget(Label(text=client['name']))
            grid.add_widget(Label(text=client['phone_number']))
            grid.add_widget(Label(text=client['email']))
            grid.add_widget(Button(text='View', on_release=partial(self.view_client, client['id'])))
            grid.client = client
            self.ids.clients_list.add_widget(grid)

    def view_client(self, client_id, instance):
        view_popup = Popup(title='View Client', content=ViewClientPopup(self, client_id), size_hint=(0.5, 0.8))
        view_popup.open()
        view_popup.content.popup = view_popup
