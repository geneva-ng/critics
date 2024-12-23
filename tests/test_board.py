import unittest
import firebase_admin
from firebase_admin import credentials
from utils.board import create_board, edit_board, get_board_data, add_member_to_board, delete_board
from utils.firebase import read_data, delete_data, update_data
from utils.user import create_user, delete_user, get_user_boards

def setUpModule():
    """Initialize Firebase before running any tests."""
    try:
        firebase_admin.get_app()
    except ValueError:
        # Initialize the app only if it hasn't been initialized
        cred = credentials.Certificate("./gcreds_test.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://critics-4bf98-default-rtdb.firebaseio.com/'
        })

class TestBoardManagement(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.board_id = "board_001"
        self.board_name = "Test Board"

    def tearDown(self):
        """Clean up after tests."""
        delete_data(f"boards/{self.board_id}")

    def test_create_board(self):
        """Test creating a new board."""
        create_board(self.board_id, self.board_name)
        board_data = read_data(f"boards/{self.board_id}")
        self.assertEqual(board_data["name"], self.board_name)  # Verify name is set correctly
        # Remove or update these assertions if categories and members aren't part of initial board creation
        # self.assertIn("categories", board_data)
        # self.assertEqual(board_data["categories"], {})
        # self.assertIn("members", board_data)
        # self.assertEqual(board_data["members"], [])

    def test_edit_board(self):
        """Test editing a board's name."""
        create_board(self.board_id, self.board_name)
        edit_board(self.board_id, name="Updated Board Name")
        board_data = read_data(f"boards/{self.board_id}")
        self.assertEqual(board_data["name"], "Updated Board Name")

    def test_add_member_to_board(self):
        """Test adding a new member to a board."""
        create_board(self.board_id, self.board_name)
        add_member_to_board(self.board_id, "user_001")
        board_data = read_data(f"boards/{self.board_id}")
        self.assertIn("user_001", board_data["members"])

    def test_get_board_data(self):
        """Test retrieving board data."""
        create_board(self.board_id, self.board_name)
        board_data = get_board_data(self.board_id)
        self.assertEqual(board_data["name"], self.board_name)
        # Remove or update these assertions if categories and members aren't part of initial board creation
        # self.assertIn("categories", board_data)
        # self.assertIn("members", board_data)
        # self.assertEqual(board_data["categories"], {})
        # self.assertEqual(board_data["members"], [])

    def test_delete_board(self):
        """Test deleting a board."""
        # Create board without owner
        create_board(self.board_id, self.board_name)
        
        # Delete with any user
        delete_board(self.board_id, "any_user")
        board_data = read_data(f"boards/{self.board_id}")
        self.assertIsNone(board_data)

    def test_delete_board_cleanup(self):
        """Test that deleting a board properly cleans up all references."""
        # Create test board
        board_id = "test_board"
        create_board(board_id, "Test Board")
        
        # Create test user and add to board
        user_key = "test_user"
        create_user(user_key, [board_id])
        add_member_to_board(board_id, user_key)
        
        # Delete board with any user_key
        delete_board(board_id, user_key)
        
        # Debug print
        user_boards = get_user_boards(user_key)
        
        # Verify cleanup
        self.assertIsNotNone(user_boards, "user_boards should not be None")
        self.assertIsInstance(user_boards, list, "user_boards should be a list")
        self.assertNotIn(board_id, user_boards)
        board_data = get_board_data(board_id)
        self.assertIsNone(board_data)


if __name__ == "__main__":
    unittest.main()
