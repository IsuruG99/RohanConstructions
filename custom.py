from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import rgba


# Custom Button Test
class CButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.5, 0.5, 0.5, 0.5)
        self.background_normal = ''
        self.background_down = ''
        self.color = (1, 1, 1, 1)
        self.font_name = 'Roboto'
        self.font_size = '20sp'

    def on_state(self, instance, value):
        if self.state == 'normal':
            self.color = (1, 1, 1, 1)
        else:
            self.color = rgba('#00FFFF')


class CButton_V2(CButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.2, 0.2, 0.2, 0.2)


class CLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 1, 1, 1)
        self.font_name = 'Roboto'
        self.font_size = '20sp'  # 20 scaled pixels
        self.halign = 'center'
        self.valign = 'middle'
        self.markup = True


class CText(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.9, 0.9, 0.9, 9)
        self.background_normal = ''
        self.background_active = ''
        self.color = (1, 1, 1, 1)
        self.font_name = 'Roboto'
        self.font_size = '20sp'
        self.valign = 'middle'


class RLabelTop(CLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (10, 40, 10, 20)


class RLabelBot(CLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (10, 20, 10, 40)
        self.font_size = '15sp'
