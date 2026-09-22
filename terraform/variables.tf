variable "project_id" {
  description = "Owner-supplied Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Cloud Run region."
  type        = string
  default     = "us-central1"
}

variable "name" {
  description = "Cloud Run Job name."
  type        = string
  default     = "edge-evidence-replication"
}

variable "image" {
  description = "Immutable replication image reference, preferably a digest."
  type        = string

  validation {
    condition     = can(regex("@sha256:[0-9a-f]{64}$", var.image))
    error_message = "image must be pinned by sha256 digest"
  }
}

variable "service_account_email" {
  description = "Existing least-privilege service account email. This module does not create IAM."
  type        = string
}

variable "args" {
  description = "Bounded replication CLI arguments supplied by the owner."
  type        = list(string)
  default     = ["--help"]
}

variable "environment" {
  description = "Non-secret environment variables."
  type        = map(string)
  default     = {}
}
