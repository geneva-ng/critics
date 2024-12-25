from utils.firebase import write_data, read_data, update_data, delete_data
from datetime import datetime

def create_user(name, user_id, boards=[]):
    path = f"users/{user_id}"
    user_data = {
        "name": name,
        "boards": boards,
        "last_active": None  # Initialize as None until first activity
    }
    write_data(path, user_data)
    return user_data

def get_user_boards(user_id):
    """
    Retrieve the list of boards a user is part of.
    """
    path = f"users/{user_id}/boards"
    return read_data(path) or []  # Ensure a list is always returned

def join_board(user_id, board_code):
    """
    Add a user to a board.
    """
    boards = get_user_boards(user_id)
    if board_code not in boards:
        boards.append(board_code)
        update_data(f"users/{user_id}", {"boards": boards})
    return boards  # Return updated boards for confirmation

def leave_board(user_id, board_code):
    """
    Remove a user from a board.
    """
    boards = get_user_boards(user_id)
    if board_code in boards:
        boards.remove(board_code)
        update_data(f"users/{user_id}", {"boards": boards})
    return boards  # Return updated boards for confirmation

def update_last_active(user_id):
    """
    Update the last_active timestamp for a user to the current date.
    :param user_id: The unique ID of the user to update.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    update_data(f"users/{user_id}", {"last_active": current_date})

def delete_user(user_id):
    """
    Delete a user and all their data.
    :param user_id: The unique ID of the user to delete.
    """
    path = f"users/{user_id}"
    delete_data(path)
    # Ensure the function does not return anything or returns None explicitly
    return None
