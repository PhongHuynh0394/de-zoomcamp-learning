import pandas as pd
from clickhouse_driver import Client
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
def write_hdfs(df: pd.DataFrame, table_name: str, layer: str) -> None:
    '''write file into HDFS container'''

    namenode_host='localhost'
    port=8020
    # table_name = params.table_name

    # Connect with HaDoop File System
    print('Connecting to HDFS...')
    hdfs = HDFileSystem(namenode_host, port)
    print('Done...')

    #Create dir
    dir = f'/{layer}/'
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


@task(log_prints=True)
def extract_hdfs(table_name: str, layer: str) -> pd.DataFrame:
    '''Extract data from HDFS layer'''
    namenode_host='localhost'
    port=8020
    # table_name = params.table_name

    # Connect with HaDoop File System
    print('Connecting to HDFS...')
    hdfs = HDFileSystem(namenode_host, port)
    print('Done...')

    destination = f"/{layer}/{table_name}.parquet"
    if not hdfs.exists(destination):
        print("File doesn't exists")
        return None
    try:
        print(f'Get data from {destination}')
        with open(f"{destination}", "rb") as data:
            df = pd.read_parquet(data)
        print('Done')
        return df
    except Exception as e:
        print(e)

@task(log_prints=True)
def hdfs_to_ch(df: pd.DataFrame) -> None:
    '''full load data from HDFS into Clickhouse warehouse'''
    host = 'localhost'
    client = Client(host)

    # Create table
    try:
        print("create table ny_taxi_data")
        client.execute("""
        CREATE TABLE IF NOT EXISTS yellow_taxi_data (
        "VendorID" BIGINT, 
        tpep_pickup_datetime TIMESTAMP, 
        tpep_dropoff_datetime TIMESTAMP, 
        passenger_count FLOAT(53), 
        trip_distance FLOAT(53), 
        "RatecodeID" FLOAT(53), 
        store_and_fwd_flag TEXT, 
        "PULocationID" BIGINT, 
        "DOLocationID" BIGINT, 
        payment_type BIGINT, 
        fare_amount FLOAT(53), 
        extra FLOAT(53), 
        mta_tax FLOAT(53), 
        tip_amount FLOAT(53), 
        tolls_amount FLOAT(53), 
        improvement_surcharge FLOAT(53), 
        total_amount FLOAT(53), 
        congestion_surcharge FLOAT(53), 
        airport_fee FLOAT(53)
    ) ENGINE = Memory
    """)
        print('Done...')
    except Exception as e:
        print(e)


    try:
        print('pusing data into clickhouse')
        rows = client.insert_dataframe("insert into yellow_taxi_data values",df, settings=dict(use_numpy=True))
        print(f'Done... pushing {rows} data into clickhouse')
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
    # raw_data = extract_psql(args)
    write_hdfs(data_extracted, "test", "raw_data")
    data_hdfs = extract_hdfs("test", "raw_data")
    ingest_data_psql(args, data_hdfs)

if __name__ == "__main__":
    main()

