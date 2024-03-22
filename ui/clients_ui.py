from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.clients import *
from functools import partial

from utils import *


# Client Main UI (Accessed by main.py)
class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Button Click goes back to Main UI
    def btn_click(self, instance):
        if instance.text == 'Back':
            self.parent.current = 'main'
