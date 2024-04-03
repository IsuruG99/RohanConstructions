from kivy.graphics import Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import rgba


# Custom Button Test
class CButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Make it button grey
        self.background_color = (0.5, 0.5, 0.5, 0.5)
        self.background_normal = ''
        self.background_down = ''
        self.color = (1, 1, 1, 1)
        self.font_name = 'Roboto'
        self.font_size = '20sp'
        self.border_radius = [10, 10, 10, 10]  # Set the radius for all corners

    def on_state(self, instance, value):
        if self.state == 'normal':
            self.color = (1, 1, 1, 1)
        else:
            self.color = rgba('#00FFFF')


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
        self.border_radius = [10, 10, 10, 10]  # Set the radius for all corners
        self.valign = 'middle'
