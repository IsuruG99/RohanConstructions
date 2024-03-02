import database
from utils import message_box


# check if the user is valid

def checkCredentials(email, password):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email and users[user]['password'] == password:
            return True

    return False

