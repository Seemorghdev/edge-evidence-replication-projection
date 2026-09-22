resource "google_cloud_run_v2_job" "replication" {
  project  = var.project_id
  name     = var.name
  location = var.region

  template {
    template {
      service_account = var.service_account_email
      max_retries     = 1
      timeout         = "120s"

      containers {
        image = var.image
        args  = var.args

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }

        dynamic "env" {
          for_each = var.environment
          content {
            name  = env.key
            value = env.value
          }
        }
      }
    }
  }
}
