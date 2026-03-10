# Backend

Firebase backend configuration for Trailer Park Empire.

## Terraform Setup (Recommended)

The `terraform/` directory provisions the entire Firebase backend from scratch — GCP project, Firebase, Firestore database, auth providers, and security rules. It also writes `game/data/firebase_config.json` with real values automatically.

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5
- A GCP account with billing enabled
- `gcloud auth application-default login` (authenticates Terraform)

### Usage

```bash
cd backend/terraform

# 1. Copy example vars and fill in real values
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars — set project_id and billing_account

# 2. Bootstrap (run ONCE on a brand-new GCP project)
#    Enables the two APIs Terraform needs before it can enable anything else.
./bootstrap.sh YOUR_PROJECT_ID

# 3. Init providers
terraform init

# 4. Preview what will be created (~15 resources)
terraform plan

# 5. Apply — creates Firebase, Firestore, auth, writes firebase_config.json
terraform apply
```

> **Why the bootstrap step?** On a brand-new GCP project, `serviceusage.googleapis.com`
> is not enabled. Terraform uses that API to enable all other APIs, creating a
> catch-22. The bootstrap script breaks the cycle with a one-time `gcloud` call.

After `apply`, `game/data/firebase_config.json` is updated with real credentials.

### What it creates

| Resource | Description |
|---|---|
| `google_project` | GCP project |
| `google_project_service` (×6) | Required APIs |
| `google_firebase_project` | Firebase enabled on the project |
| `google_firebase_web_app` | Web app registration |
| `google_firestore_database` | Firestore (native mode) |
| `google_identity_platform_config` | Auth: anonymous + email/password |
| `google_firebaserules_ruleset` | Firestore security rules |
| `google_firebaserules_release` | Deploys the ruleset |
| `local_file` | Writes `game/data/firebase_config.json` |

---

## Firebase CLI (Manual / Legacy)

The steps below are preserved for reference. The Terraform approach above is preferred for reproducible setup.

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
