from utils.firebase_helpers import write_data, read_data, update_data

def create_user(user_key, boards=[]):
    path = f"users/{user_key}"
    user_data = {
        "user_key": user_key,
        "boards": boards
    }
    write_data(path, user_data)
    return user_data

def get_user_boards(user_key):
    path = f"users/{user_key}/boards"
    return read_data(path)

def join_board(user_key, board_code):
    boards = get_user_boards(user_key) or []
    if board_code not in boards:
        boards.append(board_code)
        update_data(f"users/{user_key}", {"boards": boards})
