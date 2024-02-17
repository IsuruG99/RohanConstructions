import os
import firebase_admin
from firebase_admin import credentials, db

root_dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(root_dir, 'extra', 'service.json'))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rohan-constructions-db-default-rtdb.asia-southeast1.firebasedatabase.app/'})


def get_ref(ref_name):
    if ref_name == 'projects':
        return db.reference('projects')
    elif ref_name == 'clients':
        return db.reference('clients')
    elif ref_name == 'resources':
        return db.reference('resources')
    elif ref_name == 'suppliers':
        return db.reference('suppliers')
    elif ref_name == 'personnel':
        return db.reference('personnel')
    elif ref_name == 'finances':
        return db.reference('finances')
    return None
