from utils.firebase import write_data, read_data, update_data, delete_data

def create_board(board_id, name, owner):
    """
    Create a new board with a unique ID and a human-readable name.
    """
    path = f"boards/{board_id}"
    board_data = {
        "name": name,
        "categories": [],  # Initialize as empty
        "members": [],  # Initialize as empty
        "owner": owner  # Initialize as empty              NOTE: this is new. The tests will need to be updated.
    }
    write_data(path, board_data)  # Ensure 'categories' is written
    return board_data

def edit_board_name(board_id, name=None):
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
    return read_data(path)  # Return None if no data is found, according to read_data in firebase.py

def add_user_to_board(board_id, user_id):
    """
    Add a user to the board's list of members.
    """
    path = f"boards/{board_id}/members"
    members = read_data(path) or []  # Ensure a list is always returned
    if user_id not in members:
        members.append(user_id)
        update_data(f"boards/{board_id}", {"members": members})
    else:
        raise ValueError(f"User {user_id} is already a member of board {board_id}.")
    
def remove_user_from_board(board_id, user_id):
    """
    Remove a user from the board's list of members.
    """
    path = f"boards/{board_id}/members"
    members = read_data(path) or []  # Ensure a list is always returned
    if user_id in members:
        members.remove(user_id)
        update_data(f"boards/{board_id}", {"members": members})

def link_category_to_board(board_id, category_id):
    """
    Add a category to the specified board.
    """
    path = f"boards/{board_id}/categories"
    categories = read_data(path) or []  # Ensure a list is always returned
    if category_id not in categories:
        categories.append(category_id)
        update_data(f"boards/{board_id}", {"categories": categories})
    else:
        raise ValueError(f"Category {category_id} is already in board {board_id}.")
 
def delete_board(board_id, user_id):
    """
    Delete a board and all its associated data.
    :param board_id: The unique ID of the board to delete.
    :param user_id: The user attempting to delete the board.
    """
    # Get board data first to access member list
    board_data = read_data(f"boards/{board_id}")
    if not board_data:
        raise ValueError(f"Board {board_id} not found")
        
    # Verify user is the owner
    if board_data.get("owner") != user_id:
        raise ValueError("Only the board owner can delete the board")
        
    # Clean up user references
    if "members" in board_data:
        for member_key in board_data["members"]:
            user_data = read_data(f"users/{member_key}") or {}
            user_boards = user_data.get("boards", [])
            if board_id in user_boards:
                user_boards.remove(board_id)
                update_data(f"users/{member_key}", {"boards": user_boards})
    
    # Explicitly remove all members from the board
    if "members" in board_data:
        for member_key in board_data["members"]:
            delete_data(f"boards/{board_id}/members/{member_key}")
    
    # Delete all categories under the board
    if "categories" in board_data:
        for category_id in board_data["categories"]:
            delete_data(f"boards/{board_id}/categories/{category_id}")
    
    # Delete the board itself
    delete_data(f"boards/{board_id}")

