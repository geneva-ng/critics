import unittest
from utils.category import add_category, edit_category, delete_category
from utils.firebase import read_data, delete_data, write_data

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

    def test_delete_category_and_associated_restaurants(self):
        """Test deleting a category and ensuring associated restaurants are deleted."""
        # Add a category
        add_category(self.category_id, self.board_id, self.category_name, self.category_caption)

        # Add a restaurant linked to this category
        restaurant_id = "rest_001"
        restaurant_data = {
            "name": "Test Restaurant",
            "category_id": self.category_id,
            "rating_1": 5.0,
            "rating_2": 4.0,
            "rating_3": 3.5,
            "notes": "Great food",
            "visits": ["2024-12-25"],
            "location": "123 Main Street",
            "dishes": ["Dish 1", "Dish 2"],
            "photo": "http://example.com/photo.jpg"
        }
        write_data(f"boards/{self.board_id}/restaurants/{restaurant_id}", restaurant_data)

        # Delete the category
        delete_category(self.category_id, self.board_id)

        # Verify the category is deleted
        category = read_data(f"boards/{self.board_id}/categories/{self.category_id}")
        self.assertIsNone(category)

        # Verify the associated restaurant is also deleted
        restaurant = read_data(f"boards/{self.board_id}/restaurants/{restaurant_id}")
        self.assertIsNone(restaurant)


if __name__ == "__main__":
    unittest.main()
