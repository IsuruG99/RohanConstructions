from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import *
from functions.clients import load_client_names
from functools import partial
import datetime

from utils import *
from custom import *
from validation import *


# Add Project Popup Window
class AddPopup(GridLayout):
    def __init__(self, projects_screen: Screen, popup, **kwargs) -> None:
        super().__init__(**kwargs)
        self.projects_screen = projects_screen
        self.popup = popup
        self.validCheck = 0
        self.cols = 1
        self.rows = 1

    def addProj(self, requestType: str = "Submit") -> None:
        # Stringify Inputs
        name = str(self.ids.project_name.text)
        description = str(self.ids.project_desc.text)
        start_date = str(self.ids.project_start.text)
        end_date = str(self.ids.project_end.text)
        client_name = str(self.ids.project_client.text)
        budget = str(self.ids.project_budget.text)
        # Validate inputs
        if requestType == "Validate":
            if not validate_string(name, description, client_name, budget):
                message_box('Error', 'All fields are required.')
                return
            if not validate_date(start_date, end_date):
                message_box('Error', 'Invalid date format.')
                return
            if name_unique_check('add', name) is False:
                message_box('Error', 'Project name must be unique.')
                return
            # Send data to projects.py
            self.projects_screen.CMessageBox(title='Add Project', content='Are you sure you want to add this project?',
                                             context='Confirm', btn1='Yes', btn2='No', btn1click=self.addProj)
            self.validCheck = 1
        if requestType == "Submit":
            if self.validCheck == 1:
                add_project(name, description, start_date, end_date, client_name, budget, "In Progress")
                self.projects_screen.CMessageBox('Success', 'Project added successfully.', 'Message')
                self.projects_screen.populate_projects(load_projects(0))
                self.projects_screen.ids.projects_filter.text = 'Filter: In Progress'
                self.projects_screen.dismiss_popup(self.popup)

    def load_clients(self) -> list:
        return load_client_names()


# View Project Popup Window
class ViewPopup(GridLayout):
    def __init__(self, projects_screen: Screen, project_id: str, popup, **kwargs):
        super().__init__(**kwargs)
        self.project_id = project_id
        self.populate_view()
        self.projects_screen = projects_screen
        self.popup = popup
        self.validCheck = 0
        self.cols = 1
        self.rows = 1

    # Populate PopUp Window
    def populate_view(self) -> None:
        # Get the project data from the DB
        project = get_project(self.project_id)
        # Assign
        self.ids.viewPop_name.text = project["name"]
        self.ids.viewPop_desc.text = project["description"]
        self.ids.viewPop_startDate.text = project["start_date"]
        self.ids.viewPop_endDate.text = project["end_date"]
        self.ids.viewPop_client.text = project["client_name"]
        self.ids.viewPop_budget.text = str(project["budget"])
        self.ids.viewPop_status.text = project["status"]

    # Edit Project
    def editProj(self, requestType: str = "Submit") -> None:
        # Stringify inputs (Including Dates)
        name = str(self.ids.viewPop_name.text)
        description = str(self.ids.viewPop_desc.text)
        start_date = str(self.ids.viewPop_startDate.text)
        end_date = str(self.ids.viewPop_endDate.text)
        client_name = str(self.ids.viewPop_client.text)
        budget = str(self.ids.viewPop_budget.text)
        status = str(self.ids.viewPop_status.text)

        if requestType == "Validate":
            # Validate inputs
            if not validate_string(name, description, client_name, budget, status):
                self.projects_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_date(start_date, end_date):
                self.projects_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            if name_unique_check('update', name, self.project_id) is False:
                self.projects_screen.CMessageBox('Error', 'Project name must be unique.', 'Message')
                return
            # Send data to projects.py
            self.projects_screen.CMessageBox(title='Update Project',
                                             content='Are you sure you want to update this project?',
                                             context='Confirm', btn1='Yes', btn2='No', btn1click=self.editProj)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                if update_project(self.project_id, name, description, start_date, end_date, client_name, budget,
                                  status):
                    self.projects_screen.CMessageBox('Success', 'Project updated successfully.', 'Message')
                    self.validCheck = 0
                    self.projects_screen.populate_projects(load_projects(0))
                    self.projects_screen.ids.projects_filter.text = 'Filter: In Progress'
                    self.projects_screen.dismiss_popup(self.popup)
                else:
                    self.validCheck = 0
                    self.projects_screen.CMessageBox('Error', 'Failed to update project.', 'Message')

    # Open Reports Popup Window
    def reports_popup(self, project_name: str) -> None:
        self.projects_screen.dismiss_popup(self.popup)
        temp_reports_popup = Popup()
        reports_popup = ReportsPopup(self.projects_screen, self.project_id, temp_reports_popup)
        reportsPop = RPopup(title=project_name, content=reports_popup, size_hint=(0.6, 0.95))
        reports_popup.popup = reportsPop
        reportsPop.open()

    def load_clients(self) -> list:
        return load_client_names()

    # Delete Project
    def deleteProj(self, requestType: str = "Submit") -> None:
        if requestType == "Validate":
            # Send project_id to projects.py
            self.projects_screen.CMessageBox(title='Delete Project',
                                             content='Are you sure you want to delete this project?',
                                             context='Confirm', btn1='Yes', btn2='No', btn1click=self.deleteProj)
            self.validCheck = 1
        elif requestType == "Submit":
            if self.validCheck == 1:
                if delete_project(self.project_id):
                    self.projects_screen.CMessageBox('Success', 'Project deleted successfully.', 'Message')
                else:
                    self.projects_screen.CMessageBox('Error', 'Failed to delete project.', 'Message')
                self.validCheck = 0
                self.projects_screen.populate_projects(load_projects(0))
                self.projects_screen.ids.projects_filter.text = 'Filter: In Progress'
                self.projects_screen.dismiss_popup(self.popup)

    def dismiss_popup(self, instance) -> None:
        self.projects_screen.dismiss_popup(self.popup)


