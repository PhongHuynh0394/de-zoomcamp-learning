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
docker exec -it notebookk bash
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


