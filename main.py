from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


def btn_click(instance):
    # Navigate to corresponding UI based on button text
    btn_text = instance.text
    if btn_text == 'Projects':
        print('Projects')
    elif btn_text == 'Clients':
        print('Clients')
    elif btn_text == 'Resources':
        print('Resources')
    elif btn_text == 'Suppliers':
        print('Suppliers')
    elif btn_text == 'Personnel':
        print('Personnel')
    elif btn_text == 'Finances':
        print('Finances')


class MainApp(App):
    def build(self):
        # Window Options
        Window.size = (800, 400)
        Window.clearcolor = (0.5, 0.5, 0.5, 1)
        Window.title = 'Project Management System'

        # Main Layout
        root_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title Label
        root_layout.add_widget(Label(text='Project Management System', size_hint=(1, 0.1), font_size=30,
                                     color=(1, 1, 1, 1), bold=True))
        root_layout.add_widget(Label(text='Rohan Constructions', size_hint=(1, 0.1), font_size=25,
                                     color=(1, 1, 1, 1)))

        # Button Layout
        btn_layout = GridLayout(cols=3, spacing=20, padding=20, size_hint=(1, 0.6))

        # Create Buttons & Add to Layout
        options = ['Projects', 'Clients', 'Suppliers', 'Resources',
                   'Personnel', 'Finances']
        for option in options:
            btn = Button(text=option, size_hint=(1, 0.2), font_size=20)
            btn.bind(on_press=btn_click)
            btn_layout.add_widget(btn)

        # Add the button layout to the root layout
        root_layout.add_widget(btn_layout)

        return root_layout


MainApp().run()