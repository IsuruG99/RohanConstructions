from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from ui.manpower_ui import ManpowerScreen
from ui.projects_ui import ProjectsScreen
from ui.resources_ui import ResourcesScreen
from ui.suppliers_ui import SuppliersScreen
from ui.clients_ui import ClientsScreen
from ui.login_ui import LoginScreen
from ui.finances_ui import FinancesScreen

from utils import *
from custom import *

# Load the KV file for the main screen
Builder.load_file('main.kv')
Builder.load_file('ui/login.kv')
Builder.load_file('ui/projects.kv')
Builder.load_file('ui/suppliers.kv')
Builder.load_file('ui/clients.kv')
Builder.load_file('ui/resources.kv')
Builder.load_file('ui/manpower.kv')
Builder.load_file('ui/finances.kv')


class MainScreen(Screen):
    pass


class MainApp(App):
    accessLV = None

    def set_accessLV(self, level):
        self.accessLV = level

    def get_accessLV(self):
        return self.accessLV

    def build(self):
        Window.size = (1200, 720)
        Window.clearcolor = rgba('#411f2d')
        Window.set_icon('visuals/icon.png')

        # Screen Manager Initialized
        sm = ScreenManager()

        # Screens are added to Manager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProjectsScreen(name='projects'))
        sm.add_widget(SuppliersScreen(name='suppliers'))
        sm.add_widget(ClientsScreen(name='clients'))
        sm.add_widget(ResourcesScreen(name='resources'))
        sm.add_widget(ManpowerScreen(name='manpower'))
        sm.add_widget(FinancesScreen(name='finances'))

        return sm

    def btn_click(self, instance):
        perms = App.get_running_app().get_accessLV()
        if instance.text == 'Projects':
            self.root.current = 'projects' if perms <= 1 else message_box('Error', 'Access Denied')
        elif instance.text == 'Clients':
            self.root.current = 'clients' if perms <= 1 else message_box('Error', 'Access Denied')
        elif instance.text == 'Resources':
            self.root.current = 'resources'
        elif instance.text == 'Suppliers':
            self.root.current = 'suppliers' if perms <= 1 else message_box('Error', 'Access Denied')
        elif instance.text == 'Finances':
            self.root.current = 'finances' if perms <= 1 else message_box('Error', 'Access Denied')
        elif instance.text == 'Personnel':
            self.root.current = 'manpower'

    def on_start(self):
        Window.set_title('Rohan Constructions')


if __name__ == '__main__':
    MainApp().run()
