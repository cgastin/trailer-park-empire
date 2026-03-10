#!/usr/bin/env bash
# bootstrap.sh — run ONCE before the first `terraform apply`
#
# Enables the two APIs that Terraform itself needs to enable all other APIs
# on a brand-new GCP project. This is a known bootstrapping requirement.
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

echo "Bootstrapping Service Usage and Cloud Resource Manager APIs for project: $PROJECT_ID"

gcloud services enable \
  serviceusage.googleapis.com \
  cloudresourcemanager.googleapis.com \
  --project="$PROJECT_ID"

echo "Done. You can now run: terraform init && terraform apply"
