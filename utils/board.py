from utils.firebase import write_data, read_data, update_data

def create_board(board_id, name):
    """
    Create a new board with a unique ID and a human-readable name.
    """
    path = f"boards/{board_id}"
    board_data = {
        "name": name,
        "categories": {},  # Initialize as empty
        "members": []  # Initialize as empty
    }
    write_data(path, board_data)  # Ensure 'categories' is written
    return board_data


def edit_board(board_id, name=None):
    """
    Edit an existing board's name.
    """
    path = f"boards/{board_id}"
    updates = {}
    if name:
        updates["name"] = name
    update_data(path, updates)


def get_board_data(board_id):
    """
    Retrieve data for a specific board.
    """
    path = f"boards/{board_id}"
    return read_data(path)

def add_member_to_board(board_id, user_key):
    """
    Add a member to the specified board.
    :param board_id: The unique ID of the board.
    :param user_key: The unique ID of the user to add as a member.
    """
    path = f"boards/{board_id}/members"
    members = read_data(path) or []  # Retrieve current members or initialize as empty
    if user_key not in members:
        members.append(user_key)
        update_data(f"boards/{board_id}", {"members": members})
    else:
        raise ValueError(f"User {user_key} is already a member of board {board_id}.")
