from database import *
from utils import *


# Load manpower function
def load_manpower(status=0):
    # Get reference from database
    ref = get_ref('manpower')

    # Retrieve all manpower as a list of dictionaries
    manpower = []
    for emp_id, employee in ref.get().items():
        employee['id'] = emp_id
        manpower.append(employee)

    if status == 0:
        manpower = manpower
    elif status == 1:
        manpower = [employee for employee in manpower if employee['employment_status'] == 'Permanent']
    elif status == 2:
        manpower = [employee for employee in manpower if employee['employment_status'] == 'Temp']

    return manpower


# Get a single employee function
def get_employee(emp_id):
    # Get a reference to DB
    ref = get_ref('manpower')

    # Retrieve the employee data as a dictionary
    employee = ref.child(emp_id).get()

    return employee


# Update employee function
def update_employee(emp_id, name, role, email, phone_number, employment_status, salary):
    # Get a reference to DB
    ref = get_ref('manpower')

    if ref is not None:
        # Set the employee data under the new key
        ref.child(emp_id).update({
            'name': name,
            'role': role,
            'email': email,
            'phone_number': phone_number,
            'employment_status': employment_status,
            'salary': salary
        })

        print("Employee updated successfully.")
        return True
    else:
        message_box('Error', 'Failed to update employee: "manpower" reference not found.')
        return False


# Delete employee function
def delete_employee(emp_id):
    # Get a reference to DB
    ref = get_ref('manpower')

    if ref is not None:
        # Delete the employee
        ref.child(emp_id).delete()
        print("Employee deleted successfully.")
        return True
    else:
        message_box('Error', 'Failed to delete employee: "manpower" reference not found.')
        return False


def project_assignment(emp_id, project_name, action):
    ref = get_ref('manpower')
    assignments = ref.child(emp_id).child('project_assignments').get()
    print(assignments)
    if ref is not None:
        if action == "Remove":
            # if assignments count is 1, replace the assignments with an empty list
            if len(assignments) == 1:
                assignments = [""]
                ref.child(emp_id).update({'project_assignments': assignments})
            else:
                assignments.remove(project_name)
                ref.child(emp_id).update({'project_assignments': assignments})

            print("Project removed from employee successfully.")
            return True
        elif action == "Add":
            assignments.append(project_name)
            ref.child(emp_id).update({'project_assignments': assignments})

            print("Project added to employee successfully.")
            return True
        else:
            message_box('Error', 'Failed to perform action')
            return False
    else:
        message_box('Error', 'Failed to connect to Database.')
        return False


# Add employee function
def add_employee(name, role, email, phone_number, employment_status, project_assignments, salary):
    # Get a reference to the 'manpower' collection in the database
    ref = get_ref('manpower')

    if ref is not None:
        # Generate a new unique key for the employee
        new_emp_ref = ref.push()

        # Set the employee data under the new key
        new_emp_ref.set({
            'name': name,
            'role': role,
            'email': email,
            'phone_number': phone_number,
            'employment_status': employment_status,
            'project_assignments': project_assignments,
            'salary': salary
        })

        print("Employee added successfully.")
        return True
    else:
        message_box('Error', 'Failed to add employee: "manpower" reference not found.')
        return False
