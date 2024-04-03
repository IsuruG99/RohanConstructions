from database import *
from utils import *


# Load manpower function
def load_manpower():
    # Get reference from database
    ref = get_ref('manpower')

    # Retrieve all manpower as a list of dictionaries
    manpower = []
    for emp_id, employee in ref.get().items():
        employee['id'] = emp_id
        manpower.append(employee)

    return manpower

# Get a single employee function
def get_employee(emp_id):
    # Get a reference to DB
    ref = get_ref('manpower')

    # Retrieve the employee data as a dictionary
    employee = ref.child(emp_id).get()

    return employee

# Update employee function
def update_employee(emp_id, name, role, email, phone_number, employment_status, project_assignments):
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
            'project_assignments': project_assignments
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

# Add employee function
def add_employee(name, role, email, phone_number, employment_status, project_assignments):
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
            'project_assignments': project_assignments
        })

        print("Employee added successfully.")
        return True
    else:
        message_box('Error', 'Failed to add employee: "manpower" reference not found.')
        return False
