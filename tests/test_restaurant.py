import unittest
from utils.restaurant import add_restaurant, edit_restaurant_rating, edit_restaurant_notes, add_visit_to_restaurant, edit_restaurant_dishes, delete_restaurant, move_restaurant_category
from utils.firebase import write_data, read_data, delete_data

class TestRestaurantManagement(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        self.category_id = "cat_001"
        self.restaurant_id = "rest_001"
        self.restaurant_data = {
            "name": "Oxomoco",
            "rating_1": 8.5,
            "rating_2": 9.0,
            "rating_3": 7.5,
            "notes": "Great Mexican cuisine",
            "visits": ["2024-12-23"],
            "location": "128 Greenpoint Ave, Brooklyn, NY",
            "dishes": [],
            "photo": "http://example.com/oxomoco.jpg"
        }

        # Create the category for testing
        write_data(f"categories/{self.category_id}", {"name": "Fine Dining"})

    def tearDown(self):
        """Clean up after tests."""
        delete_data(f"categories/{self.category_id}")

    def test_add_restaurant(self):
        """Test adding a restaurant to a category."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant["name"], self.restaurant_data["name"])

    def test_edit_restaurant_rating(self):
        """Test editing the ratings of a restaurant."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        edit_restaurant_rating(self.category_id, self.restaurant_id, rating_1=7.0, rating_2=8.0)
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertEqual(restaurant["rating_1"], 7.0)
        self.assertEqual(restaurant["rating_2"], 8.0)

    def test_edit_restaurant_notes(self):
        """Test editing the notes of a restaurant."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        new_notes = "Updated: Excellent service and ambiance"
        edit_restaurant_notes(self.category_id, self.restaurant_id, new_notes)
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertEqual(restaurant["notes"], new_notes)

    def test_add_visit_to_restaurant(self):
        """Test adding a visit date to a restaurant."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        add_visit_to_restaurant(self.category_id, self.restaurant_id, "2024-12-25")
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertIn("2024-12-25", restaurant["visits"])

    def test_edit_restaurant_dishes(self):
        """Test editing the dishes of a restaurant."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        dishes = ["Grilled Avocado", "Tlayuda", "Short Rib Tacos"]
        edit_restaurant_dishes(self.category_id, self.restaurant_id, dishes)
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertEqual(restaurant["dishes"], dishes)

    def test_delete_restaurant(self):
        """Test deleting a restaurant."""
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        delete_restaurant(self.category_id, self.restaurant_id)
        restaurant = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertIsNone(restaurant)

    def test_move_restaurant_category(self):
        new_category_id = "cat_002"
        write_data(f"categories/{new_category_id}", {"name": "Casual Dining"})
        add_restaurant(self.category_id, self.restaurant_id, self.restaurant_data)
        move_restaurant_category(self.category_id, new_category_id, self.restaurant_id)
        restaurant_in_new = read_data(f"categories/{new_category_id}/restaurants/{self.restaurant_id}")
        self.assertIsNotNone(restaurant_in_new)
        self.assertEqual(restaurant_in_new["name"], self.restaurant_data["name"])
        restaurant_in_old = read_data(f"categories/{self.category_id}/restaurants/{self.restaurant_id}")
        self.assertIsNone(restaurant_in_old)
        delete_data(f"categories/{new_category_id}")

if __name__ == "__main__":
    unittest.main()
