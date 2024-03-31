import database
from utils import message_box


def load_all_finances():
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Retrieve all finance logs as a list of dictionaries
    finances = []
    for fin_id, finance in ref.get().items():
        finance['id'] = fin_id
        finances.append(finance)

    return finances


def get_log(fin_id):
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Retrieve the finance log data as a dictionary
    finance = ref.child(fin_id).get()

    return finance


def edit_log(fin_id, fin_type, amount, date, desc, entity, project, category):
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Update the log data
    if ref is not None:
        ref.child(fin_id).update({
            'type': fin_type,
            'amount': amount,
            'date': date,
            'description': desc,
            'related_entity': entity,
            'project_name': project,
            'category': category
        })
    else:
        message_box('Error', 'Failed to update log: "finances" reference not found.')

    print("Log updated successfully.")
    return True


def add_log(fin_type, amount, date, desc, entity, project, category):
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Add the new log
    if ref is not None:
        # push and set
        ref.push().set({
            'type': fin_type,
            'amount': amount,
            'date': date,
            'description': desc,
            'related_entity': entity,
            'project_name': project,
            'category': category
        })

    else:
        message_box('Error', 'Failed to add log: "finances" reference not found.')

    print("Log added successfully.")
    return True

def delete_log(fin_id):
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Delete the log
    if ref is not None:
        ref.child(fin_id).delete()
    else:
        message_box('Error', 'Failed to delete log: "finances" reference not found.')

    print("Log deleted successfully.")
    return True
