import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key JSON file
SERVICE_ACCOUNT_PATH = "./gcreds_test.json"

# Initialize Firebase Admin SDK
if not firebase_admin._apps:  # Prevent duplicate initialization
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://critics-4bf98-default-rtdb.firebaseio.com/'
    })

# Reference the root of your database
ref = db.reference('/')

# JSON structure from the file
data = {
    "users": {
        "user1": {
            "user_id": "abc123",
            "boards": ["board123"]
        },
        "user2": {
            "user_id": "xyz789",
            "boards": ["board123"]
        }
    },
    "boards": {
        "board123": {
            "board_code": "board123",
            "owner_key": "abc123",
            "members": ["abc123", "xyz789"],
            "categories": {
                "1": {
                    "name": "Desserts",
                    "caption": "Sweet and indulgent treats"
                },
                "2": {
                    "name": "Fast Food",
                    "caption": "Satisfy your pizza cravings"
                }
            },
            "restaurants": {
                "1": {
                    "name": "The Sweet Spot",
                    "category_id": "1",
                    "rating_1": 4.5,
                    "rating_2": 4.0,
                    "rating_3": 4.8,
                    "notes": "Best for chocolate lovers.",
                    "visits": ["2024-12-01"],
                    "location": "123 Candy Lane, Dessertville",
                    "dishes": ["Chocolate Cake", "Brownie Sundae"],
                    "photo": "https://example.com/photos/sweet-spot.jpg"
                },
                "2": {
                    "name": "Jollibee",
                    "category_id": "2",
                    "rating_1": 4.3,
                    "rating_2": 4.4,
                    "rating_3": 4.1,
                    "notes": "Light and fluffy cakes.",
                    "visits": ["2024-11-15"],
                    "location": "789 Frosting Ave, Dessertville",
                    "dishes": ["Red Velvet Cake", "Cheesecake"],
                    "photo": "https://example.com/photos/cake-heaven.jpg"
                }
            }
        }
    }
}

# Push data to the database
def initialize_database():
    ref.set(data)  # This will overwrite the entire database at the root level
    print("Database initialized with the provided schema.")

# Run the function to initialize the database
initialize_database()
