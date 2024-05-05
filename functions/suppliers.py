from utils import *

# Load all suppliers
def load_suppliers(status: int = 0) -> list:
    ref = database.get_ref('suppliers')

    # Retrieve all suppliers
    suppliers = []
    for supplier_id, supplier in ref.get().items():
        if supplier_id == 'supplierZero':
            continue
        supplier['id'] = supplier_id
        suppliers.append(supplier)

    # Check if supplier level is equal to the given status of 1 2 or 3 otherwise provide all suppliers
    if status in [1, 2, 3]:
        suppliers = [supplier for supplier in suppliers if supplier['supplierLevel'] == str(status)]
    return suppliers


# Adding new supplier
def add_supplier(supplierName: str, business: str, contactNo: str, email: str, address: str, startDealing: str,
                 supplierLevel: str) -> bool:
    ref = database.get_ref('suppliers')

    if ref is not None:
        new_supplier_ref = ref.push()
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
        return True
    else:
        return False


# Get a single supplier by ID
def get_supplier(suppliers_id: str) -> dict:
    ref = database.get_ref('suppliers')
    supplier = ref.child(suppliers_id).get()
    return supplier


# Update supplier details
def edit_supplier(suppliers_id: str, supplierName: str, business: str, contactNo: str, email: str, address: str,
                  startDealing: str, supplierLevel: str) -> bool:
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
        return False


# Delete a supplier by ID
def delete_supplier(suppliers_id: str) -> bool:
    ref = database.get_ref('suppliers')

    if ref is not None:
        ref.child(suppliers_id).delete()
        return True
    else:
        return False


# Return a list of supplier names for other functions
def load_supplier_names() -> list:
    load_suppliers(0)
    supplier_names = []
    for supplier in load_suppliers(0):
        supplier_names.append(supplier['supplierName'])
    return supplier_names
