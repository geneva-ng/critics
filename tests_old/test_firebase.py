import unittest
from utils.firebase import initialize_firebase, read_data, delete_data
from utils.user import create_user, get_user_boards, add_board_to_user
from utils.board import create_board, get_board_data, add_user_to_board

class TestFirebaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Firebase connection
        initialize_firebase("gcreds_test.json", "https://critics-4bf98-default-rtdb.firebaseio.com/")
    
    def test_create_user(self):
        """Test creating a new user and assigning a board."""
        create_user("test_user", ["board_001"])
        user_data = read_data("users/test_user")
        self.assertEqual(user_data["user_id"], "test_user")
        self.assertIn("board_001", user_data["boards"])
        delete_data("users/test_user")

    def test_create_board(self):
        """Test creating a new board."""
        create_board("board_001", "Test Board")
        board_data = get_board_data("board_001")
        self.assertEqual(board_data["name"], "Test Board")
        delete_data("boards/board_001")

    def test_add_board_to_user(self):
        """Test a user joining a board."""
        create_user("test_user", [])
        create_board("board_001", "Test Board")
        user_boards = add_board_to_user("test_user", "board_001")
        self.assertIn("board_001", user_boards)
        delete_data("users/test_user")
        delete_data("boards/board_001")
    
    def test_add_user_to_board(self):
        """Test adding a new member to a board."""
        create_board("board_001", "Test Board")
        add_user_to_board("board_001", "new_member")
        board_data = get_board_data("board_001")
        self.assertIn("new_member", board_data["members"])
        delete_data("boards/board_001")

if __name__ == "__main__":
    unittest.main()
