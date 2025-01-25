const admin = require("firebase-admin");
const {addRestaurantToCategory, removeRestaurantFromCategory} = require("./category");

/**
 * Add a restaurant and associate it with a category.
 * @param {string} categoryId - The category ID to associate the restaurant with.
 * @param {string} restaurantId - The unique ID for the restaurant.
 * @param {Object} data - Object containing restaurant details.
 * @param {string} data.name - The name of the restaurant.
 * @param {number} data.rating_1 - First rating (0-10).
 * @param {number} data.rating_2 - Second rating (0-10).
 * @param {number} data.rating_3 - Third rating (0-10).
 * @param {string} data.notes - Notes about the restaurant.
 * @param {Array<string>} data.visits - List of visit dates.
 * @param {string} data.location - Restaurant location.
 * @param {Array<string>} data.dishes - List of dishes.
 * @param {string} data.photo - URL to restaurant photo.
 * @return {Promise<Object>} The created restaurant data.
 * @throws {Error} If required fields are missing or invalid.
 */
async function createRestaurant(categoryId, restaurantId, data) {
  try {
    const requiredFields = [
      "name",
      "rating_1",
      "rating_2",
      "rating_3",
      "notes",
      "visits",
      "location",
      "dishes",
      "photo",
    ];

    // Check for required fields
    for (const field of requiredFields) {
      if (!(field in data)) {
        throw new Error(`Missing required field in restaurant creation: ${field}`);
      }
    }

    // Validate ratings
    const ratingFields = ["rating_1", "rating_2", "rating_3"];
    for (const field of ratingFields) {
      const rating = data[field];
      if (typeof rating !== "number" || rating < 0 || rating > 10) {
        throw new Error(`${field} must be a number between 0 and 10`);
      }
    }

    // Add category reference to restaurant data
    const restaurantData = {
      ...data,
      category_code: categoryId,
    };

    // Write restaurant data
    const path = `restaurants/${restaurantId}`;
    await admin.database().ref(path).set(restaurantData);
    console.log(`Restaurant ${restaurantId} created successfully`);

    // Add restaurant to category
    await addRestaurantToCategory(categoryId, restaurantId);

    return restaurantData;
  } catch (error) {
    console.error(`Error creating restaurant: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Edit a specific rating of a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {number} ratingNumber - Integer 1-3 specifying which rating to update.
 * @param {number} ratingValue - The new rating value.
 * @return {Promise<Object>} Object containing the updated rating field and value.
 * @throws {Error} If rating number or value is invalid.
 */
async function editRating(restaurantId, ratingNumber, ratingValue) {
  try {
    // Validate rating number
    if (!Number.isInteger(ratingNumber) || ![1, 2, 3].includes(ratingNumber)) {
      throw new Error("rating_number must be 1, 2, or 3");
    }

    // Validate rating value
    if (typeof ratingValue !== "number" || ratingValue < 0 || ratingValue > 10) {
      throw new Error("rating_value must be a number between 0 and 10");
    }

    const ratingField = `rating_${ratingNumber}`;
    const data = {[ratingField]: ratingValue};

    // Update the rating
    const path = `restaurants/${restaurantId}`;
    await admin.database().ref(path).update(data);
    console.log(`Rating ${ratingNumber} updated for restaurant ${restaurantId}`);

    return data;
  } catch (error) {
    console.error(`Error updating rating: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Edit the notes for a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {string} notes - String containing the new notes.
 * @return {Promise<Object>} Object containing the updated notes.
 * @throws {Error} If notes is not a string.
 */
async function editNotes(restaurantId, notes) {
  try {
    if (typeof notes !== "string") {
      throw new Error("notes must be a string");
    }

    const data = {notes};
    const path = `restaurants/${restaurantId}`;
    await admin.database().ref(path).update(data);
    console.log(`Notes updated for restaurant ${restaurantId}`);

    return data;
  } catch (error) {
    console.error(`Error updating notes: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Add a visit date to a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {string} visitDate - String containing the visit date.
 * @return {Promise<Array<string>>} Updated list of visit dates.
 * @throws {Error} If visitDate is not a string.
 */
async function addVisit(restaurantId, visitDate) {
  try {
    if (typeof visitDate !== "string") {
      throw new Error("visit_date must be a string");
    }

    const path = `restaurants/${restaurantId}/visits`;
    const snapshot = await admin.database().ref(path).get();
    const visits = snapshot.val() || [];

    visits.push(visitDate);
    await admin.database().ref(path).set(visits);
    console.log(`Visit date added to restaurant ${restaurantId}`);

    return visits;
  } catch (error) {
    console.error(`Error adding visit date: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Delete the most recent visit date from a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @return {Promise<Array<string>>} Updated list of visit dates.
 */
async function deleteVisit(restaurantId) {
  try {
    const path = `restaurants/${restaurantId}/visits`;
    const snapshot = await admin.database().ref(path).get();
    const visits = snapshot.val() || [];

    if (visits.length > 0) {
      visits.pop();
      await admin.database().ref(path).set(visits);
      console.log(`Most recent visit deleted from restaurant ${restaurantId}`);
    }

    return visits;
  } catch (error) {
    console.error(`Error deleting visit date: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Edit the dishes for a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {Array<string>} dishes - Array containing the new ordered list of dishes.
 * @return {Promise<Array<string>>} Updated list of dishes.
 * @throws {Error} If dishes is not an array.
 */
async function editDishRanking(restaurantId, dishes) {
  try {
    if (!Array.isArray(dishes)) {
      throw new Error("dishes must be an array");
    }

    const path = `restaurants/${restaurantId}/dishes`;
    await admin.database().ref(path).set(dishes);
    console.log(`Dishes updated for restaurant ${restaurantId}`);

    return dishes;
  } catch (error) {
    console.error(`Error updating dishes: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Add a dish to a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {string} dish - String containing the dish name to add.
 * @return {Promise<Array<string>>} Updated list of dishes.
 * @throws {Error} If dish is not a string.
 */
async function addDish(restaurantId, dish) {
  try {
    if (typeof dish !== "string") {
      throw new Error("dish must be a string");
    }

    const path = `restaurants/${restaurantId}/dishes`;
    const snapshot = await admin.database().ref(path).get();
    const dishes = snapshot.val() || [];

    dishes.push(dish);
    await admin.database().ref(path).set(dishes);
    console.log(`Dish added to restaurant ${restaurantId}`);

    return dishes;
  } catch (error) {
    console.error(`Error adding dish: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Delete a dish from a restaurant.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {string} dish - String containing the dish name to delete.
 * @return {Promise<Array<string>>} Updated list of dishes.
 * @throws {Error} If dish is not a string or not found.
 */
async function deleteDish(restaurantId, dish) {
  try {
    if (typeof dish !== "string") {
      throw new Error("dish must be a string");
    }

    const path = `restaurants/${restaurantId}/dishes`;
    const snapshot = await admin.database().ref(path).get();
    const dishes = snapshot.val() || [];

    const index = dishes.indexOf(dish);
    if (index === -1) {
      throw new Error(`Dish "${dish}" not found in restaurant ${restaurantId}`);
    }

    dishes.splice(index, 1);
    await admin.database().ref(path).set(dishes);
    console.log(`Dish deleted from restaurant ${restaurantId}`);

    return dishes;
  } catch (error) {
    console.error(`Error deleting dish: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Change a restaurant's category.
 * @param {string} restaurantId - The restaurant ID to update.
 * @param {string} newCategoryId - String containing the new category ID.
 * @return {Promise<Object>} Updated restaurant data.
 * @throws {Error} If category ID is not a string or restaurant not found.
 */
async function switchRestaurantCategory(restaurantId, newCategoryId) {
  try {
    if (typeof newCategoryId !== "string") {
      throw new Error("Category ID must be a string");
    }

    const path = `restaurants/${restaurantId}`;
    const snapshot = await admin.database().ref(path).get();
    const restaurantData = snapshot.val();

    if (!restaurantData) {
      throw new Error(`Restaurant ${restaurantId} not found`);
    }

    const oldCategoryId = restaurantData.category_code;
    restaurantData.category_code = newCategoryId;

    // Update restaurant data first
    await admin.database().ref(path).set(restaurantData);

    // Remove restaurant from old category
    await removeRestaurantFromCategory(oldCategoryId, restaurantId);

    // Add restaurant to new category
    await addRestaurantToCategory(newCategoryId, restaurantId);

    console.log(`Restaurant ${restaurantId} moved to category ${newCategoryId}`);
    return restaurantData;
  } catch (error) {
    console.error(`Error switching restaurant category: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

/**
 * Delete a restaurant.
 * @param {string} restaurantId - The restaurant ID to delete.
 * @return {Promise<void>}
 */
async function deleteRestaurant(restaurantId) {
  try {
    const path = `restaurants/${restaurantId}`;
    // Get restaurant data first
    const snapshot = await admin.database().ref(path).get();
    const restaurantData = snapshot.val();

    // Remove from category if it exists and has a category code
    if (restaurantData && restaurantData.category_code) {
      await removeRestaurantFromCategory(restaurantData.category_code, restaurantId);
    }

    // Delete the restaurant
    await admin.database().ref(path).remove();
    console.log(`Restaurant ${restaurantId} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting restaurant: ${error.message}`);
    throw error; // Re-throw to maintain the error message
  }
}

module.exports = {
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
};
