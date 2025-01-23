// auth.js
const admin = require("firebase-admin");

// Initialize Firebase Admin SDK if not already initialized
if (!admin.apps.length) {
  admin.initializeApp();
}

// Verify Token Function
exports.verifyToken = async (req, res) => {
  const idToken = req.body.idToken; // Expecting the ID token in the request body

  if (!idToken) {
    return res.status(400).send({error: "ID token is required"});
  }

  try {
    // Verify the ID token
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    res.status(200).send({
      message: "Token verified successfully",
      uid: decodedToken.uid,
      email: decodedToken.email,
    });
  } catch (error) {
    console.error("Error verifying token:", error);
    res.status(401).send({error: "Invalid or expired token"});
  }
};
