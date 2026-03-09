variable "project_id" {
  description = "GCP project ID (globally unique, e.g. tpe-prod-abc123)"
  type        = string
}

variable "project_name" {
  description = "GCP project display name"
  type        = string
  default     = "Trailer Park Empire"
}

variable "billing_account" {
  description = "GCP billing account ID (format: XXXXXX-XXXXXX-XXXXXX)"
  type        = string
}

variable "org_id" {
  description = "GCP organization ID. Leave empty for personal GCP accounts."
  type        = string
  default     = ""
}

variable "region" {
  description = "Firestore region"
  type        = string
  default     = "us-central"
}
