from utils.board import delete_board
from utils.firebase import write_data, read_data, update_data, delete_data
from datetime import datetime

def remove_user_from_board(board_id, user_id):
    """
    Remove a user from the board's list of members.
    """
    path = f"boards/{board_id}/members"
    members = read_data(path) or []  # Ensure a list is always returned
    if user_id in members:
        members.remove(user_id)
        update_data(f"boards/{board_id}", {"members": members})

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
    # Get user's boards and handle each one
    user_boards = get_user_boards(user_id)

    for board_id in user_boards:
        # Get board data to check ownership
        board_data = read_data(f"boards/{board_id}")
        if board_data and board_data.get("owner") == user_id:
            # Delete boards owned by this user
            delete_board(board_id, user_id)
        else:
            # Just remove user from boards they don't own
            remove_user_from_board(board_id, user_id)

    # Delete the user data
    path = f"users/{user_id}"
    delete_data(path)

    # Ensure the function does not return anything or returns None explicitly
    return None
