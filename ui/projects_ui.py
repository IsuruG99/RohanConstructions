from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functions.projects import *
from functions.clients import load_client_names
from functions.manpower import calc_manpowerCost
from functions.resources import calc_resourcesCost
from functools import partial
import datetime

from utils import *
from custom import *
from validation import *


# Manages user access to most functions. (Implemented by project leader)
def AccessControl(func):
    def wrapper(self, *args, **kwargs):
        # function validate_access in validation.py takes function's name (string) and returns True/False
        from kivy.app import App
        if App.get_running_app().get_accessLV() is not None:
            accessLV = App.get_running_app().get_accessLV()
            blockList = []
            # Lv2 and 3 can't add/edit and delete anything in Finances.
            # View block is handled by main.py preventing the function opening entirely.
            if accessLV in [2, 3]:
                blockList = ['add_popup', 'editProj', 'deleteProj', 'finalize_projects']
                if accessLV == 3:
                    blockList.append('reports_popup')
            if validate_access(accessLV, func.__name__, blockList):
                return func(self, *args, **kwargs)
            else:
                try:
                    self.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
                except AttributeError:
                    self.projects_screen.CMessageBox('Error', 'You do not have permission \nto access this feature.', 'Message')
    return wrapper


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
        try:
            name = str(self.ids.project_name.text)
            description = str(self.ids.project_desc.text)
            start_date = str(self.ids.project_start.text)
            end_date = str(self.ids.project_end.text)
            client_name = str(self.ids.project_client.text)
            budget = str(self.ids.project_budget.text)
        except AttributeError or ValueError:
            self.projects_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return
        # Validate inputs
        if requestType == "Validate":
            if not validate_string(name, description, client_name, budget):
                self.projects_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_date(start_date, end_date):
                self.projects_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            if not validate_currency(budget):
                self.projects_screen.CMessageBox('Error', 'Invalid budget format.', 'Message')
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
                if add_project(name, description, start_date, end_date, client_name, budget, "In Progress"):
                    self.projects_screen.CMessageBox('Success', 'Project added successfully.', 'Message')
                    self.projects_screen.populate_projects(load_projects(0))
                    self.projects_screen.ids.projects_filter.text = 'Filter: In Progress'
                    self.projects_screen.dismiss_popup(self.popup)
                else:
                    self.projects_screen.CMessageBox('Error', 'Failed to add project.', 'Message')

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
    @AccessControl
    def editProj(self, requestType: str = "Submit") -> None:
        # Stringify inputs (Including Dates)
        try:
            name = str(self.ids.viewPop_name.text)
            description = str(self.ids.viewPop_desc.text)
            start_date = str(self.ids.viewPop_startDate.text)
            end_date = str(self.ids.viewPop_endDate.text)
            client_name = str(self.ids.viewPop_client.text)
            budget = str(self.ids.viewPop_budget.text)
            status = str(self.ids.viewPop_status.text)
        except AttributeError or ValueError:
            self.projects_screen.CMessageBox('Error', 'All fields are required.', 'Message')
            return

        # Validate & Confirm first, then recursively call Submit
        if requestType == "Validate":
            # Validate inputs
            if not validate_string(name, description, client_name, budget, status):
                self.projects_screen.CMessageBox('Error', 'All fields are required.', 'Message')
                return
            if not validate_date(start_date, end_date):
                self.projects_screen.CMessageBox('Error', 'Invalid date format.', 'Message')
                return
            if not validate_currency(budget):
                self.projects_screen.CMessageBox('Error', 'Invalid budget format.', 'Message')
                return
            if name_unique_check('update', name, self.project_id) is False:
                self.projects_screen.CMessageBox('Error', 'Project name must be unique.', 'Message')
                return
            # Send data to projects.py
            self.projects_screen.CMessageBox(title='Update Project',
                                             content='Are you sure you want to update this project?',
                                             context='Confirm', btn1='Yes', btn2='No', btn1click=self.editProj)
            self.validCheck = 1
        # Submit to projects.py
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

    def load_clients(self) -> list:
        return load_client_names()

    # Delete Project
    @AccessControl
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
    def __init__(self, projects_screen: Screen, popup, **kwargs) -> None:
        super().__init__(**kwargs)
        self.projects_screen = projects_screen
        self.populate_reports()
        self.popup = popup
        self.cols = 1
        self.rows = 1

    # We have the Proj_ID, populate the fields
    def populate_reports(self, pName: str = None) -> None:
        # Get the project data from the DB
        self.ids.reportProject_startDate.text = " Unavailable "
        self.ids.reportProject_endDate.text = " Unavailable "
        self.ids.reportProject_status.text = " Unavailable "
        self.ids.reportProject_projectBudget.text = "0"
        self.ids.reportProject_manpowerCost.text = "0"
        self.ids.reportProject_resourceCost.text = "0"
        self.ids.reportProject_netProfit.text = "0"
        self.ids.assigned_manpower.clear_widgets()
        self.ids.assigned_resources.clear_widgets()
        manpower_cost: int = 0
        resource_cost: int = 0
        net_profit: int = 0

        if pName is not None and pName != '':
            # Get relevant manpower data (manpower role, count)
            projects = load_projects()
            for project in projects:
                if project['name'] == pName:
                    self.ids.reportProject_startDate.text = project['start_date']
                    self.ids.reportProject_endDate.text = project['end_date']
                    if project['status'] == 'Completed':
                        self.ids.reportProject_status.text = project['status']
                    else:
                        # Count days left and display days leflt as Y M D left or M D left
                        days_left = (datetime.datetime.strptime(project['end_date'], '%Y-%m-%d') - datetime.datetime.now()).days
                        if days_left > 365:
                            years = days_left // 365
                            months = (days_left % 365) // 30
                            days = (days_left % 365) % 30
                            self.ids.reportProject_status.text = f'{years}Y {months}M {days}D left'
                        elif days_left > 30:
                            months = days_left // 30
                            days = days_left % 30
                            self.ids.reportProject_status.text = f'{months}M {days}D left'
                        else:
                            self.ids.reportProject_status.text = f'{days_left}D left'

                    self.ids.reportProject_projectBudget.text = convert_currency(project['budget'])
                    # costs must be calculated
                    manpower_cost += calc_manpowerCost(pName)
                    resource_cost += calc_resourcesCost(pName)
                    net_profit = int(project['budget']) - manpower_cost - resource_cost
                    self.ids.reportProject_manpowerCost.text = convert_currency(manpower_cost)
                    self.ids.reportProject_resourceCost.text = convert_currency(resource_cost)
                    self.ids.reportProject_netProfit.text = convert_currency(net_profit)

            # Get manpower data (manpower role, count)
            roles = load_members(pName)
            for role, count in roles.items():
                grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=role, font_size='15sp'))
                grid.add_widget(CLabel(text=str(count), font_size='15sp'))
                self.ids.assigned_manpower.add_widget(grid)
            # Get resource data (resource name, amount)
            res = load_res(pName)
            for resource, amount in res.items():
                grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=40)
                grid.add_widget(CLabel(text=resource, font_size='15sp'))
                grid.add_widget(CLabel(text=str(amount), font_size='15sp'))
                self.ids.assigned_resources.add_widget(grid)

    @AccessControl
    def finalize_projects(self, pName: str) -> None:
        if pName is not None and pName != '':
            self.projects_screen.CMessageBox(title='Finalize Project',
                                             content='Are you sure you want to finalize this project?',
                                             context='Confirm', btn1='Yes', btn2='No',
                                             btn1click=partial(finalize_project, pName))
            self.projects_screen.populate_projects(load_projects(0))
            self.projects_screen.ids.projects_filter.text = 'Filter: In Progress'
            self.popup.dismiss()

    def load_projects(self) -> list:
        return load_project_names()

    def dismissPopup(self, instance) -> None:
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

    # Open Message/Confirm Popup Window (Custom Widget implemented by Project Leader)
    def CMessageBox(self, title: str = 'Message', content: str = 'Message Content', context: str = 'Message',
                    btn1: str = 'OK', btn2: str = 'Cancel', btn1click=None, btn2click=None) -> None:
        if context == 'Message':
            msg_popup = MsgPopUp(self, content, context, btn1, btn1click)
            popup = RPopup(title=title, content=msg_popup, size_hint=(0.35, 0.3))
            msg_popup.popup = popup
            popup.open()
        elif context == 'Confirm':
            cfm_popup = CfmPopUp(self, content, context, btn1, btn2, btn1click, btn2click)
            popup = RPopup(title=title, content=cfm_popup, size_hint=(0.35, 0.3))
            cfm_popup.popup = popup
            popup.open()

    # Open Reports Popup Window
    @AccessControl
    def reports_popup(self) -> None:
        temp_reports_popup = Popup()
        reports_popup = ReportsPopup(self, temp_reports_popup)
        reportsPop = RPopup(title='Projects Overview', content=reports_popup, size_hint=(0.6, 0.95))
        reports_popup.popup = reportsPop
        reportsPop.open()

    # Open View Popup Window
    def view_project(self, project_id: str, instance) -> None:
        # The project_id is passed to the ViewPopup Window
        temp_view_popup = Popup()
        view_popup = ViewPopup(self, project_id, temp_view_popup)
        viewPop = RPopup(title='View Project', content=view_popup, size_hint=(0.5, 0.8))
        view_popup.popup = viewPop
        viewPop.open()

    # Open Add Popup Window
    @AccessControl
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
        elif txt == 'Refresh':
            self.populate_projects(load_projects(0))
            self.ids.projects_filter.text = 'Filter: In Progress'
            self.ids.search.text = ''
        elif txt == 'Filter: All' or txt == 'Filter: In Progress' or txt == 'Filter: Completed':
            if txt == 'Filter: In Progress':
                self.populate_projects(load_projects(1))
                self.ids.projects_filter.text = 'Filter: Completed'
                self.ids.search.text = ''
            elif txt == 'Filter: Completed':
                self.populate_projects(load_projects(2))
                self.ids.projects_filter.text = 'Filter: All'
                self.ids.search.text = ''
            elif txt == 'Filter: All':
                self.populate_projects(load_projects(0))
                self.ids.projects_filter.text = 'Filter: In Progress'
                self.ids.search.text = ''
        elif txt == 'Back':
            self.parent.current = 'main'

    def dismiss_popup(self, instance) -> None:
        instance.dismiss()
