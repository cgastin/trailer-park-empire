#!/usr/bin/env bash
# bootstrap.sh — run ONCE before the first `terraform apply`
#
# Step 1: Enables the two APIs Terraform needs before it can enable anything else.
# Step 2: First apply uses local state to create the GCS state bucket.
# Step 3: Migrates state to GCS so terraform.tfstate never lives on local disk.
#
# Usage:
#   chmod +x bootstrap.sh
#   ./bootstrap.sh <project-id>

set -euo pipefail

PROJECT_ID="${1:-}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "Usage: ./bootstrap.sh <project-id>" >&2
  exit 1
fi

# --- Step 1: Enable bootstrap APIs ----------------------------------------
echo "==> Step 1: Enabling bootstrap APIs for project: $PROJECT_ID"

gcloud services enable \
  serviceusage.googleapis.com \
  cloudresourcemanager.googleapis.com \
  --project="$PROJECT_ID"

echo "Bootstrap APIs enabled."

# --- Step 2: First apply with local state ----------------------------------
echo ""
echo "==> Step 2: First terraform apply (local state — creates GCS state bucket)"
echo "    Action required: comment out the backend \"gcs\" block in main.tf, then press Enter."
echo "    (The GCS bucket must exist before Terraform can use it as a backend.)"
read -r -p "    Press Enter when ready..."

terraform init
terraform apply -target=google_storage_bucket.tf_state

# --- Step 3: Migrate state to GCS ------------------------------------------
echo ""
echo "==> Step 3: Migrating state to GCS"
echo "    Action required: uncomment the backend \"gcs\" block in main.tf, then press Enter."
read -r -p "    Press Enter when ready..."

terraform init -migrate-state

echo ""
echo "==> Done. State is now stored in GCS. You can delete terraform.tfstate locally."
echo "    Run: terraform apply   to provision the remaining resources."
