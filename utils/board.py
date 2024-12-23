from utils.firebase import write_data, read_data, update_data, delete_data

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
    
def delete_board(board_id, user_key):
    """
    Delete a board and all its associated data.
    :param board_id: The unique ID of the board to delete.
    :param user_key: The user attempting to delete the board.
    """
    # Get board data first to access member list
    board_data = read_data(f"boards/{board_id}")
    if not board_data:
        raise ValueError(f"Board {board_id} not found")
        
    # Clean up user references
    if "members" in board_data:
        for member_key in board_data["members"]:
            user_data = read_data(f"users/{member_key}") or {}
            user_boards = user_data.get("boards", [])
            if board_id in user_boards:
                user_boards.remove(board_id)
                update_data(f"users/{member_key}", {"boards": user_boards})
    
    # Delete the board and all its nested data
    path = f"boards/{board_id}"
    delete_data(path)