class ReportsPopup(GridLayout):
    def __init__(self, projects_screen: Screen, proj_id: str, popup, **kwargs) -> None:
        super().__init__(**kwargs)
        self.projects_screen = projects_screen
        self.populate_reports(proj_id)
        self.popup = popup
        self.cols = 1
        self.rows = 1

    # We have the Proj_ID, populate the fields
    def populate_reports(self, pid: str) -> None:
        # Get the project data from the DB
        project = get_project(pid)

        # Assign
        self.ids.proj_desc.text = project["description"]
        self.ids.proj_start.text = project["start_date"]
        self.ids.proj_end.text = project["end_date"]
        self.ids.proj_client.text = project["client_name"]
        self.ids.proj_budget.text = str(project["budget"])
        # Get relevant manpower data (manpower role, count)
        roles = load_members(project["name"])
        for role, count in roles.items():
            grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
            grid.add_widget(CLabel(text=role, font_size='15sp'))
            grid.add_widget(CLabel(text=str(count), font_size='15sp'))
            self.ids.assigned_manpower.add_widget(grid)
        # Get resource data (resource name, amount)
        res = load_res(project["name"])
        for resource, amount in res.items():
            grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
            grid.add_widget(CLabel(text=resource, font_size='15sp'))
            grid.add_widget(CLabel(text=str(amount), font_size='15sp'))
            self.ids.assigned_resources.add_widget(grid)

    def dismissPopup(self,instance) -> None:
        self.popup.dismiss()


