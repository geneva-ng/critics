const admin = require("firebase-admin");

/**
 * Adds a board to a user's list of boards.
 * @param {string} userId - The unique identifier for the user.
 * @param {string} boardCode - The code/ID of the board to add.
 * @return {Promise<Array>} The updated list of boards.
 */
async function addBoardToUser(userId, boardCode) {
  const path = `users/${userId}/boards`;

  try {
    const snapshot = await admin.database().ref(path).get();
    const boards = snapshot.val() || []; // Ensure a list is always returned

    if (!boards.includes(boardCode)) {
      boards.push(boardCode);
      await admin.database().ref(`users/${userId}`).update({boards});
    }

    console.log(`Board ${boardCode} added to user ${userId}`);
    return boards;
  } catch (error) {
    console.error(`Error adding board to user: ${error.message}`);
    throw new Error("Failed to add board to user");
  }
}

/**
 * Creates a new board with a unique ID and a human-readable name.
 * @param {string} boardId - The unique identifier for the board.
 * @param {string} name - The human-readable name of the board.
 * @param {string} owner - The user ID of the board owner.
 * @return {Promise<Object>} The created board data.
 */
async function createBoard(boardId, name, owner) {
  const path = `boards/${boardId}`;
  const boardData = {
    name: name,
    categories: [], // Initialize as empty
    members: [owner], // Initialize with owner as first member
    owner: owner, // Set owner
  };

  try {
    // Add this board to the owner's list of boards
    await addBoardToUser(owner, boardId);

    // Write board data
    await admin.database().ref(path).set(boardData);
    console.log(`Board ${boardId} created successfully`);
    return boardData;
  } catch (error) {
    console.error(`Error creating board: ${error.message}`);
    throw new Error("Failed to create board");
  }
}

/**
 * Edit an existing board's name.
 * @param {string} boardId - The unique identifier for the board.
 * @param {string} name - The new name for the board (optional).
 * @return {Promise<void>}
 */
async function editBoardName(boardId, name) {
  const path = `boards/${boardId}`;
  const updates = {};

  if (name) {
    updates.name = name;
  }

  try {
    await admin.database().ref(path).update(updates);
    console.log(`Board ${boardId} name updated successfully`);
  } catch (error) {
    console.error(`Error updating board name: ${error.message}`);
    throw new Error("Failed to update board name");
  }
}

/**
 * Retrieve data for a specific board.
 * @param {string} boardId - The unique identifier for the board.
 * @return {Promise<Object|null>} The board data or null if not found.
 */
async function getBoardData(boardId) {
  const path = `boards/${boardId}`;

  try {
    const snapshot = await admin.database().ref(path).get();
    if (snapshot.exists()) {
      return snapshot.val();
    }
    return null; // Return null if no data is found
  } catch (error) {
    console.error(`Error retrieving board data: ${error.message}`);
    throw new Error("Failed to retrieve board data");
  }
}

/**
 * Add a user to the board's list of members.
 * @param {string} boardId - The unique identifier for the board.
 * @param {string} userId - The user to add to the board.
 * @return {Promise<void>}
 * @throws {Error} If board doesn't exist or user is already a member.
 */
