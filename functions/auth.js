const functions = require('firebase-functions');
const admin = require('firebase-admin');

// Ensure admin is initialized only once
if (!admin.apps.length) {
  admin.initializeApp();
}

// NOTE: This was a shit attempt at trying to do token authentication. 
// You're going to need to study authentication flow before you can 
// implement this correctly. 
// Decide if you want to only do service account auth for now, or
// handle the auth flow for all users. 


// Example: Function to verify an ID token
exports.verifyToken = functions.https.onRequest(async (req, res) => {
  const idToken = req.headers.authorization?.split('Bearer ')[1];

  if (!idToken) {
    return res.status(401).send({ error: 'Unauthorized' });
  }

  try {
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    res.status(200).send({ message: 'Token verified', uid: decodedToken.uid });
  } catch (error) {
    console.error("Error verifying token:", error);
    res.status(403).send({ error: 'Invalid token' });
  }
});
