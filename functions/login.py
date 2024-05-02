from datetime import datetime

import database
from utils import message_box


# Checks the credentials of a user against the database.
def checkCredentials(email: str, password: str) -> bool:
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        # Check if the email and password match the user in the database
        if users[user]['email'] == email and users[user]['password'] == password:
            return True
    return False


# Retrieves the access level of a user from the database.
def getAccessLV(email: str) -> int:
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            return users[user]['access']
    return False


# Retrieves the name of a user based on their email.
def getAccessName(email: str) -> str:
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            return users[user]['email']
    return ''


# Retrieves all users from the database and filters them based on their access level.
def load_users(status: int = 0) -> list:
    ref = database.get_ref('users')
    users = []
    for user_id, user in ref.get().items():
        if user['email'] == 'None':
            continue
        user['id'] = user_id
        users.append(user)

    # Filter users based on their access level
    if status == 0:
        return users
    elif status == 1:
        return [user for user in users if user['access'] == 1]
    elif status == 2:
        return [user for user in users if user['access'] == 2]
    elif status == 3:
        return [user for user in users if user['access'] == 3]


# Retrieves a user from the database based on their ID.
def get_user(user_id: str) -> dict:
    ref = database.get_ref('users')
    user = ref.child(user_id).get()
    return user


# Updates the last login time of a user in the database.
def update_last_login(email: str) -> None:
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            # Update the 'last_login' field of the user in the database with the current time
            ref.child(user).update({"last_login": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')})
            return


# Updates the details of a user in the database.
def edit_user(email: str, password: str, access: int) -> bool:
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


# Adds a new user to the database.
def add_user(email: str, password: str, access: int) -> None:
    ref = database.get_ref('users')
    ref.push({"email": email, "password": password, "access": access, "last_login": "None"})
    return


# Deletes a user from the database.
def delete_user(email: str) -> bool:
    ref = database.get_ref('users')
    users = ref.get()
    for user in users:
        if users[user]['email'] == email:
            ref.child(user).delete()
            return True
    else:
        message_box('Error', 'User not found')
        return False


# Checks if the email is unique in the database.
def check_unique_email(email: str, action: str) -> bool:
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
