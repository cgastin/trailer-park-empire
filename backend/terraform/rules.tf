# ---------------------------------------------------------------------------
# Firestore Security Rules
# Reads backend/firestore.rules and deploys it to the Firestore database.
# ---------------------------------------------------------------------------

resource "google_firebaserules_ruleset" "firestore" {
  provider = google-beta
  project  = google_firebase_project.tpe.project

  source {
    files {
      name    = "firestore.rules"
      content = file("${path.module}/../firestore.rules")
    }
  }

  depends_on = [google_firestore_database.tpe]
}

resource "google_firebaserules_release" "firestore" {
  provider     = google-beta
  project      = google_firebase_project.tpe.project
  name         = "cloud.firestore"
  ruleset_name = google_firebaserules_ruleset.firestore.name
}
