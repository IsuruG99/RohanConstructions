from utils import *


# Here you will write all in depth functions

def load_resources(status: int = 0) -> list:
    # Get reference from database
    ref = database.get_ref('resources')

    # Retrieve all resources as a list of dictionaries
    res = []
    for res_id, resource in ref.get().items():
        if res_id == 'resourceZero':
            continue
        resource['id'] = res_id
        res.append(resource)

    # 0 is all, 1 is in stock, 2 is out of stock
    if status == 0:
        res = res
    elif status == 1:
        res = [resource for resource in res if resource['status'] == 'In Stock']
    elif status == 2:
        res = [resource for resource in res if resource['status'] == 'Out of Stock']

    return res


# Get a single Resource
def get_res(res_id: str) -> dict:
    # Get a reference to DB
    ref = database.get_ref('resources')

    res = ref.child(res_id).get()
    return res


def update_res(res_id: str, name: str, quantity: str, status: str, supplier_name: str, cost: str) -> bool:
    # Get a reference to DB
    ref = database.get_ref('resources')

    if ref is not None:
        ref.child(res_id).update({
            'name': name,
            'quantity': quantity,
            'status': status,
            'supplier_name': supplier_name,
            'unit_cost': cost
        })
        return True
    else:
        return False


def delete_res(res_id: str) -> bool:
    # Get a reference to DB
    ref = database.get_ref('resources')

    if ref is not None:
        ref.child(res_id).delete()
    else:
        return False
    return True


# Add resource function
def add_res(name: str, quantity: str, status: str, supplier_name: str, cost: str) -> bool:
    # Get a reference to DB
    ref = database.get_ref('resources')

    if ref is not None:
        new_res_ref = ref.push()

        new_res_ref.set({
            'name': name,
            'quantity': quantity,
            'status': status,
            'supplier_name': supplier_name,
            'unit_cost': cost,
            'resource_assignments': [{"amount": "", "project": ""}]
        })
        return True
    else:
        return False


def resource_assignment(res_id: str, amount: str, project_name: str, action: str) -> bool:
    ref = database.get_ref('resources')
    assignments = ref.child(res_id).child('resource_assignments').get()
    if action == "Remove":
        if len(assignments) == 1:
            assignments = [{"amount": "", "project": ""}]
            ref.child(res_id).update({'resource_assignments': assignments})
            change_qty(res_id, amount, "AddQty")
            return True
        else:
            for assignment in assignments:
                if assignment['project'] == project_name:
                    assignments.remove(assignment)
                    ref.child(res_id).update({'resource_assignments': assignments})
                    change_qty(res_id, amount, "AddQty")
                    return True
    elif action == "Add":
        project_exists = False
        for assignment in assignments:
            if assignment['project'] == project_name:
                assignment['amount'] = str(int(assignment['amount']) + int(amount))
                project_exists = True
                break

        if not project_exists:
            assignments.append({"amount": amount, "project": project_name})

        ref.child(res_id).update({'resource_assignments': assignments})
        change_qty(res_id, amount, "SubtractQty")
        return True
    elif action == "Subtract":
        for assignment in assignments:
            if assignment['project'] == project_name:
                if int(assignment['amount']) >= int(amount):
                    assignment['amount'] = str(int(assignment['amount']) - int(amount))
                    ref.child(res_id).update({'resource_assignments': assignments})
                    change_qty(res_id, amount, "AddQty")
                    return True
                else:
                    return False
    else:
        return False

    message_box('Error', 'Failed to connect to Database.')


# Separate function to subtract amount from resource quantity
def change_qty(res_id: str, amount: str, action: str) -> bool:
    if action == "AddQty":
        ref = database.get_ref('resources')
        res = get_res(res_id)
        new_qty = int(res['quantity']) + int(amount)
        ref.child(res_id).update({'quantity': str(new_qty)})
        return True
    elif action == "SubtractQty":
        ref = database.get_ref('resources')
        res = get_res(res_id)
        new_qty = int(res['quantity']) - int(amount)
        ref.child(res_id).update({'quantity': str(new_qty)})
        return True


def calc_resourcesCost(pName: str) -> int:
    res = load_resources()
    cost = 0
    for resource in res:
        for assignment in resource['resource_assignments']:
            if assignment['project'] == pName:
                cost += int(resource['unit_cost']) * int(assignment['amount'])
    return cost

