output "job_name" {
  description = "Configured Cloud Run Job name."
  value       = google_cloud_run_v2_job.replication.name
}
