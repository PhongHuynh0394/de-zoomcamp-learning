from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web to pandas dataframe"""

    return pd.read_parquet(dataset_url)


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """write dataframe out locally as parquet file"""
    path = Path(f"../data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    # df['tpep_pickup_dropoff'] = pd.to_datetime(df['tpep_pickup_dropoff'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_gcs(path: Path) -> None:
    """write file to GCS"""

@flow()
def etl_web_to_gcs() -> None:
    """The main etl function"""
    color = "yellow"
    year = 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url=f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}.parquet"

    print(dataset_url)
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)
    

if __name__ == "__main__":
    etl_web_to_gcs()
