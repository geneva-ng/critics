import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import firebase_admin
from firebase_admin import credentials, db

SERVICE_ACCOUNT_PATH = "/Users/geneva/Downloads/critics/gcreds_test.json"
if not firebase_admin._apps:  # Prevent duplicate initialization
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://critics-4bf98-default-rtdb.firebaseio.com/'
    })

from utils.board import get_board_data, add_member_to_board
from utils.user import create_user, join_board
import uuid

def create_new_board(owner_key, name=None):
    """
    Create a new board with the specified owner.
    
    Args:
        owner_key: The user key of the board owner
        name: Optional name for the board
        
    Returns:
        The board ID of the newly created board
    """
    # Generate unique board ID
    board_id = str(uuid.uuid4())[:8]
    
    # Initialize board data
    board_data = {
        "board_code": board_id,
        "owner_key": owner_key,
        "members": [owner_key],
        "name": name,
        "categories": {},
        "restaurants": {}
    }
    
    # Write board data to database
    ref = db.reference(f'boards/{board_id}')
    ref.set(board_data)
    
    # Add board to owner's boards list
    join_board(owner_key, board_id)
    
    return board_id

# Example usage of create_new_board function
if __name__ == "__main__":
    # Create a test user and board
    owner_key = "test_owner_123"
    board_name = "My Test Board"
    
    # Create new board
    board_id = create_new_board(owner_key, board_name)
    print(f"Created new board with ID: {board_id}")
    
    # Verify board was created by retrieving data
    board_data = get_board_data(board_id)
    print(f"Board data: {board_data}")
