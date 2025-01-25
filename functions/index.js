/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

// Import required dependencies
const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const auth = require("./auth");
const {
  createUser,
  getUserBoards,
  updateUserBoards,
  deleteUser,
  removeUserFromBoard,
} = require("./user");
const {
  addBoardToUser,
  createBoard,
  editBoardName,
  getBoardData,
  addUserToBoard,
  linkCategoryToBoard,
  unlinkCategoryFromBoard,
  deleteBoard,
} = require("./board");
const {
  createCategory,
  editCategory,
  addRestaurantToCategory,
  removeRestaurantFromCategory,
  deleteCategory,
} = require("./category");
const {
  createRestaurant,
  editRating,
  editNotes,
  addVisit,
  deleteVisit,
  editDishRanking,
  addDish,
  deleteDish,
  switchRestaurantCategory,
  deleteRestaurant,
} = require("./restaurant");

// Authentication endpoints
exports.verifyToken = onRequest(auth.verifyToken);

// User management endpoints
exports.createUser = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {username, userId, boards} = req.body;

    // Validate required parameters
    if (!username || !userId) {
      return res.status(400).json({error: "Username and userId are required"});
    }

    // Create user with provided parameters
    const user = await createUser(username, userId, boards || []);
    res.json({success: true, user});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Example endpoints (can be removed in production)
exports.helloWorld = onRequest((req, res) => {
  logger.info("Hello logs!", {structuredData: true});
  res.send("Hello from Firebase!");
});

