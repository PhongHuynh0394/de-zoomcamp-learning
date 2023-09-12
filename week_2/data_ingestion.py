import pandas as pd
from hdfs3 import HDFileSystem
from time import time
from datetime import timedelta
# import pyarrow.parquet as pq
import os
from sqlalchemy import create_engine
import argparse as arg
from prefect import flow, task
from prefect.tasks import task_input_hash
# from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url) -> pd.DataFrame:
    parquet_file = 'output.parquet'

    #dowload parquet
    try:
        print('Start Downloading...')
        os.system(f"wget {url} -O {parquet_file}")
        print('Download successfully')
    except Exception as e:
        print(e)

    df = pd.read_parquet(parquet_file)
    os.remove(parquet_file)
    return df 

@task(log_prints=True)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    '''drop all object which have passenger_count equal 0'''
    print(f"pre: Missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"pos: Missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def ingest_data(params, df: pd.DataFrame):
    table_name = params.table_name
    chunksize = 100_000
    df.to_csv('cleaned.csv')

    # connect to Database Postgres
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        # load by chunk
        for table in pd.read_csv('cleaned.csv', chunksize=chunksize):
            start = time()
            table.to_sql(table_name, con=engine, if_exists='append')
            end = time()
            print(f'successfully pushing {len(table)} data into database... take {round(end - start, 2)} second')

    os.remove('cleaned.csv')
    print('Remove file successfully')

@task(log_prints=True)
def push_hdfs(params, df: pd.DataFrame) -> None:
    '''pusing file into HDFS container'''

    table_name = params.table_name
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

    # Writing file into HDFS
    try:
        print(f'HDFS: Start writing table {table_name} into {dir}')
        with hdfs.open(f"{dir}{table_name}.csv", "wb") as file:
            df.to_csv(file, chunksize=100000)
        print('Done writing {table_name}.csv into {dir}')
    except Exception as e:
        print(f"Error: {e}")


@flow(name="Ingest flow")
def main():
    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    parser = arg.ArgumentParser(description="Ingest Parquet to Postgres")
    parser.add_argument('--table_name', help='name of the table where is written result to',default="yellow_taxi_data")
    args = parser.parse_args()

    raw_data = extract_data(URL)
    data = transform_data(raw_data)
    # ingest_data(args, data)
    push_hdfs(args, data)

if __name__ == "__main__":
    main()

