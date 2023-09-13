from pathlib import Path
import pandas as pd
from prefect import flow, task
from hdfs3 import HDFileSystem

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

@task(log_prints=True)
def write_hdfs(path: Path) -> None:
    '''write file into HDFS container'''

    namenode_host='localhost'
    port=8020

    # Connect with HaDoop File System
    print('Connecting to HDFS...')
    hdfs = HDFileSystem(namenode_host, port)
    print('Done...')

    #Create dir
    dir = '/phong_huynh/'
    if not hdfs.exists(dir):
        print(f"Directory {dir} doesn't exists! Create {dir}")
        hdfs.mkdir(dir)
        print('Done...')

    local_path = path
    target = str(local_path).split('/')[-1]

    # Pusing file into HDFS
    try:
        print(f'HDFS: Start pusing file')
        hdfs.put(local_path, f'{dir}{target}')
        print(f'HDFS: Done pushing {path} into {dir}')
    except Exception as e:
        print(f"Error: {e}")


@flow()
def etl_to_hdfs() -> None:
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
    write_hdfs(path)
    

if __name__ == "__main__":
    etl_to_hdfs()
