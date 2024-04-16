from datetime import datetime

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


def getAccessLV(email):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            return users[user]['access']

    return False


def getAccessName(email):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            return users[user]['email']

    return False


def load_users(status=0):
    # Make a dictionary of users
    ref = database.get_ref('users')
    users = []
    for user_id, user in ref.get().items():
        user['id'] = user_id
        users.append(user)

    if status == 0:
        return users
    elif status == 1:
        return [user for user in users if user['access'] == 1]
    elif status == 2:
        return [user for user in users if user['access'] == 2]
    elif status == 3:
        return [user for user in users if user['access'] == 3]


def get_user(user_id):
    ref = database.get_ref('users')
    user = ref.child(user_id).get()
    return user


# Used when a user logs in, to store "last_login": "2024-04-12T08:00:00.000Z" format
# to the user's data in the database
# Get the time from current time and date on Sri Lanka.
def update_last_login(email):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            ref.child(user).update({"last_login": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')})
            return


def edit_user(email, password, access):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        print("DB Email:" + users[user]['email'] + " == " + email + "Our Email")
        if users[user]['email'] == email:
            print(user, email, password, access)
            ref.child(user).update({"password": password, "access": access})
            return True
    else:
        message_box('Error', 'User not found')
        return False


def add_user(email, password, access):
    ref = database.get_ref('users')
    ref.push({"email": email, "password": password, "access": access, "last_login": "None"})
    return


def delete_user(email):
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            ref.child(user).delete()
            return True
    else:
        message_box('Error', 'User not found')
        return False


def check_unique_email(email, action):
    if action == "New":
        ref = database.get_ref('users')
        users = ref.get()
        for user in users:
            if users[user]['email'] == email:
                return False
    elif action == "Update":
        # Not entirely sure, for now this is empty
        pass

    return True
