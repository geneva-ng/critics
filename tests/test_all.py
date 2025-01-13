import pytest
from utils.firebase import read_data
from restaurant import create_restaurant
from category import create_category, link_category_to_board
from board import create_board
from user import create_user, add_board_to_user

# Constants for testing
USER_ID = "user_100"
BOARD_ID = "board_100"
CATEGORY_ID = "category_100"
RESTAURANT_ID = "restaurant_100"

def test_create_user():
    user = create_user("Geneva", USER_ID)
    assert user["name"] == "Geneva"
    assert user["boards"] == []
    # Verify in Firestore
    user_data = read_data(f"users/{USER_ID}")
    assert user_data is not None

def test_create_board():
    test_create_user()  # Ensure user exists
    board = create_board(BOARD_ID, "Geneva's Board", USER_ID)
    assert board["name"] == "Geneva's Board"
    assert board["owner"] == USER_ID
    # Add board to user
    boards = add_board_to_user(USER_ID, BOARD_ID)
    assert BOARD_ID in boards
    # Verify in Firestore
    board_data = read_data(f"boards/{BOARD_ID}")
    assert board_data is not None

def test_create_category():
    test_create_board()  # Ensure board exists
    category = create_category(CATEGORY_ID, "Fine Dining", "A place for fancy eats")
    assert category["name"] == "Fine Dining"
    assert category["caption"] == "A place for fancy eats"
    # Link category to board
    categories = link_category_to_board(BOARD_ID, CATEGORY_ID)
    assert CATEGORY_ID in categories
    # Verify in Firestore
    category_data = read_data(f"categories/{CATEGORY_ID}")
    assert category_data is not None

def test_create_restaurant():
    test_create_category()  # Ensure category exists
    restaurant = create_restaurant(
        CATEGORY_ID, 
        RESTAURANT_ID, 
        {
            "name": "The Modern",
            "rating_1": 9,
            "rating_2": 8.5,
            "rating_3": 9.5,
            "notes": "Excellent service and food!",
            "visits": ["2025-01-10"],
            "location": "9 W 57th St, New York, NY 10019",
            "dishes": ["Beet Salad", "Lobster Roll"],
            "photo": "http://example.com/photo.jpg"
        }
    )
    assert restaurant["name"] == "The Modern"
    assert restaurant["category_code"] == CATEGORY_ID
    # Verify in Firestore
    restaurant_data = read_data(f"restaurants/{RESTAURANT_ID}")
    assert restaurant_data is not None

if __name__ == "__main__":
    pytest.main()
