mock_provider "google" {}

run "sanitized_job_contract" {
  command = plan

  variables {
    project_id            = "example-project"
    service_account_email = "replication@example-project.iam.gserviceaccount.com"
    image                 = "us-docker.pkg.dev/example-project/edge/replication@sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
  }

  assert {
    condition     = google_cloud_run_v2_job.replication.template[0].template[0].max_retries == 1
    error_message = "job retries must remain bounded"
  }
}
