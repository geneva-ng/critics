import unittest
from datetime import datetime
from utils.firebase import write_data, delete_data, read_data
from utils.user import create_user, get_user_boards, join_board, delete_user, update_last_active, leave_board

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.user_key = "test_user_123"
        self.test_boards = ["board1", "board2"]
        self.user_data = create_user(self.user_key, self.test_boards)

    def tearDown(self):
        """Clean up after tests."""
        delete_data(f"users/{self.user_key}")

    def test_create_user(self):
        """Test creating a new user."""
        user = create_user("new_test_user")
        self.assertEqual(user["user_key"], "new_test_user")
        self.assertEqual(user["boards"], [])
        self.assertIsNone(user["last_active"])
        delete_data("users/new_test_user")

    def test_get_user_boards(self):
        """Test getting a user's boards."""
        boards = get_user_boards(self.user_key)
        self.assertEqual(boards, self.test_boards)

    def test_join_board(self):
        """Test joining a board."""
        new_board = "board3"
        join_board(self.user_key, new_board)
        updated_boards = get_user_boards(self.user_key)
        self.assertIn(new_board, updated_boards)
        self.assertEqual(len(updated_boards), len(self.test_boards) + 1)

    def test_join_board_duplicate(self):
        """Test joining a board that user is already member of."""
        existing_board = self.test_boards[0]
        join_board(self.user_key, existing_board)
        updated_boards = get_user_boards(self.user_key)
        self.assertEqual(len(updated_boards), len(self.test_boards))

    def test_update_last_active(self):
        """Test updating user's last active timestamp."""
        update_last_active(self.user_key)
        user_data = read_data(f"users/{self.user_key}")
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(user_data["last_active"], current_date)

    def test_delete_user(self):
        """Test deleting a user."""
        # Setup user data
        user_key = "test_user"
        create_user(user_key, [])
        
        # Delete user
        delete_user(user_key)
        
        # Fetch user data after deletion
        user_data = read_data(f"users/{user_key}")
        
        # Assert that user data is None after deletion
        self.assertIsNone(user_data)

    def test_leave_board(self):
        """Test leaving a board."""
        leave_board(self.user_key, self.test_boards[0])
        updated_boards = get_user_boards(self.user_key)
        self.assertNotIn(self.test_boards[0], updated_boards)
        self.assertEqual(len(updated_boards), len(self.test_boards) - 1)

if __name__ == "__main__":
    unittest.main()
