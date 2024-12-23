from utils.firebase_helpers import initialize_firebase, read_data, delete_data
from utils.board_management import create_board, edit_board
from utils.category_management import add_category, edit_category
from utils.restaurant_management import add_restaurant, edit_restaurant_rating, edit_restaurant_dishes

# Initialize Firebase
initialize_firebase("./gcreds_test.json", "https://critics-4bf98-default-rtdb.firebaseio.com/")

# Define board and restaurant data
board_id = "board_001"  # Using a code-like identifier for the board
category_id = "cat_001"
restaurant_id = "rest_001"

# Simulate User Tasks
def enact_changes():
    """Simulate a user performing tasks on the database."""
    # Step 1: Create a new board named "Fine Dining Adventures"
    print("Creating board 'Fine Dining Adventures'...")
    create_board(board_id, name="Fine Dining Adventures", description="A collection of upscale restaurant experiences")
    print("Board created.")

    # Step 2: Create a new category named "Fine Dining"
    print("Creating category 'Fine Dining'...")
    add_category(board_id, category_id, "Fine Dining", "")
    print("Category created.")

    # Step 3: Add a caption to the category
    print("Adding a caption to the category...")
    edit_category(board_id, category_id, name="Fine Dining", caption="Elegant and upscale experiences")
    print("Caption added.")

    # Step 4: Add a restaurant named Oxomoco
    print("Adding a restaurant 'Oxomoco'...")
    restaurant_data = {
        "name": "Oxomoco",
        "category_id": category_id,
        "rating_1": 8.5,
        "rating_2": 9.0,
        "rating_3": 7.5,
        "notes": "Arbitrary data for testing.",
        "visits": ["2024-12-23"],
        "location": "128 Greenpoint Ave, Brooklyn, NY",
        "dishes": [],
        "photo": "http://example.com/oxomoco.jpg"
    }
    add_restaurant(board_id, restaurant_id, restaurant_data)
    print("Restaurant added.")

    # Step 5: Change all ratings to 6
    print("Updating ratings for 'Oxomoco'...")
    edit_restaurant_rating(board_id, restaurant_id, rating_1=6.0, rating_2=6.0, rating_3=6.0)
    print("Ratings updated.")

    # Step 6: Add three dishes
    print("Adding dishes for 'Oxomoco'...")
    dishes = ["Grilled Avocado", "Tlayuda", "Short Rib Tacos"]
    edit_restaurant_dishes(board_id, restaurant_id, dishes)
    print("Dishes added.")

    # Step 7: Reorder the dishes
    print("Reordering dishes for 'Oxomoco'...")
    reordered_dishes = ["Short Rib Tacos", "Grilled Avocado", "Tlayuda"]
    edit_restaurant_dishes(board_id, restaurant_id, reordered_dishes)
    print("Dishes reordered.")

def undo_changes():
    """Undo changes made by the enact_changes function."""
    print("Undoing changes...")
    # Delete the restaurant
    print(f"Deleting restaurant '{restaurant_id}'...")
    delete_data(f"boards/{board_id}/restaurants/{restaurant_id}")
    print("Restaurant deleted.")

    # Delete the category
    print(f"Deleting category '{category_id}'...")
    delete_data(f"boards/{board_id}/categories/{category_id}")
    print("Category deleted.")

    # Delete the board
    print(f"Deleting board '{board_id}'...")
    delete_data(f"boards/{board_id}")
    print("Board deleted.")

# Toggle between enact and undo
if __name__ == "__main__":
    # Comment out one of the following lines to toggle
    enact_changes()
    # undo_changes()
