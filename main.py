from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

from ui.archive_ui import ArchiveScreen
from ui.manpower_ui import ManpowerScreen
from ui.projects_ui import ProjectsScreen
from ui.resources_ui import ResourcesScreen
from ui.suppliers_ui import SuppliersScreen
from ui.clients_ui import ClientsScreen
from ui.finances_ui import FinancesScreen
from ui.login_ui import *

from utils import *
from custom import *
from validation import *
from pieChart import *

# Load the KV file for the main screen
Builder.load_file('main.kv')
Builder.load_file('ui/login.kv')
Builder.load_file('ui/projects.kv')
Builder.load_file('ui/suppliers.kv')
Builder.load_file('ui/clients.kv')
Builder.load_file('ui/resources.kv')
Builder.load_file('ui/manpower.kv')
Builder.load_file('ui/finances.kv')
Builder.load_file('ui/archive.kv')
Builder.load_file('validation.kv')



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.loggedIn()

    def btn_click(self, instance) -> None:
        perms = App.get_running_app().get_accessLV()
        if instance.text == 'LogOut' or instance.text == 'LogIn':
            self.openLogPopup(instance.text)
        elif perms is None:
            self.CMessageBox('Error', 'Please login to continue.', 'Message')
            return
        else:
            if instance.text == 'Projects':
                self.parent.current = 'projects'
            elif instance.text == 'Clients':
                self.parent.current = 'clients'
            elif instance.text == 'Resources':
                self.parent.current = 'resources'
            elif instance.text == 'Suppliers':
                self.parent.current = 'suppliers'
            elif instance.text == 'Finances':
                self.parent.current = 'finances'
            elif instance.text == 'Personnel':
                self.parent.current = 'manpower'
            elif instance.text == 'Archive':
                self.parent.current = 'archive'
            elif instance.text == 'Admin':
                self.openAdminControls()

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'Message',
                    btn1: str = 'OK', btn2: str = 'Cancel', btn1click=None, btn2click=None) -> None:
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

    def openAdminControls(self) -> None:
        temp_popup = Popup()  # Temporary Popup instance
        admin_popup = AdminControls(self, temp_popup)
        adminPop = RPopup(title='Admin Controls', content=admin_popup, size_hint=(0.6, 0.9))
        admin_popup.popup = adminPop
        adminPop.open()

    def openLogPopup(self, request: str) -> None:
        if request == 'LogIn':
            temp_popup = Popup()  # Temporary Popup instance
            login_popup = LogInPopUp(self, temp_popup)
            logPop = RPopup(title='LogIn', content=login_popup, size_hint=(0.5, 0.45))
            login_popup.popup = logPop  # Replace the temporary Popup with the actual RPopup
            logPop.open()
        elif request == 'LogOut':
            self.CMessageBox('LogOut', 'You have been logged out.', 'Message')
            App.get_running_app().set_accessLV(None)
            App.get_running_app().set_accessName(None)
            self.ids.logBtn.text = 'LogIn'
            self.ids.logStatus.text = 'Not Logged In.'
            self.ids.projectsBtn.disabled = True
            self.ids.clientsBtn.disabled = True
            self.ids.suppliersBtn.disabled = True
            self.ids.financesBtn.disabled = True
            self.ids.personnelBtn.disabled = True
            self.ids.resourcesBtn.disabled = True
            self.ids.archiveBtn.disabled = True
        else:
            self.CMessageBox('Error', 'Invalid Request', 'Message')

    def loggedIn(self, email: str = None) -> None:
        perms = App.get_running_app().get_accessLV()
        if perms is not None:
            self.ids.logBtn.text = 'LogOut'
            self.ids.logStatus.text = 'Welcome, ' + cutEmail(email) + '!'
            # If user is access 2 and 3, enable the Personnel and Resources buttons
            if perms in [2, 3]:
                self.ids.financesBtn.disabled = True
                self.ids.archiveBtn.disabled = True
                self.ids.projectsBtn.disabled = False
                self.ids.clientsBtn.disabled = False
                self.ids.suppliersBtn.disabled = False
                self.ids.personnelBtn.disabled = False
                self.ids.resourcesBtn.disabled = False
                if perms == 2:
                    self.ids.financesBtn.disabled = False
            # If user is access 1 or 0, enable all buttons, show Admin Panel
            else:
                self.ids.projectsBtn.disabled = False
                self.ids.clientsBtn.disabled = False
                self.ids.suppliersBtn.disabled = False
                self.ids.financesBtn.disabled = False
                self.ids.personnelBtn.disabled = False
                self.ids.resourcesBtn.disabled = False
                self.ids.archiveBtn.disabled = False
                self.ids.logBtn.text = 'Admin'
        # if user us not logged in disable all buttons
        else:
            self.ids.logBtn.text = 'LogIn'
            self.ids.logStatus.text = 'Not Logged In.'
            self.ids.projectsBtn.disabled = True
            self.ids.clientsBtn.disabled = True
            self.ids.suppliersBtn.disabled = True
            self.ids.financesBtn.disabled = True
            self.ids.personnelBtn.disabled = True
            self.ids.resourcesBtn.disabled = True
            self.ids.archiveBtn.disabled = True


class MainApp(App):
    accessLV: int = None
    accessName: str = None

    def set_accessLV(self, level) -> None:
        if level is None:
            self.accessLV = None
        else:
            self.accessLV = int(level)

    def get_accessLV(self) -> int:
        return self.accessLV

    def set_accessName(self, name: str) -> None:
        self.accessName = name

    def get_accessName(self) -> str:
        return self.accessName

    def build(self) -> ScreenManager:
        Window.size = (1200, 720)
        Window.clearcolor = rgba('#343534')
        Window.set_icon('visuals/icon.png')

        # Remove max/min buttons
        Window.borderless = False

        # Screen Manager Initialized
        sm = ScreenManager()

        # Screens are added to Manager
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProjectsScreen(name='projects'))
        sm.add_widget(SuppliersScreen(name='suppliers'))
        sm.add_widget(ClientsScreen(name='clients'))
        sm.add_widget(ResourcesScreen(name='resources'))
        sm.add_widget(ManpowerScreen(name='manpower'))
        sm.add_widget(FinancesScreen(name='finances'))
        sm.add_widget(ArchiveScreen(name='archive'))

        return sm

    def on_start(self) -> None:
        Window.set_title('Rohan Constructions')


if __name__ == '__main__':
    MainApp().run()
