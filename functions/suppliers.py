import database
from utils import *


def load_suppliers():
    # Get a reference to Database
    ref = database.get_ref('suppliers')

    # Retrieve all suppliers as a list of dictionaries
    suppliers = []
    for supplier_id, supplier in ref.get().items():
        supplier['id'] = supplier_id
        suppliers.append(supplier)

    return suppliers


# Adding new supplier
def add_supplier(supplierName, business, contactNo, email, address, startDealing, supplierLevel):
    # Get a reference to Database
    ref = database.get_ref('suppliers')

    if ref is not None:
        # Generate unique key for the new supplier
        new_supplier_ref = ref.push()

        # Set the supplier data under the new key
        new_supplier_ref.set(
            {
                'supplierName': supplierName,
                'business': business,
                'contactNo': contactNo,
                'email': email,
                'address': address,
                'startDealing': startDealing,
                'supplierLevel': supplierLevel
            })

    else:
        message_box('Error', 'New supplier adding fail !: "suppliers" reference not found.')


# Get a single supplier by ID
def get_supplier(sp_id):
    # Get a reference to DB
    ref = database.get_ref('suppliers')

    # Retrieve the supplier data as a dictionary
    sup = ref.child(sp_id).get()

    return sup


def edit_supplier(sup_id, supplierName, business, contactNo, email, address, startDealing, supplierLevel):
    # Get a reference to Database
    ref = database.get_ref('suppliers')

    if ref is not None:
        ref.child(sup_id).update(
            {
                'supplierName': supplierName,
                'business': business,
                'contactNo': contactNo,
                'email': email,
                'address': address,
                'startDealing': startDealing,
                'supplierLevel': supplierLevel
            })
        message_box('Success', 'Supplier edited')

    else:
        message_box('Error', 'Failed to connect to database.')


def delete_supplier(sup_id):
    ref = database.get_ref('suppliers')
    if ref is not None:
        ref.child(sup_id).delete()
        message_box('Success', 'Supplier deleted')
    else:
        message_box('Error', 'Failed to connect to database.')

