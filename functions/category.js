const admin = require("firebase-admin");
const {linkCategoryToBoard, unlinkCategoryFromBoard} = require("./board");

/**
 * Add a category to the specified board.
 * @param {string} categoryId - The unique identifier for the category.
 * @param {string} name - The name of the category.
 * @param {string} caption - The caption for the category.
 * @param {string} boardId - The board to add this category to.
 * @return {Promise<Object>} The created category data.
 * @throws {Error} If categoryId is invalid.
 */
async function createCategory(categoryId, name, caption, boardId) {
  try {
    if (!categoryId || typeof categoryId !== "string") {
      throw new Error("Invalid category ID: must be a non-empty string.");
    }

    const path = `categories/${categoryId}`;
    const categoryData = {
      name,
      caption,
      restaurants: [],
    };

    // Write category data first
    await admin.database().ref(path).set(categoryData);
    console.log(`Category ${categoryId} created successfully`);

    // Then link the category to the board
    await linkCategoryToBoard(boardId, categoryId);

    return categoryData;
  } catch (error) {
    console.error(`Error creating category: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Edit an existing category's name or caption.
 * @param {string} categoryId - The unique identifier for the category.
 * @param {string} [name] - The new name for the category (optional).
 * @param {string} [caption] - The new caption for the category (optional).
 * @return {Promise<void>}
 */
async function editCategory(categoryId, name, caption) {
  try {
    const path = `categories/${categoryId}`;
    const updates = {};

    if (name) {
      updates.name = name;
    }
    if (caption) {
      updates.caption = caption;
    }

    await admin.database().ref(path).update(updates);
    console.log(`Category ${categoryId} updated successfully`);
  } catch (error) {
    console.error(`Error updating category: ${error.message}`);
    throw new Error("Failed to update category");
  }
}

/**
 * Add a restaurant ID to a category's restaurants array.
 * @param {string} categoryId - The category ID to update.
 * @param {string} restaurantId - The restaurant ID to add.
 * @return {Promise<Array<string>>} Updated list of restaurant IDs.
 * @throws {Error} If restaurantId is not a string.
 */
async function addRestaurantToCategory(categoryId, restaurantId) {
  try {
    if (typeof restaurantId !== "string") {
      throw new Error("Restaurant ID must be a string");
    }

    const path = `categories/${categoryId}/restaurants`;
    const snapshot = await admin.database().ref(path).get();
    const restaurants = snapshot.val() || [];

    restaurants.push(restaurantId);
    await admin.database().ref(path).set(restaurants);
    console.log(`Restaurant ${restaurantId} added to category ${categoryId}`);
    return restaurants;
  } catch (error) {
    console.error(`Error adding restaurant to category: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Remove a restaurant ID from a category's restaurants array.
 * @param {string} categoryId - The category ID to update.
 * @param {string} restaurantId - The restaurant ID to remove.
 * @return {Promise<Array<string>>} Updated list of restaurant IDs.
 * @throws {Error} If restaurantId is not a string or not found in category.
 */
async function removeRestaurantFromCategory(categoryId, restaurantId) {
  try {
    if (typeof restaurantId !== "string") {
      throw new Error("Restaurant ID must be a string");
    }

    const path = `categories/${categoryId}/restaurants`;
    const snapshot = await admin.database().ref(path).get();
    const restaurants = snapshot.val() || [];

    const index = restaurants.indexOf(restaurantId);
    if (index === -1) {
      throw new Error(`Restaurant ${restaurantId} not found in category ${categoryId}`);
    }

    restaurants.splice(index, 1);
    await admin.database().ref(path).set(restaurants);
    console.log(`Restaurant ${restaurantId} removed from category ${categoryId}`);
    return restaurants;
  } catch (error) {
    console.error(`Error removing restaurant from category: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Delete a category from the specified board and remove associated restaurants.
 * @param {string} categoryId - The category ID to delete.
 * @param {string} boardId - The board ID to remove the category from.
 * @return {Promise<void>}
 */
async function deleteCategory(categoryId, boardId) {
  try {
    // Get all restaurants associated with the category
    const categoryPath = `categories/${categoryId}`;
    const categorySnapshot = await admin.database().ref(categoryPath).get();
    const categoryData = categorySnapshot.val() || {};
    const restaurants = categoryData.restaurants || [];

    // Delete each restaurant
    for (const restaurantId of restaurants) {
      await admin.database().ref(`restaurants/${restaurantId}`).remove();
      console.log(`Restaurant ${restaurantId} deleted`);
    }

    // Unlink the category from the board
    await unlinkCategoryFromBoard(boardId, categoryId);

    // Delete the category
    await admin.database().ref(categoryPath).remove();
    console.log(`Category ${categoryId} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting category: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

module.exports = {
  createCategory,
  editCategory,
  addRestaurantToCategory,
  removeRestaurantFromCategory,
  deleteCategory,
};
