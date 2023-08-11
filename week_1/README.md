# Week 1:

## Pgadmin connection
Check localhost:8080

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