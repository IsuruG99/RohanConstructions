from kivy.graphics import Color, Rectangle, BoxShadow, RoundedRectangle, Line
from kivy.properties import BoundedNumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.dropdown import DropDown

import database

main_background_color = rgba('#343534')
button_normal_text_color = rgba('#f0e29f')
button_normal_background_color = rgba('#2d2c2d')
button_normal_border_color = rgba('#f0e29f')
button_down_text_color = rgba('#9eacf0')
button_down_background_color = rgba('#2d2c2d')
button_down_border_color = rgba('#9eacf0')
label_text_color = rgba('#f0e29f')
text_input_background_color = rgba('#d0c376')
text_input_text_color = rgba('#2d2c2d')
popup_title_color = rgba('#f0e29f')
popup_separator_color = rgba('#f0e29f')
popup_background_color = rgba('#2d2c2d')
popup_border_color = rgba('#bdb281')
spinner_background_color = rgba('#d0c376')
spinner_text_color = rgba('#2d2c2d')

spinner_font_name = 'Roboto'
label_font_name = 'Roboto'
popup_title_font_name = 'Roboto'
text_input_font_name = 'Roboto'
button_font_name = 'Roboto'

popup_title_font_size = '30sp'
spinner_font_size = '18sp'
label_font_size = '18sp'
text_input_font_size = '18sp'

pieChart_color1 = rgba('#ff69b4')  # Light Pink
pieChart_color2 = rgba('#add8e6')  # Light Blue


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


class RoundedBackgroundContent(BoxLayout):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(rgba=popup_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[25])
            # make border color #343534
            self.border_color = Color(rgba=popup_border_color)
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 25), width=2)
            self.bind(size=self.update_rect, pos=self.update_rect)
        self.add_widget(content)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 25)


class PopupContent(BoxLayout):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.title_label = Label(text=title, font_size=popup_title_font_size, size_hint_y=None, height=40,
                                 color=popup_title_color, font_name=popup_title_font_name)
        self.separator = Widget(size_hint_y=None, height=2)
        self.separator.canvas.add(Color(rgba=popup_separator_color))
        self.separator.canvas.add(Rectangle(pos=self.separator.pos, size=self.separator.size))
        self.add_widget(self.title_label)
        self.add_widget(self.separator)
        self.add_widget(content)


class RPopup(Popup):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        #make title color, seperater color invisible
        self.title_color = rgba(0, 0, 0, 0)
        self.separator_color = rgba(0, 0, 0, 0)
        self.title = ''
        self.background = ''
        self.background_color = rgba(0, 0, 0, 0)
        self.content = RoundedBackgroundContent(PopupContent(title, content))

    def dismiss(self, *args, **kwargs):
        super().dismiss(*args, **kwargs)


# Custom Button Test
class CButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = button_normal_text_color
        self.background_color = button_normal_background_color
        self.background_normal = ''
        self.background_down = ''
        self.font_name = button_font_name
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
            self.shadow = BoxShadow(pos=self.pos,
                                    size=self.size,
                                    offset=(0, -10),
                                    spread_radius=(-35, -35),
                                    border_radius=(0, 0, 0, 10),
                                    blur_radius=80)

    def update_shadow_pos(self, instance, value):
        self.shadow.pos = value[0], value[1] - self.shadow_offset

    def update_shadow_size(self, instance, value):
        self.shadow.size = value[0], value[1]