# Projects Main UI (Accessed by main.py)
class ProjectsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_projects(load_projects(0))


    # Populate the ScrollView with the projects
    def populate_projects(self, projects: list = load_projects(0), headers: list = None) -> None:
        # Clear the ScrollView
        self.ids.projects_list.clear_widgets()
        self.ids.projects_headers.clear_widgets()

        # Create Headers
        if headers is None:
            headers = ['Project Name', 'Client', 'End Date', 'Status']
        size_hints = [0.4, 0.3, 0.15, 0.15]
        for header in headers:
            self.ids.projects_headers.add_widget(
                CButton(text=header, bold=True, padding=(10, 10), size_hint_x=size_hints[headers.index(header)],
                        on_release=partial(self.sort_projects, header, projects)))

        # Fill the Grid with Project Data
        for project in projects:
            grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=40)
            button = Button(text=project["name"], on_release=partial(self.view_project, project["id"]),
                            background_normal='', font_size='20sp', size_hint_x=0.4,
                            background_color=(0.1, 0.1, 0.1, 0.0), font_name='Roboto', color=(1, 1, 1, 1),
                            bold=True)
            grid.project = project
            grid.add_widget(button)
            grid.add_widget(CLabel(text=project["client_name"], size_hint_x=0.3))
            grid.add_widget(CLabel(text=project["end_date"], size_hint_x=0.15))
            grid.add_widget(CLabel(text=project["status"], size_hint_x=0.15))
            self.ids.projects_list.add_widget(grid)

    # Sort Projects, called by the header buttons, calls populate_projects with matching Projects List
    def sort_projects(self, header: str, projects: list, instance) -> None:
        # Sort by header
        if header == 'Project Name' or header == 'Project Name [D]':
            projects = sorted(projects, key=lambda x: x['name'])
            self.populate_projects(projects, headers=['Project Name [A]', 'Client', 'End Date', 'Status'])
        elif header == 'Client' or header == 'Client [D]':
            projects = sorted(projects, key=lambda x: x['client_name'])
            self.populate_projects(projects, headers=['Project Name', 'Client [A]', 'End Date', 'Status'])
        elif header == 'End Date' or header == 'End Date [D]':
            projects = sorted(projects, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'))
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date [A]', 'Status'])
        elif header == 'Status' or header == 'Status [D]':
            projects = sorted(projects, key=lambda x: x['status'])
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date', 'Status [A]'])
        elif header == 'Project Name [A]':
            projects = sorted(projects, key=lambda x: x['name'], reverse=True)
            self.populate_projects(projects, headers=['Project Name [D]', 'Client', 'End Date', 'Status'])
        elif header == 'Client [A]':
            projects = sorted(projects, key=lambda x: x['client_name'], reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client [D]', 'End Date', 'Status'])
        elif header == 'End Date [A]':
            projects = sorted(projects, key=lambda x: datetime.datetime.strptime(x['end_date'], '%Y-%m-%d'),
                              reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date [D]', 'Status'])
        elif header == 'Status [A]':
            projects = sorted(projects, key=lambda x: x['status'], reverse=True)
            self.populate_projects(projects, headers=['Project Name', 'Client', 'End Date', 'Status [D]'])

    # Search Projects by given String, calls populate_projects with matching Projects List
    def searchProj(self, searchValue: str) -> None:
        if not searchValue == '':
            projects = load_projects(0)
            projects = [project for project in projects if searchValue.lower() in project['name'].lower() or
                        searchValue.lower() in project['client_name'].lower() or searchValue.lower() in
                        project['end_date'].lower()]
            self.populate_projects(projects)

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

    # Open View Popup Window
    def view_project(self, project_id: str, instance) -> None:
        # The project_id is passed to the ViewPopup Window
        temp_view_popup = Popup()
        view_popup = ViewPopup(self, project_id, temp_view_popup)
        viewPop = RPopup(title='View Project', content=view_popup, size_hint=(0.5, 0.8))
        view_popup.popup = viewPop
        viewPop.open()

    # Open Add Popup Window
    def add_popup(self) -> None:
        temp_add_popup = Popup()
        add_popup = AddPopup(self, temp_add_popup)
        addPop = RPopup(title='Add Project', content=add_popup, size_hint=(0.5, 0.8))
        add_popup.popup = addPop
        addPop.open()

    # Button Click Event Handler
    def btn_click(self, instance) -> None:
        txt = instance.text
        if txt == 'Add':
            self.add_popup()
        elif txt == 'Filter: All' or txt == 'Filter: In Progress' or txt == 'Filter: Completed':
            if txt == 'Filter: In Progress':
                self.populate_projects(load_projects(1))
                self.ids.projects_filter.text = 'Filter: Completed'
            elif txt == 'Filter: Completed':
                self.populate_projects(load_projects(2))
                self.ids.projects_filter.text = 'Filter: All'
            elif txt == 'Filter: All':
                self.populate_projects(load_projects(0))
                self.ids.projects_filter.text = 'Filter: In Progress'
        elif txt == 'Back':
            self.parent.current = 'main'

    # Font Size Adjustment Test
    #     def fontSizer(self, instance):
    #         for grid in self.ids.projects_list.children:
    #             for child in grid.children:
    #                 if isinstance(child, (Label, Button)):
    #                     if instance.text == '+':
    #                         child.font_size += 5
    #                     else:
    #                         child.font_size -= 5
    #                     child.size_hint_y = None
    #                     child.texture_update()
    #                     child.size = child.texture_size

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()
