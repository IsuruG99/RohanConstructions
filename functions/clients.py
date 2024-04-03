import database
from utils import *


# add a new client to the database
def add_client(name, phone_number, email, address, project_name, project_duration, project_status):
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
            'address': address,
            'project_name': project_name,
            'project_duration': project_duration,
            'project_status': project_status
        })
        print("Client added successfully.")
    else:
        message_box('Error', 'Failed to add client: "clients" reference not found.')


# get all clients from the database
def load_clients():
    ref = database.get_ref('clients')
    print("reached load_clients")

    if ref is None:
        message_box('Error', 'Failed to load clients: "clients" reference not found.')
        return []

    # retrieve all clients as a list of dictionaries from the database
    try:
        clients_data = ref.get()
        print("reached clients data")
        if clients_data is None:
            message_box('Error', 'Failed to load clients: No data found.')
            return []

        clients = []
        for client_id, client in clients_data.items():
            client['id'] = client_id
            clients.append(client)
        return clients
    except Exception as e:
        message_box('Error', f'Failed to load clients: {str(e)}')
        return []


# get client by client.id
def get_client(client_id):
    ref = database.get_ref('clients')

    client = ref.child(client_id).get()

    return client


# updating existing client details to the database
def update_client(client_id, name, phone_number, email, address, project_name, project_duration, project_status):
    ref = database.get_ref('clients')

    if ref is not None:
        ref.child(client_id).update({
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'address': address,
            'project_name': project_name,
            'project_duration': project_duration,
            'project_status': project_status
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
