from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from ui.projects_ui import ProjectsScreen
from utils import messagebox

# Load the KV file for the main screen
Builder.load_file('main.kv')
Builder.load_file('ui/projects.kv')


class MainScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        # Screen Manager Initialized
        sm = ScreenManager()

        # Screens are added to Manager
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProjectsScreen(name='projects'))

        return sm

    def btn_click(self, instance):
        if instance.text == 'Projects':
            self.root.current = 'projects'  # Switch to the projects screen
        elif instance.text == 'Clients':
            messagebox('Error', 'Clients screen not implemented yet.')
        elif instance.text == 'Resources':
            messagebox('Error', 'Resources screen not implemented yet.')
        elif instance.text == 'Suppliers':
            messagebox('Error', 'Suppliers screen not implemented yet.')
        elif instance.text == 'Personnel':
            messagebox('Error', 'Personnel screen not implemented yet.')
        elif instance.text == 'Finances':
            messagebox('Error', 'Finances screen not implemented yet.')


if __name__ == '__main__':
    MainApp().run()
