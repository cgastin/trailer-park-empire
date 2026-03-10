terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }

  # Remote state — keeps terraform.tfstate (which contains the SCRYPT signer key)
  # off local disk. Migrate from local state with:
  #   terraform init -migrate-state
  # The bucket is created by google_storage_bucket.tf_state below on first apply.
  # Uncomment after running: terraform apply -target=google_storage_bucket.tf_state
  # then run: terraform init -migrate-state
  # backend "gcs" {
  #   bucket = "<your-project-id>-tf-state"
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  user_project_override = true
}

provider "google-beta" {
  user_project_override = true
}

# ---------------------------------------------------------------------------
# GCP Project
# ---------------------------------------------------------------------------

resource "google_project" "tpe" {
  provider        = google-beta
  name            = var.project_name
  project_id      = var.project_id
  billing_account = var.billing_account

  # org_id is optional — omit when using a personal GCP account
  org_id = var.org_id != "" ? var.org_id : null
}

# ---------------------------------------------------------------------------
# Required APIs
# ---------------------------------------------------------------------------

locals {
  required_apis = [
    "firebase.googleapis.com",
    "identitytoolkit.googleapis.com",
    "firestore.googleapis.com",
    "firebaserules.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(local.required_apis)

  provider           = google-beta
  project            = google_project.tpe.project_id
  service            = each.value
  disable_on_destroy = false

  depends_on = [google_project.tpe]
}

# ---------------------------------------------------------------------------
# Firebase Project
# ---------------------------------------------------------------------------

resource "google_firebase_project" "tpe" {
  provider = google-beta
  project  = google_project.tpe.project_id

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Firebase Web App
# ---------------------------------------------------------------------------

resource "google_firebase_web_app" "tpe" {
  provider     = google-beta
  project      = google_firebase_project.tpe.project
  display_name = "Trailer Park Empire"

  depends_on = [google_firebase_project.tpe]
}

data "google_firebase_web_app_config" "tpe" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.tpe.app_id
  project    = google_firebase_project.tpe.project
}

# ---------------------------------------------------------------------------
# Firestore Database
# ---------------------------------------------------------------------------

resource "google_firestore_database" "tpe" {
  provider    = google-beta
  project     = google_firebase_project.tpe.project
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Write game/data/firebase_config.json
# ---------------------------------------------------------------------------

resource "local_file" "firebase_config" {
  filename = "${path.module}/../../game/data/firebase_config.json"
  content = jsonencode({
    api_key            = data.google_firebase_web_app_config.tpe.api_key
    project_id         = google_project.tpe.project_id
    auth_base_url      = "https://identitytoolkit.googleapis.com/v1"
    token_base_url     = "https://securetoken.googleapis.com/v1"
    firestore_base_url = "https://firestore.googleapis.com/v1"
  })
}

# ---------------------------------------------------------------------------
# Terraform Remote State Bucket
# Stores terraform.tfstate in GCS instead of local disk.
# The bucket name must match the backend "gcs" block above.
#
# IMPORTANT: Bootstrap order —
#   1. Comment out the backend "gcs" block above and run `terraform apply`
#      to create this bucket with local state.
#   2. Uncomment the backend "gcs" block and run `terraform init -migrate-state`
#      to move state into the bucket.
#   3. Delete the local terraform.tfstate file.
# ---------------------------------------------------------------------------

resource "google_storage_bucket" "tf_state" {
  provider                    = google-beta
  project                     = google_project.tpe.project_id
  name                        = "${var.project_id}-tf-state"
  location                    = "US"
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.apis]
}
