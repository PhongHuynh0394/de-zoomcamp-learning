import pandas as pd
from pathlib import Path
from hdfs3 import HDFileSystem
from time import time
from datetime import timedelta
# import pyarrow.parquet as pq
import os
from sqlalchemy import create_engine
import argparse as arg
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector

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
def ingest_data_psql(params, df: pd.DataFrame):
    table_name = params.table_name
    chunksize = 100_000
    df.to_csv('raw_data.csv')

    # connect to Database Postgres
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        # load by chunk
        for table in pd.read_csv('raw_data.csv', chunksize=chunksize):
            start = time()
            table.to_sql(table_name, con=engine, if_exists='append')
            end = time()
            print(f'successfully pushing {len(table)} data into database... take {round(end - start, 2)} second')

    os.remove('raw_data.csv')
    print('Remove file successfully')


@task(log_prints=True)
def extract_psql(params) -> pd.DataFrame:
    '''Extract data from psql to push to hdfs'''
    table_name = params.table_name
    query = f"SELECT * FROM {table_name}"

    # connect to Database Postgres
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        df = pd.read_sql_query(query, engine)

    return df

@task(log_prints=True)
def write_hdfs(params, df: pd.DataFrame) -> None:
    '''write file into HDFS container'''

    namenode_host='localhost'
    port=8020
    table_name = params.table_name

    # Connect with HaDoop File System
    print('Connecting to HDFS...')
    hdfs = HDFileSystem(namenode_host, port)
    print('Done...')

    #Create dir
    dir = '/raw_data/'
    if not hdfs.exists(dir):
        print(f"Directory {dir} doesn't exists! Create {dir}")
        hdfs.mkdir(dir)
        print('Done...')

    # Pusing file into HDFS
    try:
        print(f'HDFS: Start pusing file')
        with hdfs.open(f"{dir}{table_name}.parquet", "wb") as file:
            df.to_parquet(file)
        print(f'HDFS: Done writing {table_name}.parquet into {dir}')
    except Exception as e:
        print(f"Error: {e}")


@flow(name="Ingest flow")
def main():
    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    parser = arg.ArgumentParser(description="Ingest Parquet to Postgres")
    parser.add_argument('--table_name', help='name of the table where is written result to',default="yellow_taxi_data")
    args = parser.parse_args()

    # data = transform_data(raw_data)
    data_extracted = extract_data(URL)
    ingest_data_psql(args, data_extracted)
    raw_data = extract_psql(args)
    write_hdfs(args, raw_data)

if __name__ == "__main__":
    main()

