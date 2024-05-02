from utils import *


# Add a new client to the database
def add_client(name: str, phone_number: str, email: str, address: str) -> bool:
    ref = database.get_ref('clients')
    if ref is not None:
        new_client_ref = ref.push()
        new_client_ref.set({
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'address': address
        })
        return True
    else:
        return False


# Load all clients from the database
def load_clients(status: int = 0) -> list:
    ref = database.get_ref('clients')

    clients = []
    for client_id, client in ref.get().items():
        if client_id == 'clientZero':
            continue
        client['id'] = client_id
        clients.append(client)

    # Status was implemented for a filter, but not used in the final application
    if status == 0:
        clients = clients

    return clients


# Retrieve a client by client_id
def get_client(client_id: str) -> dict:
    ref = database.get_ref('clients')

    client = ref.child(client_id).get()
    return client


# Updates existing client details to the database
def update_client(client_id: str, name: str, phone_number: str, email: str, address: str) -> bool:
    ref = database.get_ref('clients')

    if ref is not None:
        ref.child(client_id).update({
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'address': address
        })
        return True
    else:
        return False


# Delete a client by client_id
def delete_client(client_id: str) -> bool:
    ref = database.get_ref('clients')

    if ref is not None:
        ref.child(client_id).delete()
        return True
    else:
        return False


# Load all client names from the database
def load_client_names() -> list:
    clientList = load_clients()

    clients = []
    for client_id, client in clientList:
        client['id'] = client_id
        clients.append(client['name'])

    return clients
