from utils.firebase_helpers import write_data, read_data, update_data, delete_data

def add_restaurant(category_id, restaurant_id, data):
    """
    Add a restaurant to a category.
    :param category_id: The category ID to add the restaurant to.
    :param restaurant_id: The unique ID for the restaurant.
    :param data: Dictionary containing restaurant details.
    """
    required_fields = ["name", "rating_1", "rating_2", "rating_3", "notes", "visits", "location", "dishes", "photo"]
    for field in required_fields:
        if field not in data:
            raise KeyError(f"Missing required field: {field}")

    # Validate ratings
    for rating_field in ["rating_1", "rating_2", "rating_3"]:
        if not isinstance(data[rating_field], (int, float)) or not (0 <= data[rating_field] <= 10):
            raise ValueError(f"{rating_field} must be a number between 0 and 10.")

    path = f"categories/{category_id}/restaurants/{restaurant_id}"
    write_data(path, data)
    return data


def edit_restaurant_rating(category_id, restaurant_id, rating_1=None, rating_2=None, rating_3=None):
    """
    Edit the ratings of a restaurant.
    :param category_id: The category ID the restaurant belongs to.
    :param restaurant_id: The restaurant ID to update.
    :param rating_1, rating_2, rating_3: New ratings.
    """
    path = f"categories/{category_id}/restaurants/{restaurant_id}"
    updates = {}
    if rating_1 is not None:
        updates["rating_1"] = rating_1
    if rating_2 is not None:
        updates["rating_2"] = rating_2
    if rating_3 is not None:
        updates["rating_3"] = rating_3
    update_data(path, updates)
    return updates


def edit_restaurant_notes(category_id, restaurant_id, notes):
    """
    Edit the notes for a restaurant.
    :param category_id: The category ID the restaurant belongs to.
    :param restaurant_id: The restaurant ID to update.
    :param notes: New notes for the restaurant.
    """
    path = f"categories/{category_id}/restaurants/{restaurant_id}"
    update_data(path, {"notes": notes})


def add_visit_to_restaurant(category_id, restaurant_id, visit_date):
    """
    Add a visit date to a restaurant.
    :param category_id: The category ID the restaurant belongs to.
    :param restaurant_id: The restaurant ID to update.
    :param visit_date: The date of the visit.
    """
    path = f"categories/{category_id}/restaurants/{restaurant_id}/visits"
    visits = read_data(path) or []
    visits.append(visit_date)
    write_data(path, visits)


def edit_restaurant_dishes(category_id, restaurant_id, dishes):
    """
    Edit the dishes for a restaurant.
    :param category_id: The category ID the restaurant belongs to.
    :param restaurant_id: The restaurant ID to update.
    :param dishes: List of dishes for the restaurant.
    """
    path = f"categories/{category_id}/restaurants/{restaurant_id}/dishes"
    write_data(path, dishes)


def delete_restaurant(category_id, restaurant_id):
    """
    Delete a restaurant.
    :param category_id: The category ID the restaurant belongs to.
    :param restaurant_id: The restaurant ID to delete.
    """
    path = f"categories/{category_id}/restaurants/{restaurant_id}"
    delete_data(path)
