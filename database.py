import os
import firebase_admin
import google.auth.exceptions

from firebase_admin import credentials, db

from utils import *

root_dir = os.path.dirname(os.path.abspath(__file__))
dbURL = 'https://rohan-constructions-db-default-rtdb.asia-southeast1.firebasedatabase.app/'

try:
    cred = credentials.Certificate(os.path.join(root_dir, 'extra', 'service.json'))
    firebase_admin.initialize_app(cred, {
        'databaseURL': dbURL})
except (google.auth.exceptions.RefreshError, google.auth.exceptions.TransportError):
    message_box('Error', 'No internet connection.', 'Message')
    exit(1)


def get_ref(ref_name):
    try:
        if ref_name == 'projects':
            return db.reference('projects')
        elif ref_name == 'clients':
            return db.reference('clients')
        elif ref_name == 'resources':
            return db.reference('resources')
        elif ref_name == 'suppliers':
            return db.reference('suppliers')
        elif ref_name == 'manpower':
            return db.reference('manpower')
        elif ref_name == 'finances':
            return db.reference('finance')
        elif ref_name == 'users':
            return db.reference('users')
        elif ref_name == 'archive':
            return db.reference('archive')
        return None
    except (google.auth.exceptions.RefreshError, google.auth.exceptions.TransportError):
        message_box('Error', 'No internet connection.', 'Message')
        exit(1)
