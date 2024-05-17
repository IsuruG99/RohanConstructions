import database
from utils import message_box


# Load finance logs function
def load_all_finances(status: int = 0) -> list:
    # Get a reference to DB - from database.py
    ref = database.get_ref('finances')

    # Retrieve all finance logs as a list of dictionaries
    finances = []
    for fin_id, finance in ref.get().items():
        if fin_id == 'logZero':
            continue
        finance['id'] = fin_id
        finances.append(finance)

    # 0 is all, 1 is income, 2 is expense
    if status == 0:
        finances = finances
    elif status == 1:
        finances = [finance for finance in finances if finance['type'] == 'Income']
    elif status == 2:
        finances = [finance for finance in finances if finance['type'] == 'Expense']

    return finances


# Get a single finance log function
def get_log(fin_id: str) -> dict:
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Retrieve the finance log data as a dictionary
    finance = ref.child(fin_id).get()

    return finance

# Update finance log function
def edit_log(fin_id: str, fin_type: str, amount: str, date: str, desc: str, entity: str, project: str, category: str,
             user: str = "None") -> bool:
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Update the log data
    if ref is not None:
        #Get reference to child
        ref.child(fin_id).update({
            'type': fin_type,
            'amount': amount,
            'date': date,
            'description': desc,
            'related_entity': entity,
            'project_name': project,
            'category': category,
            'user': user
        })
        return True
    else:
        return False

# Add finance log function
def add_log(fin_type: str, amount: str, date: str, desc: str, entity: str, project: str, category: str,
            user: str = "None") -> bool:
    # Get a reference to DB
    ref = database.get_ref('finances')

    # Add the new log
    if ref is not None:
        # Push (Generate primary key from firebase) & Set (Add data to the key)
        ref.push().set({
            'type': fin_type,
            'amount': amount,
            'date': date,
            'description': desc,
            'related_entity': entity,
            'project_name': project,
            'category': category,
            'user': user
        })
        return True
    else:
        return False

# Delete finance log function
def delete_log(fin_id: str) -> bool:
    # Get a reference to DB
    ref = database.get_ref('finances')
    #Delete the child from the DB
    if ref is not None:
        ref.child(fin_id).delete()
        return True
    else:
        return False
