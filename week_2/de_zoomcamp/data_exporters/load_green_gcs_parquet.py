import pyarrow as pa 
import pyarrow.parquet as pq
from pandas import DataFrame
from os import path
import os

gg_service_key = "/home/src/" + os.getenv('GOOGLE_SERVICE_KEY')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gg_service_key
bucket_name = "de_datalake_de-zoomcamp-396014"
project_id = "de-zoomcamp-396014"
table_name = "green_taxi_data"
root_path = f"{bucket_name}/{table_name}"

    
@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )


