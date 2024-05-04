from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from utils import *
from custom import *
from validation import *

from functions.archive import *
from functions.projects import load_projects, load_project_names

import datetime


class AddArchive(GridLayout):
    def __init__(self, archiveScreen: Screen, popup, **kwargs):
        super().__init__(**kwargs)
        self.archiveScreen = archiveScreen

        self.popup = popup
        self.cols = 1
        self.rows = 1

    def dismiss_popup(self):
        self.popup.dismiss()

class ViewArchive(GridLayout):
    def __init__(self, archiveScreen: Screen, popup, archive_id: str, **kwargs):
        super().__init__(**kwargs)
        self.archiveScreen = archiveScreen
        self.popup = popup
        self.cols = 1
        self.rows = 1
        self.archive_id = archive_id
        self.populate_view()

    def populate_view(self):
        archive = get_archive(self.archive_id)
        self.ids.viewArchive_client.text = archive['client_name']
        self.ids.viewArchive_start.text = archive['start_date']
        self.ids.viewArchive_end.text = archive['end_date']
        self.ids.viewArchive_user.text = archive['user']
        self.ids.viewArchive_desc.text = archive['description']

        # Manpower Assignment from "employee_allocations": [
        #         {
        #           "role": "Architect",
        #           "count": "2"
        #         },
        #         {
        #           "role": "Site Engineer",
        #           "count": "5"
        #         }
        #       ],
        #       "resource_allocations": [
        #         {
        #           "resource": "Cement",
        #           "amount": "100"
        #         }]
        for employee in archive['employee_allocations']:
            if employee['count'] is not None:
                grid = GridLayout(cols=2, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=employee['role'], size_hint_x=0.5))
                grid.add_widget(CLabel(text=employee['count'], size_hint_x=0.5))
                self.ids.viewArchive_assignedEmp.add_widget(grid)

        for resource in archive['resource_allocations']:
            if resource['amount'] is not None and resource['resource'] is not None:
                grid = GridLayout(cols=2, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=resource['resource'], size_hint_x=0.5))
                grid.add_widget(CLabel(text=resource['amount'], size_hint_x=0.5))
                self.ids.viewArchive_assignedRes.add_widget(grid)


        self.ids.viewArchive_budget.text = archive['budget']
        self.ids.viewArchive_resCost.text = archive['resourceCost']
        self.ids.viewArchive_empCost.text = archive['manpowerCost']
        self.ids.viewArchive_netProfit.text = archive['netProfit']


    def dismiss_popup(self):
        self.popup.dismiss()


class ArchiveScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_archive(load_all_archives(0))

    def populate_archive(self, archiveList: list = load_all_archives(), headers: list = None) -> None:
        self.ids.archive_list.clear_widgets()
        self.ids.archive_headers.clear_widgets()
        if headers is None:
            headers = ["Project", "Client", "Date", "Budget"]
        size_hints = [0.3, 0.2, 0.2, 0.3]
        for header in headers:
            self.ids.archive_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sortArchive, header, archiveList)))

        for archive in archiveList:
            grid = GridLayout(cols=4, size_hint_y=None, height=40)
            button = Button(text=archive["name"], on_release=partial(self.viewArchive, archive["id"], archive["name"]),
                            background_normal='', font_size='20sp', size_hint_x=0.3,
                            background_color=(0.1, 0.1, 0.1, 0.0), font_name='Roboto', color=(1, 1, 1, 1),
                            bold=True)
            grid.archive = archive
            grid.add_widget(button)
            grid.add_widget(CLabel(text=archive["client_name"], size_hint_x=0.2))
            grid.add_widget(CLabel(text=archive["end_date"], size_hint_x=0.2))
            grid.add_widget(CLabel(text=convert_currency(archive["budget"]), size_hint_x=0.3))
            self.ids.archive_list.add_widget(grid)

    def addArchive(self) -> None:
        temp_addArchive = Popup()
        addArchive = AddArchive(self, temp_addArchive)
        addArch = RPopup(title="Add Archive", content=addArchive, size_hint=(0.8, 0.8))
        addArchive.popup = addArch
        addArch.open()

    def viewArchive(self, archive_id: str, aName:str, instance) -> None:
        temp_viewArchive = Popup()
        viewArchive = ViewArchive(self, temp_viewArchive, archive_id)
        viewArch = RPopup(title=aName, content=viewArchive, size_hint=(0.55, 0.95))
        viewArchive.popup = viewArch
        viewArch.open()

    def sortArchive(self, header: str, archives: list, instance) -> list:
        if header == 'Project' or header == 'Project [D]':
            archives = sorted(archives, key=lambda x: x['name'])
            self.populate_archive(archives, headers=['Project [A]', 'Client', 'Date', 'Budget'])
        elif header == 'Client' or header == 'Client [D]':
            archives = sorted(archives, key=lambda x: x['client_name'])
            self.populate_archive(archives, headers=['Project', 'Client [A]', 'Date', 'Budget'])
        elif header == 'Date' or header == 'Date [D]':
            archives = sorted(archives, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'))
            self.populate_archive(archives, headers=['Project', 'Client', 'Date [A]', 'Budget'])
        elif header == 'Budget' or header == 'Budget [D]':
            archives = sorted(archives, key=lambda x: currencyStringToFloat(x['budget']))
            self.populate_archive(archives, headers=['Project', 'Client', 'Date', 'Budget [A]'])
        elif header == 'Project [A]':
            archives = sorted(archives, key=lambda x: x['name'], reverse=True)
            self.populate_archive(archives, headers=['Project [D]', 'Client', 'Date', 'Budget'])
        elif header == 'Client [A]':
            archives = sorted(archives, key=lambda x: x['client_name'], reverse=True)
            self.populate_archive(archives, headers=['Project', 'Client [D]', 'Date', 'Budget'])
        elif header == 'Date [A]':
            archives = sorted(archives, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'),
                              reverse=True)
            self.populate_archive(archives, headers=['Project', 'Client', 'Date [D]', 'Budget'])
        elif header == 'Budget [A]':
            archives = sorted(archives, key=lambda x: currencyStringToFloat(x['budget']), reverse=True)
            self.populate_archive(archives, headers=['Project', 'Client', 'Date', 'Budget [D]'])

    def searchArchive(self, query: str) -> list:
        if not query == "":
            archives = load_all_archives(0)
            archives = [archive for archive in archives if query.lower() in archive['name'].lower() or query.lower() in
                        archive['client_name'].lower() or query.lower() in archive['budget'].lower()]
            self.populate_archive(archives)

    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'None',
                    btn1: str = 'Ok', btn2: str = 'Cancel',
                    btn1click=None, btn2click=None) -> None:
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

    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == "Add":
            self.addArchive()
        elif txt == "Refresh":
            self.populate_archive(load_all_archives(0))
            self.ids.search.text = ""
        elif txt == "Filter: All":
            pass
        elif txt == "Back":
            self.manager.current = "main"
