# Backend

Firebase backend configuration for Trailer Park Empire.

## Contents

- `firestore.rules` — Firestore security rules. Authenticated users can only read/write their own save document.

## Deploying

Requires the Firebase CLI (`npm install -g firebase-tools`).

```bash
# Login
firebase login

# Deploy Firestore rules only
firebase deploy --only firestore:rules --project YOUR_PROJECT_ID
```

## Firebase Console Setup

Before deploying, ensure these are enabled in the Firebase Console:

1. **Authentication** → Anonymous provider enabled
2. **Authentication** → Email/Password provider enabled
3. **Firestore Database** → created (start in test mode, then apply rules above)

## Firestore Security Rules

The rules in `firestore.rules` enforce:
- Only authenticated users can access the database
- Users can only read/write their own document at `users/{uid}/save/game`

## Social Auth (Future — Milestone 4b)

Social auth (Apple, Google, Facebook) requires Cloud Functions to handle OAuth
token exchange and deep link routing. This is a separate task after Milestone 5.
