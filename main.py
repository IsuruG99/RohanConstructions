from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from ui.projects_ui import ProjectsScreen
from ui.suppliers_ui import SuppliersScreen
from ui.clients_ui import ClientsScreen
from ui.login_ui import LoginScreen
from utils import message_box

# Load the KV file for the main screen
Builder.load_file('main.kv')
Builder.load_file('ui/login.kv')
Builder.load_file('ui/projects.kv')
Builder.load_file('ui/suppliers.kv')
Builder.load_file('ui/clients.kv')


class MainScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        Window.size = (1200, 720)

        # Screen Manager Initialized
        sm = ScreenManager()

        # Screens are added to Manager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProjectsScreen(name='projects'))
        sm.add_widget(SuppliersScreen(name='suppliers'))
        sm.add_widget(ClientsScreen(name='clients'))

        return sm

    def btn_click(self, instance):
        if instance.text == 'Projects':
            self.root.current = 'projects'  # Switch to the projects screen
        elif instance.text == 'Clients':
            self.root.current = 'clients'  # Switch to the Clients screen
        elif instance.text == 'Resources':
            message_box('Error', 'Resources screen not implemented yet.')
        elif instance.text == 'Suppliers':
            self.root.current = 'suppliers'  # Switch to the Suppliers screen
        elif instance.text == 'Personnel':
            message_box('Error', 'Personnel screen not implemented yet.')
        elif instance.text == 'Finances':
            message_box('Error', 'Finances screen not implemented yet.')

    def on_start(self):
        self.title = 'Rohan Constructions'


if __name__ == '__main__':
    MainApp().run()
