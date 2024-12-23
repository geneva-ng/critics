import unittest
from utils.board_management import create_board, edit_board, get_board_data, add_member_to_board
from utils.firebase_helpers import read_data, delete_data

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
        self.assertIn("categories", board_data)  # Check that 'categories' exists
        self.assertEqual(board_data["categories"], {})  # Validate it's an empty dictionary
        self.assertIn("members", board_data)
        self.assertEqual(board_data["members"], [])

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
        self.assertIn("categories", board_data)  # Check for 'categories'
        self.assertIn("members", board_data)
        self.assertEqual(board_data["categories"], {})
        self.assertEqual(board_data["members"], [])

if __name__ == "__main__":
    unittest.main()