// Add endpoint for getting user boards
exports.getUserBoards = onRequest(async (req, res) => {
  try {
    // Get userId from request body
    const {userId} = req.body;

    // Validate required parameter
    if (!userId) {
      return res.status(400).json({error: "userId is required"});
    }

    // Get the user's boards
    const boards = await getUserBoards(userId);
    res.json({success: true, boards});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for updating user boards
exports.updateUserBoards = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {userId, boards} = req.body;

    // Validate required parameters
    if (!userId || !Array.isArray(boards)) {
      return res.status(400).json({error: "userId and boards array are required"});
    }

    // Update the user's boards
    const result = await updateUserBoards(userId, boards);
    res.json({success: true, ...result});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for deleting a user
exports.deleteUser = onRequest(async (req, res) => {
  try {
    // Get userId from request body
    const {userId} = req.body;

    // Validate required parameter
    if (!userId) {
      return res.status(400).json({error: "userId is required"});
    }

    // Delete the user and their data
    await deleteUser(userId);
    res.json({success: true, message: "User deleted successfully"});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for removing a user from a board
exports.removeUserFromBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {userId, boardId} = req.body;

    // Validate required parameters
    if (!userId || !boardId) {
      return res.status(400).json({error: "userId and boardId are required"});
    }

    // Remove the user from the board
    await removeUserFromBoard(boardId, userId);
    res.json({success: true, message: "User removed from board successfully"});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for adding a board to a user
exports.addBoardToUser = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {userId, boardCode} = req.body;

    // Validate required parameters
    if (!userId || !boardCode) {
      return res.status(400).json({error: "userId and boardCode are required"});
    }

    // Add board to user
    const boards = await addBoardToUser(userId, boardCode);
    res.json({success: true, boards});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for creating a new board
exports.createBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, name, owner} = req.body;

    // Validate required parameters
    if (!boardId || !name || !owner) {
      return res.status(400).json({error: "boardId, name, and owner are required"});
    }

    // Create the board
    const boardData = await createBoard(boardId, name, owner);
    res.json({success: true, board: boardData});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for editing board name
exports.editBoardName = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, name} = req.body;

    // Validate required parameter
    if (!boardId) {
      return res.status(400).json({error: "boardId is required"});
    }

    // Update the board name
    await editBoardName(boardId, name);
    res.json({success: true, message: "Board name updated successfully"});
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for getting board data
exports.getBoardData = onRequest(async (req, res) => {
  try {
    // Get boardId from request body
    const {boardId} = req.body;

    // Validate required parameter
    if (!boardId) {
      return res.status(400).json({error: "boardId is required"});
    }

    // Get the board data
    const boardData = await getBoardData(boardId);

    if (boardData) {
      res.json({success: true, board: boardData});
    } else {
      res.status(404).json({error: "Board not found"});
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for adding a user to a board
exports.addUserToBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, userId} = req.body;

    // Validate required parameters
    if (!boardId || !userId) {
      return res.status(400).json({error: "boardId and userId are required"});
    }

    // Add user to board
    await addUserToBoard(boardId, userId);
    res.json({
      success: true,
      message: `User ${userId} successfully added to board ${boardId}`,
    });
  } catch (error) {
    console.error(error);
    // Return appropriate status codes based on error type
    if (error.message.includes("does not exist")) {
      if (error.message.includes("Board")) {
        res.status(404).json({error: error.message});
      } else if (error.message.includes("User")) {
        res.status(404).json({error: error.message});
      }
    } else if (error.message.includes("already a member")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for linking a category to a board
exports.linkCategoryToBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, categoryId} = req.body;

    // Validate required parameters
    if (!boardId || !categoryId) {
      return res.status(400).json({error: "boardId and categoryId are required"});
    }

    // Link category to board
    await linkCategoryToBoard(boardId, categoryId);
    res.json({
      success: true,
      message: `Category ${categoryId} successfully linked to board ${boardId}`,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("does not exist")) {
      res.status(404).json({error: error.message});
    } else if (error.message.includes("already in board")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for unlinking a category from a board
exports.unlinkCategoryFromBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, categoryId} = req.body;

    // Validate required parameters
    if (!boardId || !categoryId) {
      return res.status(400).json({error: "boardId and categoryId are required"});
    }

    // Unlink category from board
    await unlinkCategoryFromBoard(boardId, categoryId);
    res.json({
      success: true,
      message: `Category ${categoryId} successfully unlinked from board ${boardId}`,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for deleting a board
exports.deleteBoard = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {boardId, userId} = req.body;

    // Validate required parameters
    if (!boardId || !userId) {
      return res.status(400).json({error: "boardId and userId are required"});
    }

    // Delete the board
    await deleteBoard(boardId, userId);
    res.json({
      success: true,
      message: `Board ${boardId} successfully deleted`,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("not found")) {
      res.status(404).json({error: error.message});
    } else if (error.message.includes("Only the board owner")) {
      res.status(403).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for creating a category
exports.createCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, name, caption, boardId} = req.body;

    // Validate required parameters
    if (!categoryId || !name || !boardId) {
      return res.status(400).json({error: "categoryId, name, and boardId are required"});
    }

    // Create the category
    const categoryData = await createCategory(categoryId, name, caption, boardId);
    res.json({
      success: true,
      category: categoryData,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("Invalid category ID")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for editing a category
exports.editCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, name, caption} = req.body;

    // Validate required parameter
    if (!categoryId) {
      return res.status(400).json({error: "categoryId is required"});
    }

    // Edit the category
    await editCategory(categoryId, name, caption);
    res.json({
      success: true,
      message: `Category ${categoryId} successfully updated`,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for adding a restaurant to a category
exports.addRestaurantToCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, restaurantId} = req.body;

    // Validate required parameters
    if (!categoryId || !restaurantId) {
      return res.status(400).json({error: "categoryId and restaurantId are required"});
    }

    // Add restaurant to category
    const restaurants = await addRestaurantToCategory(categoryId, restaurantId);
    res.json({
      success: true,
      restaurants,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be a string")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for removing a restaurant from a category
exports.removeRestaurantFromCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, restaurantId} = req.body;

    // Validate required parameters
    if (!categoryId || !restaurantId) {
      return res.status(400).json({error: "categoryId and restaurantId are required"});
    }

    // Remove restaurant from category
    const restaurants = await removeRestaurantFromCategory(categoryId, restaurantId);
    res.json({
      success: true,
      restaurants,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be a string")) {
      res.status(400).json({error: error.message});
    } else if (error.message.includes("not found in category")) {
      res.status(404).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for deleting a category
exports.deleteCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, boardId} = req.body;

    // Validate required parameters
    if (!categoryId || !boardId) {
      return res.status(400).json({error: "categoryId and boardId are required"});
    }

    // Delete the category
    await deleteCategory(categoryId, boardId);
    res.json({
      success: true,
      message: `Category ${categoryId} successfully deleted`,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("not found")) {
      res.status(404).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for creating a restaurant
exports.createRestaurant = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {categoryId, restaurantId, data} = req.body;

    // Validate required parameters
    if (!categoryId || !restaurantId || !data) {
      return res.status(400).json({
        error: "categoryId, restaurantId, and data object are required",
      });
    }

    // Create the restaurant
    const restaurantData = await createRestaurant(categoryId, restaurantId, data);
    res.json({
      success: true,
      restaurant: restaurantData,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("Missing required field") ||
        error.message.includes("must be a number between")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for editing a restaurant rating
exports.editRating = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, ratingNumber, ratingValue} = req.body;

    // Validate required parameters
    if (!restaurantId || ratingNumber === undefined || ratingValue === undefined) {
      return res.status(400).json({
        error: "restaurantId, ratingNumber, and ratingValue are required",
      });
    }

    // Edit the rating
    const data = await editRating(restaurantId, ratingNumber, ratingValue);
    res.json({
      success: true,
      update: data,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for editing restaurant notes
exports.editNotes = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, notes} = req.body;

    // Validate required parameters
    if (!restaurantId || notes === undefined) {
      return res.status(400).json({
        error: "restaurantId and notes are required",
      });
    }

    // Edit the notes
    const data = await editNotes(restaurantId, notes);
    res.json({
      success: true,
      update: data,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for adding a restaurant visit
exports.addVisit = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, visitDate} = req.body;

    // Validate required parameters
    if (!restaurantId || !visitDate) {
      return res.status(400).json({
        error: "restaurantId and visitDate are required",
      });
    }

    // Add the visit
    const visits = await addVisit(restaurantId, visitDate);
    res.json({
      success: true,
      visits,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for deleting a restaurant visit
exports.deleteVisit = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId} = req.body;

    // Validate required parameter
    if (!restaurantId) {
      return res.status(400).json({
        error: "restaurantId is required",
      });
    }

    // Delete the visit
    const visits = await deleteVisit(restaurantId);
    res.json({
      success: true,
      visits,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});

// Add endpoint for editing restaurant dishes
exports.editDishRanking = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, dishes} = req.body;

    // Validate required parameters
    if (!restaurantId || !dishes) {
      return res.status(400).json({
        error: "restaurantId and dishes are required",
      });
    }

    // Update the dishes
    const updatedDishes = await editDishRanking(restaurantId, dishes);
    res.json({
      success: true,
      dishes: updatedDishes,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for adding a restaurant dish
exports.addDish = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, dish} = req.body;

    // Validate required parameters
    if (!restaurantId || !dish) {
      return res.status(400).json({
        error: "restaurantId and dish are required",
      });
    }

    // Add the dish
    const dishes = await addDish(restaurantId, dish);
    res.json({
      success: true,
      dishes,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for deleting a restaurant dish
exports.deleteDish = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, dish} = req.body;

    // Validate required parameters
    if (!restaurantId || !dish) {
      return res.status(400).json({
        error: "restaurantId and dish are required",
      });
    }

    // Delete the dish
    const dishes = await deleteDish(restaurantId, dish);
    res.json({
      success: true,
      dishes,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else if (error.message.includes("not found")) {
      res.status(404).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for switching restaurant category
exports.switchRestaurantCategory = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId, newCategoryId} = req.body;

    // Validate required parameters
    if (!restaurantId || !newCategoryId) {
      return res.status(400).json({
        error: "restaurantId and newCategoryId are required",
      });
    }

    // Switch the category
    const restaurantData = await switchRestaurantCategory(restaurantId, newCategoryId);
    res.json({
      success: true,
      restaurant: restaurantData,
    });
  } catch (error) {
    console.error(error);
    if (error.message.includes("must be")) {
      res.status(400).json({error: error.message});
    } else if (error.message.includes("not found")) {
      res.status(404).json({error: error.message});
    } else {
      res.status(500).json({error: error.message});
    }
  }
});

// Add endpoint for deleting a restaurant
exports.deleteRestaurant = onRequest(async (req, res) => {
  try {
    // Get parameters from request body
    const {restaurantId} = req.body;

    // Validate required parameter
    if (!restaurantId) {
      return res.status(400).json({
        error: "restaurantId is required",
      });
    }

    // Delete the restaurant
    await deleteRestaurant(restaurantId);
    res.json({
      success: true,
      message: `Restaurant ${restaurantId} successfully deleted`,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({error: error.message});
  }
});
