from utils.board import remove_user_from_board
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

def add_board_to_user(user_id, board_code):
    """
    Adds a board to a user's list of boards.
    """
    boards = get_user_boards(user_id)
    if board_code not in boards:
        boards.append(board_code)
        update_data(f"users/{user_id}", {"boards": boards})
    return boards  # Return updated boards for confirmation

def remove_board_from_user(user_id, board_code):
    """
    Remove a board from a user's list of boards.
    """
    boards = get_user_boards(user_id)
    if board_code in boards:
        boards.remove(board_code)
        update_data(f"users/{user_id}", {"boards": boards})
    return boards  # Return updated boards for confirmation

def delete_user(user_id):
    """
    Delete a user and all their data.
    :param user_id: The unique ID of the user to delete.
    """

    # Get user's boards and remove the user from each one before deleting the user
    user_boards = get_user_boards(user_id)
    for board_id in user_boards:
        remove_user_from_board(board_id, user_id)
    
    path = f"users/{user_id}"
    delete_data(path)

    # Ensure the function does not return anything or returns None explicitly
    return None
