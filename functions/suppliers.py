import database
from utils import *


def load_suppliers(status=0):
    # Get a reference to Database
    ref = database.get_ref('suppliers')

    # Retrieve all suppliers as a list of dictionaries
    suppliers = []
    for supplier_id, supplier in ref.get().items():
        supplier['id'] = supplier_id
        suppliers.append(supplier)

    if status == 0:
        suppliers = suppliers
    elif status == 1:
        suppliers = [supplier for supplier in suppliers if supplier['supplierLevel'] == '1']
    elif status == 2:
        suppliers = [supplier for supplier in suppliers if supplier['supplierLevel'] == '2']
    elif status == 3:
        suppliers = [supplier for supplier in suppliers if supplier['supplierLevel'] == '3']

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
def get_supplier(suppliers_id):
    # Get a reference to DB
    ref = database.get_ref('suppliers')

    # Retrieve the supplier data as a dictionary
    supplier = ref.child(suppliers_id).get()

    return supplier


def edit_supplier(suppliers_id, supplierName, business, contactNo, email, address, startDealing, supplierLevel):
    # Get a reference to Database
    ref = database.get_ref('suppliers')

    if ref is not None:
        ref.child(suppliers_id).update(
            {
                'supplierName': supplierName,
                'business': business,
                'contactNo': contactNo,
                'email': email,
                'address': address,
                'startDealing': startDealing,
                'supplierLevel': supplierLevel
            })
        return True
    else:
        message_box('Error', 'Failed to connect to database.')
        return False


def delete_supplier(suppliers_id):
    ref = database.get_ref('suppliers')

    if ref is not None:
        ref.child(suppliers_id).delete()
        return True
    else:
        message_box('Error', 'Failed to connect to database.')
        return False