# ---------------------------------------------------------------------------
# Identity Platform (Firebase Auth)
# Enables anonymous and email/password sign-in providers.
# ---------------------------------------------------------------------------

resource "google_identity_platform_config" "tpe" {
  provider = google-beta
  project  = google_firebase_project.tpe.project

  sign_in {
    allow_duplicate_emails = false

    anonymous {
      enabled = true
    }

    email {
      enabled           = true
      password_required = true
    }
  }

  depends_on = [
    google_project_service.apis,
    google_firebase_project.tpe,
  ]
}
