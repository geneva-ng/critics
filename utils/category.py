from utils.firebase import write_data, read_data, update_data, delete_data

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

def edit_category_name_caption(category_id, board_id, name=None, caption=None):
    """
    Edit an existing category's name or caption.
    """
    path = f"boards/{board_id}/categories/{category_id}"
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
    # Fetch all restaurants under the board
    restaurants_path = f"boards/{board_id}/restaurants"
    restaurants = read_data(restaurants_path) or {}

    # Filter and delete restaurants associated with the category
    for restaurant_id, restaurant in restaurants.items():
        if restaurant.get("category_id") == category_id:
            delete_data(f"{restaurants_path}/{restaurant_id}")

    # Delete the category itself
    path = f"boards/{board_id}/categories/{category_id}"
    delete_data(path)
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

