from utils.firebase import write_data, read_data, update_data, delete_data
from datetime import datetime

def create_user(user_key, boards=[]):
    path = f"users/{user_key}"
    user_data = {
        "user_key": user_key,
        "boards": boards,
        "last_active": None  # Initialize as None until first activity
    }
    write_data(path, user_data)
    return user_data

def get_user_boards(user_key):
    path = f"users/{user_key}/boards"
    return read_data(path) or []

def join_board(user_key, board_code):
    boards = get_user_boards(user_key) or []
    if board_code not in boards:
        boards.append(board_code)
        update_data(f"users/{user_key}", {"boards": boards})

def leave_board(user_key, board_code):
    boards = get_user_boards(user_key) or []
    if board_code in boards:
        boards.remove(board_code)
        update_data(f"users/{user_key}", {"boards": boards})

def update_last_active(user_key):
    """
    Update the last_active timestamp for a user to the current date.
    :param user_key: The unique ID of the user to update.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    update_data(f"users/{user_key}", {"last_active": current_date})

def delete_user(user_key):
    """
    Delete a user and all their data.
    :param user_key: The unique ID of the user to delete.
    """
    path = f"users/{user_key}"
    delete_data(path)
    # Ensure the function does not return anything or returns None explicitly
    return None
