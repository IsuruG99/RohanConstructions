import database
from utils import *


# add a new client to the database
def add_client(name, phone_number, email, address):
    # generate a new unique key for the client easily manipulate data
    ref = database.get_ref('clients')

    # check the unique key is unique
    if ref is not None:
        new_client_ref = ref.push()

        # add the client data to the new unique key
        new_client_ref.set({
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'address': address
        })
        return True
    else:
        message_box('Error', 'Failed to add client: "clients" reference not found.')
        return False


# get all clients from the database
def load_clients(status=0):
    ref = database.get_ref('clients')

    clients = []
    for client_id, client in ref.get().items():
        client['id'] = client_id
        clients.append(client)

    if status == 0:
        clients = clients

    return clients


# get client by client.id
def get_client(client_id):
    ref = database.get_ref('clients')

    client = ref.child(client_id).get()

    return client


# updating existing client details to the database
def update_client(client_id, name, phone_number, email, address):
    ref = database.get_ref('clients')

    if ref is not None:
        ref.child(client_id).update({
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'address': address
        })
        print("Client updated successfully.")
        return True
    else:
        message_box('Error', 'Failed to update client: "clients" reference not found.')
        return False


# delete a client by client_id
def delete_client(client_id):
    ref = database.get_ref('clients')

    if ref is not None:
        ref.child(client_id).delete()
        print("Client deleted successfully.")
        return True
    else:
        message_box('Error', 'Failed to delete client: "clients" reference not found.')
        return False


# For other functions, a list of client names
def load_client_names():
    ref = database.get_ref('clients')

    clients = []
    for client_id, client in ref.get().items():
        client['id'] = client_id
        clients.append(client['name'])

    return clients
