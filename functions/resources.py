import database
from utils import *


# Here you will write all in depth functions

def load_resources():
    # Get reference from database
    ref = database.get_ref('resources')

    # Retrieve all resources as a list of dictionaries
    res = []
    for res_id, resource in ref.get().items():
        resource['id'] = res_id
        res.append(resource)

    return res


# Get a single Resource
def get_res(res_id):
    # Get a reference to DB
    ref = database.get_ref('resources')

    # Retrieve the resource data as a dictionary
    res = ref.child(res_id).get()

    return res


def update_res(res_id, name, quantity, status, supplier_name, cost):
    # Get a reference to DB
    ref = database.get_ref('resources')

    if ref is not None:
        # Set the res data under the new key
        ref.child(res_id).update({
            'name': name,
            'quantity': quantity,
            'status': status,
            'supplier_name': supplier_name,
            'unit_cost': cost
        })

    else:
        message_box('Error', 'Failed to update resource: "resources" reference not found.')

    print("Resource updated successfully.")
    return True


def delete_res(res_id):
    # Get a reference to DB
    ref = database.get_ref('resources')

    if ref is not None:
        # Delete the Resource
        ref.child(res_id).delete()
    else:
        message_box('Error', 'Failed to delete Resource: "resources" reference not found.')

    print("Resources deleted successfully.")
    return True


# Add resource function
def add_res(name, quantity, status, supplier_name, cost):
    # Get a reference to the 'resources' collection in the database
    ref = database.get_ref('resources')

    if ref is not None:
        # Generate a new unique key for the resource
        new_res_ref = ref.push()

        # Set the resource data under the new key
        new_res_ref.set({
            'name': name,
            'quantity': quantity,
            'status': status,
            'supplier_name': supplier_name,
            'unit_cost': cost
        })

        print("Resource added successfully.")
        return True
    else:
        message_box('Error', 'Failed to add resource: "resources" reference not found.')
        return False
