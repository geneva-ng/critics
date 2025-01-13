from utils.firebase import write_data, read_data, update_data, delete_data
from utils.board import unlink_category_from_board

def create_category(category_id, name, caption):
    """
    Add a category to the specified board.
    """
    if not category_id or not isinstance(category_id, str):
        raise ValueError("Invalid category ID: must be a non-empty string.")
    path = f"categories/{category_id}"
    category_data = {
        "name": name,
        "caption": caption,
        "restaurants": []
    }
    write_data(path, category_data)
    return category_data

def edit_category_name_caption(category_id, name=None, caption=None):
    """
    Edit an existing category's name or caption.
    """
    path = f"categories/{category_id}"
    updates = {}
    if name:
        updates["name"] = name
    if caption:
        updates["caption"] = caption
    update_data(path, updates)

def delete_category(category_id, board_id):
    """
    Delete a category from the specified board and remove associated restaurants.
    """

    # Get all restaurants associated with the category
    category_path = f"categories/{category_id}"
    category_data = read_data(category_path) or {}
    restaurants = category_data.get("restaurants", [])

    # Delete each restaurant
    for restaurant_id in restaurants:
        delete_data(f"restaurants/{restaurant_id}")

    # Unlink the category from the board
    unlink_category_from_board(board_id, category_id)

    # Delete the category
    delete_data(category_path)

    return None  # Explicitly return None for consistency

def add_restaurant_to_category(category_id, restaurant_id):
    """
    Add a restaurant ID to a category's restaurants array.
    :param category_id: The category ID to update.
    :param restaurant_id: String containing the restaurant ID to add.
    """
    if not isinstance(restaurant_id, str):
        raise ValueError("Restaurant ID must be a string")

    path = f"categories/{category_id}/restaurants"
    restaurants = read_data(path) or []
    restaurants.append(restaurant_id)
    write_data(path, restaurants)
    return restaurants

def remove_restaurant_from_category(category_id, restaurant_id):
    """
    Remove a restaurant ID from a category's restaurants array.
    :param category_id: The category ID to update.
    :param restaurant_id: String containing the restaurant ID to remove.
    """
    if not isinstance(restaurant_id, str):
        raise ValueError("Restaurant ID must be a string")

    path = f"categories/{category_id}/restaurants"
    restaurants = read_data(path) or []
    restaurants.remove(restaurant_id)
    write_data(path, restaurants)
    return restaurants