# 10% Edge RButton
class RButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Transparent background color, so the button has no background color
        self.color = button_normal_text_color
        self.background_color = rgba(0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        self.font_name = button_font_name
        self.font_size = '20sp'

        # Then we use a rounded rectangle to draw the button in a color we want
        with self.canvas.before:
            self.rect_color = Color(rgba=button_normal_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_state(self, instance, value):
        # On state should change the color of the rounded rectangle
        if self.state == 'down':
            self.rect_color.rgba = button_down_background_color
            self.color = button_down_text_color
        else:
            self.color = button_normal_text_color
            self.rect_color.rgba = button_normal_background_color


class RButton2(RButton):
    shadow_offset = BoundedNumericProperty(30, min=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_shadow_pos)
        self.bind(size=self.update_shadow_size)

        # Box Shadow Test
        with self.canvas.before:
            Color(0, 0, 0, 0.5)
            self.shadow = BoxShadow(pos=self.pos,
                                    size=self.size,
                                    offset=(0, -10),
                                    spread_radius=(-35, -35),
                                    border_radius=(0, 0, 0, 10),
                                    blur_radius=80)

    def update_shadow_pos(self, instance, value):
        self.shadow.pos = value[0], value[1] - self.shadow_offset

    def update_shadow_size(self, instance, value):
        self.shadow.size = value[0], value[1]


# 25% Edge RButton
class RButton3(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = button_normal_text_color
        self.background_color = rgba(0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        self.font_name = button_font_name
        self.font_size = '20sp'

        # Then we use a rounded rectangle to draw the button in a color we want
        with self.canvas.before:
            self.rect_color = Color(rgba=button_normal_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[25])
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_state(self, instance, value):
        # On state should change the color of the rounded rectangle
        if self.state == 'down':
            self.rect_color.rgba = button_down_background_color
            self.color = button_down_text_color
        else:
            self.color = button_normal_text_color
            self.rect_color.rgba = button_normal_background_color


# Rounded Bordered Button
class RButton4(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = button_normal_text_color
        self.background_color = rgba(0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        self.font_name = button_font_name
        self.font_size = '20sp'

        # Then we use a rounded rectangle to draw the button in a color we want
        with self.canvas.before:
            # Add a yellow border
            self.border_color = Color(rgba=button_normal_border_color)  # yellow
            self.border_rect = RoundedRectangle(size=(self.size[0] + 2, self.size[1] + 2), pos=self.pos,
                                                radius=[12])

            # The original rounded rectangle
            self.rect_color = Color(rgba=button_normal_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.border_rect.pos = (instance.pos[0] - 1, instance.pos[1] - 1)
        self.border_rect.size = (instance.size[0] + 2, instance.size[1] + 2)

    def on_state(self, instance, value):
        # On state should change the color of the rounded rectangle
        if self.state == 'down':
            self.rect_color = Color(rgba=button_down_background_color)
            self.color = button_down_text_color
            self.border_color = Color(rgba=button_down_border_color)
        else:
            self.color = button_normal_text_color
            self.rect_color = Color(rgba=button_normal_background_color)
            self.border_color = Color(rgba=button_normal_border_color)


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
        self.multiline = False
        self.padding_x = 15


class RText(CText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (10, 10, 10, 10)
        self.background_color = (0, 0, 0, 0)

        # rounded rectangle
        with self.canvas.before:
            Color(rgba=text_input_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = spinner_font_name
        self.font_size = spinner_font_size
        self.background_color = spinner_background_color
        self.color = spinner_text_color
        self.option_cls.background_color = spinner_background_color
        self.option_cls.color = (1, 1, 1, 1)
        self.background_normal = ''
        self.background_down = ''
        self.valign = 'middle'
        self.padding = (10, 10)
        # scroll bar
        self.scroll_width = 20


class RSpinner(CSpinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (10, 10, 10, 10)
        self.background_color = (0, 0, 0, 0)

        # rounded rectangle
        with self.canvas.before:
            Color(rgba=spinner_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class AutoFillText(CText):
    def __init__(self, completions: list = ["A"], **kwargs):
        super().__init__(**kwargs)
        self.completions = completions
        self.dropdown = DropDown()
        self.bind(focus=self.on_focus)
        self.dropdown.bind(on_select=self.on_dropdown_select)

    def on_text(self, instance, value):
        if self.focus:
            matches = [completion for completion in self.completions if completion.startswith(value)]
            if matches:
                self.dropdown.clear_widgets()
                for match in matches:
                    btn = CButton(text=match, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                    self.dropdown.add_widget(btn)
                if not self.dropdown.parent:
                    self.dropdown.open(self)
            else:
                self.dropdown.dismiss()
        else:
            self.dropdown.dismiss()

    def on_dropdown_select(self, instance, data):
        self.text = data
        self.dropdown.dismiss()

    def on_focus(self, instance, value):
        if value:
            self.bind(text=self.on_text)
        else:
            self.dropdown.dismiss()


class RAutoFillText(AutoFillText):
    def __init__(self, completions: list = ["A"], **kwargs):
        super().__init__(completions, **kwargs)
        self.padding = (10, 10, 10, 10)
        self.background_color = (0, 0, 0, 0)

        # rounded rectangle
        with self.canvas.before:
            Color(rgba=text_input_background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MenuButton(RButton3):
    main_text = StringProperty('a')
    sub_text = StringProperty('b')
    main_font_size = StringProperty('55sp')
    sub_font_size = StringProperty('20sp')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, rows=2, size=self.size, pos=self.pos)
        self.main_label = CLabel(text=self.main_text, size=self.size, pos=self.pos, font_size=self.main_font_size,
                                 color=button_normal_text_color)
        self.sub_label = CLabel(text=self.sub_text, size=self.size, pos=self.pos, font_size=self.sub_font_size,
                                color=button_normal_text_color)
        self.layout.add_widget(self.main_label)
        self.layout.add_widget(self.sub_label)
        self.add_widget(self.layout)
        self.bind(size=self.update_layout, pos=self.update_layout)
        self.bind(main_text=self.update_text, sub_text=self.update_text)
        self.bind(main_font_size=self.update_font_size, sub_font_size=self.update_font_size)
        self.bind(state=self.on_state)

    def update_layout(self, instance, value):
        self.layout.size = instance.size
        self.layout.pos = instance.pos

    def update_text(self, instance, value):
        self.main_label.text = self.main_text
        self.sub_label.text = self.sub_text

    def update_font_size(self, instance, value):
        self.main_label.font_size = self.main_font_size
        self.sub_label.font_size = self.sub_font_size

    def on_state(self, instance, value):
        if self.state == 'down':
            self.main_label.color = button_down_text_color
            self.sub_label.color = button_down_text_color
            self.color = button_down_background_color
        else:
            self.main_label.color = button_normal_text_color
            self.sub_label.color = button_normal_text_color
            self.color = button_normal_background_color
