import firebase_admin
from firebase_admin import credentials, db

# Firebase Initialization
def initialize_firebase(service_account_path, database_url):
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})

# Generic Firebase operations
def write_data(path, data):
    ref = db.reference(path)
    ref.set(data)

def update_data(path, data):
    ref = db.reference(path)
    ref.update(data)

def read_data(path):
    ref = db.reference(path)
    return ref.get()

def delete_data(path):
    ref = db.reference(path)
    ref.delete()