async function addUserToBoard(boardId, userId) {
  try {
    // Check if board exists
    const boardData = await getBoardData(boardId);
    if (!boardData) {
      throw new Error(`Board ${boardId} does not exist.`);
    }

    const path = `boards/${boardId}/members`;
    const snapshot = await admin.database().ref(path).get();
    const members = snapshot.val() || []; // Ensure a list is always returned

    if (!members.includes(userId)) {
      members.push(userId);
      await admin.database().ref(`boards/${boardId}`).update({members});
      await addBoardToUser(userId, boardId);
      console.log(`User ${userId} added to board ${boardId}`);
    } else {
      throw new Error(`User ${userId} is already a member of board ${boardId}.`);
    }
  } catch (error) {
    console.error(`Error adding user to board: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Add a category to the specified board.
 * @param {string} boardId - The unique identifier for the board.
 * @param {string} categoryId - The category to add to the board.
 * @return {Promise<void>}
 * @throws {Error} If category doesn't exist or is already in board.
 */
async function linkCategoryToBoard(boardId, categoryId) {
  try {
    // Check if category exists
    const categorySnapshot = await admin.database().ref(`categories/${categoryId}`).get();
    if (!categorySnapshot.exists()) {
      throw new Error(`Category ${categoryId} does not exist.`);
    }

    const path = `boards/${boardId}/categories`;
    const snapshot = await admin.database().ref(path).get();
    const categories = snapshot.val() || []; // Ensure a list is always returned

    if (!categories.includes(categoryId)) {
      categories.push(categoryId);
      await admin.database().ref(`boards/${boardId}`).update({categories});
      console.log(`Category ${categoryId} linked to board ${boardId}`);
    } else {
      throw new Error(`Category ${categoryId} is already in board ${boardId}.`);
    }
  } catch (error) {
    console.error(`Error linking category to board: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Remove a category from the specified board.
 * @param {string} boardId - The unique identifier for the board.
 * @param {string} categoryId - The category to remove from the board.
 * @return {Promise<void>}
 */
async function unlinkCategoryFromBoard(boardId, categoryId) {
  try {
    const path = `boards/${boardId}/categories`;
    const snapshot = await admin.database().ref(path).get();
    const categories = snapshot.val() || []; // Ensure a list is always returned

    if (categories.includes(categoryId)) {
      const updatedCategories = categories.filter((id) => id !== categoryId);
      await admin.database().ref(`boards/${boardId}`).update({categories: updatedCategories});
      console.log(`Category ${categoryId} unlinked from board ${boardId}`);
    }
  } catch (error) {
    console.error(`Error unlinking category from board: ${error.message}`);
    throw new Error("Failed to unlink category from board");
  }
}

/**
 * Delete a board and all its associated data.
 * @param {string} boardId - The unique ID of the board to delete.
 * @param {string} userId - The user attempting to delete the board.
 * @return {Promise<void>}
 * @throws {Error} If board doesn't exist or user isn't the owner.
 */
async function deleteBoard(boardId, userId) {
  try {
    // Get board data first to access member list
    const boardData = await getBoardData(boardId);
    if (!boardData) {
      throw new Error(`Board ${boardId} not found`);
    }

    // Verify user is the owner
    if (boardData.owner !== userId) {
      throw new Error("Only the board owner can delete the board");
    }

    // Clean up user references
    if (boardData.members) {
      for (const memberId of boardData.members) {
        const userSnapshot = await admin.database().ref(`users/${memberId}`).get();
        const userData = userSnapshot.val() || {};
        const userBoards = userData.boards || [];
        if (userBoards.includes(boardId)) {
          const updatedBoards = userBoards.filter((id) => id !== boardId);
          await admin.database().ref(`users/${memberId}`).update({boards: updatedBoards});
        }
      }
    }

    // Delete all categories under the board
    if (boardData.categories) {
      for (const categoryId of boardData.categories) {
        const categoryPath = `categories/${categoryId}`;
        const categorySnapshot = await admin.database().ref(categoryPath).get();
        const categoryData = categorySnapshot.val() || {};

        // Delete associated restaurants
        if (categoryData.restaurants) {
          for (const restaurantId of categoryData.restaurants) {
            await admin.database().ref(`restaurants/${restaurantId}`).remove();
          }
        }

        // Delete the category itself
        await admin.database().ref(categoryPath).remove();

        // Unlink from board (though board will be deleted anyway)
        await unlinkCategoryFromBoard(boardId, categoryId);
      }
    }

    // Delete the board itself
    await admin.database().ref(`boards/${boardId}`).remove();
    console.log(`Board ${boardId} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting board: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

module.exports = {
  addBoardToUser,
  createBoard,
  editBoardName,
  getBoardData,
  addUserToBoard,
  linkCategoryToBoard,
  unlinkCategoryFromBoard,
  deleteBoard,
};
