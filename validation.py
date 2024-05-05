from kivy.uix.gridlayout import GridLayout

from ui import *

from custom import *
from utils import *


class MsgPopUp(GridLayout):
    def __init__(self, parentScreen, content, context='None', btn1='Ok', btn1click=None, **kwargs):
        super().__init__(**kwargs)
        self.parentScreen = parentScreen
        self.content = content
        self.context = context
        self.btn1 = btn1
        self.popup = None
        self.btn1click = btn1click
        self.createMessageBox()
        self.cols = 1
        self.rows = 1

    def createMessageBox(self):
        if self.context == 'Message':
            self.ids.msgGrid.add_widget(CLabel(text=self.content, color=label_text_color))
            self.ids.msgGrid.add_widget(CButton(text=self.btn1, on_release=self.dismiss_and_call_btn1click))

    def dismiss_and_call_btn1click(self, instance):
        if self.btn1click is not None:
            self.btn1click(instance)
            self.popup.dismiss()
        else:
            self.popup.dismiss()

class CfmPopUp(GridLayout):
    def __init__(self, parentScreen, content, context='None', btn1='Ok', btn2='Cancel', btn1click=None, btn2click=None, **kwargs):
        super().__init__(**kwargs)
        self.parentScreen = parentScreen
        self.content = content
        self.context = context
        self.btn1 = btn1
        self.btn2 = btn2
        self.btn1click = btn1click
        self.btn2click = btn2click
        self.popup = None
        self.createConfirmBox()
        self.cols = 1
        self.rows = 1

    def createConfirmBox(self):
        if self.context == 'Confirm':
            self.ids.cfmGrid.add_widget(CLabel(text=self.content, color=label_text_color))
            grid2 = GridLayout(cols=2, size_hint=(1, 0.5), spacing=(10, 0))
            grid2.add_widget(CButton(text=self.btn1, on_release=self.dismiss_and_callback1))
            grid2.add_widget(CButton(text=self.btn2, on_release=self.dismiss_and_callback2))
            self.ids.cfmGrid.add_widget(grid2)

    def dismiss_and_callback1(self, instance):
        if self.btn1click is not None:
            self.btn1click()
            self.popup.dismiss()
        else:
            self.popup.dismiss()

    def dismiss_and_callback2(self, instance):
        if self.btn2click is not None:
            self.btn2click()
            self.popup.dismiss()
        else:
            self.popup.dismiss()


# Part of the AccessControl Decorator
def validate_access(accessLV: int, functionName: str, functionList: list) -> bool:
    if accessLV == 0:
        return True
    else:
        if functionName in functionList:
            return False
        else:
            return True
