output "project_id" {
  description = "GCP project ID"
  value       = google_project.tpe.project_id
}

output "api_key" {
  description = "Firebase Web API key (also written to game/data/firebase_config.json)"
  value       = data.google_firebase_web_app_config.tpe.api_key
}

output "app_id" {
  description = "Firebase Web App ID"
  value       = google_firebase_web_app.tpe.app_id
}
