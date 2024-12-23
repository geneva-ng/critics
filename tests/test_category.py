import unittest
from utils.category import add_category, edit_category, delete_category
from utils.firebase import read_data, delete_data

class TestCategoryManagement(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.board_id = "board_001"
        self.category_id = "cat_001"
        self.category_name = "Desserts"
        self.category_caption = "Sweet treats"

    def tearDown(self):
        """Clean up after tests."""
        delete_data(f"boards/{self.board_id}/categories/{self.category_id}")

    def test_add_category(self):
        """Test adding a category."""
        add_category(self.category_id, self.board_id, self.category_name, self.category_caption)
        category = read_data(f"boards/{self.board_id}/categories/{self.category_id}")
        self.assertIsNotNone(category)
        self.assertEqual(category["name"], self.category_name)
        self.assertEqual(category["caption"], self.category_caption)

    def test_edit_category(self):
        """Test editing a category's name and caption."""
        add_category(self.category_id, self.board_id, self.category_name, self.category_caption)
        edit_category(self.category_id, self.board_id, name="Updated Desserts", caption="Updated Caption")
        category = read_data(f"boards/{self.board_id}/categories/{self.category_id}")
        self.assertEqual(category["name"], "Updated Desserts")
        self.assertEqual(category["caption"], "Updated Caption")

    def test_delete_category(self):
        """Test deleting a category."""
        add_category(self.category_id, self.board_id, self.category_name, self.category_caption)
        delete_category(self.category_id, self.board_id)
        category = read_data(f"boards/{self.board_id}/categories/{self.category_id}")
        self.assertIsNone(category)

if __name__ == "__main__":
    unittest.main()
