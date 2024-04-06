from kivy.graphics import Color, Rectangle, BoxShadow
from kivy.properties import BoundedNumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.utils import rgba

main_background_color = rgba('#411f2d')
button_normal_text_color = rgba('#ffffff')
button_normal_background_color = rgba('#ac4147')
button_down_text_color = rgba('#ffffff')
button_down_background_color = rgba('#f88863')
label_text_color = rgba('#ffffff')
text_input_background_color = rgba('#ffc27f')
text_input_text_color = rgba('#411f2d')
popup_background_color = rgba('#411f2d')
popup_title_color = rgba('#ffffff')
popup_separator_color = rgba('#ffffff')
spinner_background_color = rgba('#411f2d')
spinner_text_color = rgba('#ffffff')

spinner_font_name = 'Roboto'
label_font_name = 'Roboto'
popup_title_font_name = 'Roboto'
text_input_font_name = 'Roboto'

popup_title_font_size = '30sp'
spinner_font_size = '20sp'
label_font_size = '20sp'
text_input_font_size = '20sp'


class CPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = ''  # Remove the default background
        self.title_color = popup_title_color
        self.background_color = popup_background_color
        self.separator_color = popup_separator_color
        self.title_size = popup_title_font_size
        self.title_name = popup_title_font_name
        self.title_align = 'center'
        self.title_height = 40


# Custom Button Test
class CButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = button_normal_text_color
        self.background_color = button_normal_background_color
        self.background_normal = ''
        self.background_down = ''
        self.font_name = 'Roboto'
        self.font_size = '20sp'

    def on_state(self, instance, value):
        if self.state == 'normal':
            self.color = button_normal_text_color
            self.background_color = button_normal_background_color
        else:
            self.color = button_down_text_color
            self.background_color = button_down_background_color


class CButton2(CButton):
    shadow_offset = BoundedNumericProperty(30, min=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(pos=self.update_shadow_pos)
        self.bind(size=self.update_shadow_size)

        # Box Shadow Test
        with self.canvas.before:
            Color(0, 0, 0, 0.5)
            self.shadow = BoxShadow(pos=self.pos, size=self.size, offset=(0, -10),
                                    spread_radius=(-35, -35), border_radius=(0, 0, 0, 10), blur_radius=80)

    def update_shadow_pos(self, instance, value):
        self.shadow.pos = value[0], value[1] - self.shadow_offset

    def update_shadow_size(self, instance, value):
        self.shadow.size = value[0], value[1]


class CLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = label_text_color
        self.font_name = label_font_name
        self.font_size = label_font_size  # 20 scaled pixels
        self.halign = 'center'
        self.valign = 'middle'
        self.markup = True


class CText(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = text_input_text_color
        self.font_name = text_input_font_name
        self.font_size = text_input_font_size
        self.background_color = text_input_background_color
        self.background_normal = ''
        self.background_active = ''
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


class CSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = spinner_font_name
        self.font_size = spinner_font_size
        self.background_color = spinner_background_color
        self.color = spinner_text_color
        self.option_cls.background_color = spinner_background_color
        self.option_cls.color = spinner_text_color
        self.background_normal = ''
        self.background_down = ''
        self.valign = 'middle'
        self.padding = (10, 10)
        # scroll bar
        self.scroll_width = 20
