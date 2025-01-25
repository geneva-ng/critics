const admin = require("firebase-admin");

/**
 * Creates a new user in the database.
 * @param {string} name - The name of the user.
 * @param {string} userId - The unique identifier for the user.
 * @param {Array} boards - An array of boards associated with the user (default is an empty array).
 * @return {Object} The user data that was created.
 */
async function createUser(name, userId, boards = []) {
  const path = `users/${userId}`;
  const userData = {
    name: name,
    boards: boards,
  };

  try {
    await admin.database().ref(path).set(userData); // Writing to Firebase Realtime Database
    console.log(`User created successfully at path: ${path}`);
    return userData;
  } catch (error) {
    console.error(`Error creating user: ${error.message}`);
    throw new Error("Failed to create user");
  }
}

/**
 * Retrieve the list of boards a user is part of.
 * @param {string} userId - The unique identifier for the user.
 * @return {Array} The list of boards associated with the user.
 */
async function getUserBoards(userId) {
  const path = `users/${userId}/boards`;

  try {
    const snapshot = await admin.database().ref(path).get();
    if (snapshot.exists()) {
      return snapshot.val();
    }
    return [];
  } catch (error) {
    const errorMsg = `Error retrieving boards for user ${userId}: ${error.message}`;
    console.error(errorMsg);
    throw new Error("Failed to retrieve user boards");
  }
}

/**
 * Updates the boards array for a specific user.
 * @param {string} userId - The unique identifier for the user.
 * @param {Array} boards - The new array of boards to set.
 * @return {Object} The updated user data.
 */
async function updateUserBoards(userId, boards) {
  const path = `users/${userId}/boards`;

  try {
    await admin.database().ref(path).set(boards);
    console.log(`Boards updated successfully for user: ${userId}`);
    return {boards};
  } catch (error) {
    const errorMsg = `Error updating boards for user ${userId}: ${error.message}`;
    console.error(errorMsg);
    throw new Error("Failed to update user boards");
  }
}

/**
 * Removes a user from a board's list of members.
 * @param {string} boardId - The ID of the board.
 * @param {string} userId - The ID of the user to remove.
 * @return {Promise<void>}
 */
async function removeUserFromBoard(boardId, userId) {
  const path = `boards/${boardId}/members`;

  try {
    const snapshot = await admin.database().ref(path).get();
    let members = snapshot.val() || []; // Ensure a list is always returned

    if (members.includes(userId)) {
      members = members.filter((id) => id !== userId);
      await admin.database().ref(`boards/${boardId}`).update({members});
      console.log(`User ${userId} removed from board ${boardId}`);
    }
  } catch (error) {
    console.error(`Error removing user ${userId} from board ${boardId}: ${error.message}`);
    throw new Error("Failed to remove user from board");
  }
}
/**
 * Deletes a user and all their associated data.
 * @param {string} userId - The unique identifier for the user to delete.
 * @return {Promise<void>}
 */
async function deleteUser(userId) {
  try {
    // Get user's boards
    const boards = await getUserBoards(userId);

    // Handle each board
    for (const boardId of boards) {
      // Get board data to check ownership
      const boardSnapshot = await admin.database().ref(`boards/${boardId}`).get();
      const boardData = boardSnapshot.val();

      if (boardData && boardData.owner === userId) {
        // Delete boards owned by this user
        await admin.database().ref(`boards/${boardId}`).remove();
      } else {
        // Remove user from boards they don't own
        await removeUserFromBoard(boardId, userId);
      }
    }

    // Delete the user data
    await admin.database().ref(`users/${userId}`).remove();
    console.log(`User ${userId} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting user ${userId}: ${error.message}`);
    throw new Error("Failed to delete user");
  }
}

module.exports = {createUser, getUserBoards, updateUserBoards, deleteUser, removeUserFromBoard};
