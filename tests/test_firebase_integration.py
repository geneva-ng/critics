import unittest
import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key JSON file
SERVICE_ACCOUNT_PATH = "gcreds_test.json"

# Initialize Firebase Admin SDK (prevent duplicate initialization)
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://critics-4bf98-default-rtdb.firebaseio.com/'
    })

# Reference the database root
ref = db.reference('/')

class FirebaseIntegrationTests(unittest.TestCase):

    def test_create_data(self):
        """Test adding data to the database."""
        test_data = {
            "test_key": {
                "name": "Sample Data",
                "value": 123
            }
        }
        ref.child("integration_test").set(test_data)
        result = ref.child("integration_test").get()
        self.assertEqual(result, test_data)
    
    def test_read_data(self):
        """Test reading data from the database."""
        ref.child("integration_test/test_key").set({"name": "Read Test", "value": 456})
        result = ref.child("integration_test/test_key").get()
        self.assertEqual(result, {"name": "Read Test", "value": 456})
    
    def test_update_data(self):
        """Test updating existing data in the database."""
        ref.child("integration_test/test_key").set({"name": "Update Test", "value": 789})
        ref.child("integration_test/test_key").update({"value": 999})
        result = ref.child("integration_test/test_key").get()
        self.assertEqual(result["value"], 999)

    def test_delete_data(self):
        """Test deleting data from the database."""
        ref.child("integration_test/test_key").set({"name": "Delete Test", "value": 111})
        ref.child("integration_test/test_key").delete()
        result = ref.child("integration_test/test_key").get()
        self.assertIsNone(result)

    def test_nested_data(self):
        """Test handling nested data."""
        nested_data = {
            "level1": {
                "level2": {
                    "key": "Nested Value"
                }
            }
        }
        ref.child("integration_test_nested").set(nested_data)
        result = ref.child("integration_test_nested/level1/level2/key").get()
        self.assertEqual(result, "Nested Value")
    
    def tearDown(self):
        """Clean up after each test."""
        ref.child("integration_test").delete()
        ref.child("integration_test_nested").delete()

if __name__ == "__main__":
    unittest.main()
