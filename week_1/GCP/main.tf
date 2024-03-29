terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  credentials = file(var.credentials) # use this if do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# data lake bucket (GCS)
resource "google_storage_bucket" "data-lake-bucket" {
  name = "${local.data_lake_bucket}_${var.project}" #Concat DL bucket & project name
  location = var.region
  force_destroy = true

  # optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 1 //days
    }
  }
}
# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}
