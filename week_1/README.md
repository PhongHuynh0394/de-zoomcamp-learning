# Week 1

## Pgadmin connection
**Prerequisite**: `Docker`

Just run `docker compose up -d`

Then check localhost:8080

We need to add all container into 1 specify network to find each other (this time, localhost change into container name - this case it is "postgres" instead of "localhost")

## Run ingestion file
File type: `Parquet`
Source: [NY taxi data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
```bash
# yellow taxi data
URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

```
To push data into database, go into notebook folder and run the .py file with the following params:
```python
python3 data_ingestion.py \
    --user=root \
    --password=root \
    --host=postgres \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
**Note**: The file should be run inside notebook container.

```bash
docker exec -it notebook bash
```

```bash
# For green taxi 2019
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz 
# For zone
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

## GCP Intro and Terrafrom
### Google Cloud Authentication
**Prerequisite**: `gcloud` `Terrafrom`

Create a project, go to `IAM & Admin` and create a service account. Then download the .json file key

Export the path to JSON
```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-json/file.json>

gcloud auth application-default login
```

**Set up for Acess**
1. `IAM Roles` for Services account:
    - Go to IAM section of IAM & Admin https://console.cloud.google.com/iam-admin/iam
    - Add principal: Storage Admin + Storage Object Admin + BigQuery Admin

2. Enable some APIS for project:
    - https://console.cloud.google.com/apis/library/iam.googleapis.com
    - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

### Terraform

Set up Infra by using Terraform. just run:
```bash
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan

# Create infra
terraform apply #can you -var="project=<project-id" instead

# Delete infra after done, to avoid costs
terraform destroy
```

When apply successfully, you will get something like this:
```bash
var.credentials
  Your GCP IAM credentials path

  Enter a value: 

var.project
  Your GCP Project ID

  Enter a value: 


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "us-central1"
      + max_time_travel_hours      = (known after apply)
      + project                    = "de-zoomcamp-193031"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US-CENTRAL1"
      + name                        = "de_datalake_de-zoomcamp-193031"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/de-zoomcamp-193031/datasets
google_storage_bucket.data-lake-bucket: Creation complete after 1s [id=de_datalake_de-zoomcamp-193031

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

Note: The project ID is used for example

## HomeWork
- Ques 1: --rm
- Ques 2: 0.42.0
- Ques 3: 15612
- Ques 4: 2019-09-26
- Ques 5: Bronx, Manhattan, Queens
- Ques 6: JFK AirPort
