from kivy.uix.gridlayout import GridLayout

from ui import *

from custom import *
from utils import *


class MsgPopUp(GridLayout):
    def __init__(self, parent_screen, content, context, btn1, btn1click, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen
        self.content = content
        self.context = context
        self.btn1 = btn1
        self.btn1click = btn1click
        self.cols = 1
        self.rows = 1
        self.create_message_box()

    def create_message_box(self):
        self.ids.msgGrid.add_widget(CLabel(text=self.content, color=label_text_color))
        grid = GridLayout(cols=3, spacing=10)
        # 2 spaces from left and right to center the button, make them take 0.25 each
        grid.add_widget(CLabel(text='', size_hint_x=0.25))
        grid.add_widget(RButton4(text=self.btn1, size_hint_x=0.5,on_release=self.dismiss_and_call_btn1click))
        grid.add_widget(CLabel(text='', size_hint_x=0.25))
        self.ids.msgGrid.add_widget(grid)


    def dismiss_and_call_btn1click(self, instance):
        if self.btn1click is not None:
            self.btn1click()
        self.popup.dismiss()


class CfmPopUp(GridLayout):
    def __init__(self, parent_screen, content, context, btn1, btn2, btn1click, btn2click, **kwargs):
        super().__init__(**kwargs)
        self.parent_screen = parent_screen
        self.content = content
        self.context = context
        self.btn1 = btn1
        self.btn2 = btn2
        self.btn1click = btn1click
        self.btn2click = btn2click
        self.cols = 1
        self.rows = 1
        self.create_confirm_box()

    def create_confirm_box(self):
        self.ids.cfmGrid.add_widget(CLabel(text=self.content, color=label_text_color))
        # Make a grid for 2 buttons
        grid = GridLayout(cols=2, spacing=10)
        grid.add_widget(RButton4(text=self.btn1, on_release=self.dismiss_and_call_btn1click))
        grid.add_widget(RButton4(text=self.btn2, on_release=self.dismiss_and_call_btn2click))
        self.ids.cfmGrid.add_widget(grid)

    def dismiss_and_call_btn1click(self, instance):
        if self.btn1click is not None:
            self.btn1click()
        self.popup.dismiss()

    def dismiss_and_call_btn2click(self, instance):
        if self.btn2click is not None:
            self.btn2click()
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
