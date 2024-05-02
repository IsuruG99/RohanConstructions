from database import *
from utils import *


# Load manpower function
def load_manpower(status: int = 0) -> list:
    # Get reference from database
    ref = get_ref('manpower')
    if ref is not None:
        # Retrieve all manpower as a list of dictionaries
        manpower = []
        for emp_id, employee in ref.get().items():
            if emp_id == 'empZero':
                continue
            employee['id'] = emp_id
            manpower.append(employee)

        if status == 0:
            manpower = manpower
        elif status == 1:
            manpower = [employee for employee in manpower if employee['employment_status'] == 'Permanent']
        elif status == 2:
            manpower = [employee for employee in manpower if employee['employment_status'] == 'Temp']

    else:
        manpower = [{'email': 'None', 'employment_status': 'None', 'name': 'None', 'phone_number': 'None',
                     'project_assignments': [], 'role': 'None', 'contract_fee': 'None', 'retainer_fee': 'None'}]
    return manpower


# Get a single employee function
def get_employee(emp_id: str) -> dict:
    ref = get_ref('manpower')

    # Retrieve the employee data as a dictionary
    employee = ref.child(emp_id).get()
    return employee


# Update employee function
def update_employee(emp_id: str, name: str, role: str, email: str, phone_number: str, employment_status: str,
                    contract_fee: str, retainer_fee:str) -> bool:
    ref = get_ref('manpower')

    if ref is not None:
        ref.child(emp_id).update({
            'name': name,
            'role': role,
            'email': email,
            'phone_number': phone_number,
            'employment_status': employment_status,
            'contract_fee': contract_fee,
            'retainer_fee': retainer_fee
        })
        return True
    else:
        # Reference not found
        return False


# Delete employee function
def delete_employee(emp_id: str) -> bool:
    ref = get_ref('manpower')

    if ref is not None:
        ref.child(emp_id).delete()
        return True
    else:
        # Reference not found
        return False


def project_assignment(emp_id: str, project_name: str, action: str) -> bool:
    ref = get_ref('manpower')
    assignments = ref.child(emp_id).child('project_assignments').get()
    if ref is not None:
        if action == "Remove":
            # if assignments count is 1, replace the assignments with an empty list
            if len(assignments) == 1:
                assignments = [""]
                ref.child(emp_id).update({'project_assignments': assignments})
            else:
                if project_name in assignments:
                    assignments.remove(project_name)
                    ref.child(emp_id).update({'project_assignments': assignments})
                else:
                    print("Project not found in employee assignments.")
                    return False

            print("Project removed from employee successfully.")
            return True
        elif action == "Add":
            if project_name not in assignments:
                assignments.append(project_name)
                ref.child(emp_id).update({'project_assignments': assignments})
                return True
            else:
                # Project Already Exists
                return False
        else:
            # Invalid Action
            return False
    else:
        # Reference not found
        return False


# Add employee function
def add_employee(name: str, role: str, email: str, phone_number: str, employment_status: str, project_assignments: list,
                 contract_fee: str, retainer_fee: str) -> bool:
    ref = get_ref('manpower')
    if ref is not None:
        new_emp_ref = ref.push()

        new_emp_ref.set({
            'name': name,
            'role': role,
            'email': email,
            'phone_number': phone_number,
            'employment_status': employment_status,
            'project_assignments': project_assignments,
            'contract_fee': contract_fee,
            'retainer_fee': retainer_fee
        })

        return True
    else:
        message_box('Error', 'Failed to add employee: "manpower" reference not found.')
        return False

# For project Overview
def calc_manpowerCost(pName: str) -> int:
    manpower = load_manpower()
    cost = 0
    for employee in manpower:
        if pName in employee['project_assignments']:
            cost += int(employee['contract_fee'])
    return cost