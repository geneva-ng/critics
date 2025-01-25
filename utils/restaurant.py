from utils.firebase import write_data, read_data, update_data, delete_data
from utils.category import add_restaurant_to_category, remove_restaurant_from_category

# moved
def create_restaurant(category_id, restaurant_id, data):
    """
    Add a restaurant and associate it with a category.
    :param category_id: The category ID to associate the restaurant with.
    :param restaurant_id: The unique ID for the restaurant.
    :param data: Dictionary containing restaurant details.
    """
    required_fields = [
        "name",
        "rating_1", 
        "rating_2",
        "rating_3",
        "notes",
        "visits", # list of date strings
        "location",
        "dishes",
        "photo"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field in restaurant creation: {field}")

    # Validate ratings
    for rating_field in ["rating_1", "rating_2", "rating_3"]:
        if not isinstance(data[rating_field], (int, float)) or not (0 <= data[rating_field] <= 10):
            raise ValueError(f"{rating_field} must be a number between 0 and 10.")

    # Add category reference to restaurant data
    restaurant_data = data.copy()
    restaurant_data["category_code"] = category_id

    path = f"restaurants/{restaurant_id}"
    write_data(path, restaurant_data)

    # Add restaurant to category, on the category-side
    add_restaurant_to_category(category_id, restaurant_id)

    return restaurant_data

# moved
def edit_rating(restaurant_id, rating_number, rating_value):
    """
    Edit a specific rating of a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param rating_number: Integer 1-3 specifying which rating to update.
    :param rating_value: The new rating value.
    """
    if not isinstance(rating_number, int) or rating_number not in [1, 2, 3]:
        raise ValueError("rating_number must be 1, 2, or 3")

    if not isinstance(rating_value, (int, float)) or not (0 <= rating_value <= 10):
        raise ValueError("rating_value must be a number between 0 and 10")

    rating_field = f"rating_{rating_number}"
    data = {rating_field: rating_value}

    path = f"restaurants/{restaurant_id}"
    update_data(path, data)
    return data

# moved
def edit_notes(restaurant_id, notes):
    """
    Edit the notes for a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param notes: String containing the new notes.
    """
    if not isinstance(notes, str):
        raise ValueError("notes must be a string")

    data = {"notes": notes}
    path = f"restaurants/{restaurant_id}"
    update_data(path, data)
    return data

# moved
def add_visit(restaurant_id, visit_date):
    """
    Add a visit date to a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param visit_date: String containing the visit date.
    """
    if not isinstance(visit_date, str):
        raise ValueError("visit_date must be a string")

    path = f"restaurants/{restaurant_id}/visits"
    visits = read_data(path) or []
    visits.append(visit_date)
    write_data(path, visits)
    return visits

# moved
def delete_visit(restaurant_id):
    """
    Delete the most recent visit date from a restaurant.
    :param restaurant_id: The restaurant ID to update.
    """
    path = f"restaurants/{restaurant_id}/visits"
    visits = read_data(path) or []
    if visits:
        visits.pop()
        write_data(path, visits)
    return visits

# moved
def edit_dish_ranking(restaurant_id, dishes):
    """
    Edit the dishes for a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param dishes: Array containing the new ordered list of dishes.
    """
    if not isinstance(dishes, list):
        raise ValueError("dishes must be an array")

    path = f"restaurants/{restaurant_id}/dishes"
    write_data(path, dishes)
    return dishes

# moved
def add_dish(restaurant_id, dish):
    """
    Add a dish to a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param dish: String containing the dish name to add.
    """
    if not isinstance(dish, str):
        raise ValueError("dish must be a string")

    path = f"restaurants/{restaurant_id}/dishes"
    dishes = read_data(path) or []
    dishes.append(dish)
    write_data(path, dishes)
    return dishes

# moved
def delete_dish(restaurant_id, dish):
    """
    Delete a dish from a restaurant.
    :param restaurant_id: The restaurant ID to update.
    :param dish: String containing the dish name to delete.
    """
    if not isinstance(dish, str):
        raise ValueError("dish must be a string")

    path = f"restaurants/{restaurant_id}/dishes"
    dishes = read_data(path) or []
    dishes.remove(dish)
    write_data(path, dishes)
    return dishes

def delete_restaurant(restaurant_id):
    """
    Delete a restaurant.
    :param restaurant_id: The restaurant ID to delete.
    """
    path = f"restaurants/{restaurant_id}"

    # Remove restaurant from category, on the category-side
    restaurant_data = read_data(path)
    if restaurant_data and "category_code" in restaurant_data:
        remove_restaurant_from_category(restaurant_data["category_code"], restaurant_id)

    delete_data(path)

# moved
def switch_restaurant_category(restaurant_id, new_category_id):
    """
    Change a restaurant's category.
    :param restaurant_id: The restaurant ID to update.
    :param new_category_id: String containing the new category ID.
    """
    if not isinstance(new_category_id, str):
        raise ValueError("Category ID must be a string")

    path = f"restaurants/{restaurant_id}"
    restaurant_data = read_data(path)
    
    if not restaurant_data:
        raise ValueError(f"Restaurant {restaurant_id} not found")
        
    restaurant_data["category_code"] = new_category_id
    write_data(path, restaurant_data)

    # Remove restaurant from old category, on the category-side
    remove_restaurant_from_category(restaurant_id, restaurant_data["category_code"])

    # Add restaurant to new category, on the category-side
    add_restaurant_to_category(new_category_id, restaurant_id)

    return restaurant_data
