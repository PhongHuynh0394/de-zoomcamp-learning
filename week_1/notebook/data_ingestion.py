import pandas as pd
from time import time
import pyarrow.parquet as pq
import os
from sqlalchemy import create_engine
import argparse as arg

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    del_file = params.delete_file
    chunksize = 100_000

    parquet_file = 'output.parquet'

    if del_file == None:
        del_file=input('Delete download file or not [Y/n]:')

    #dowload parquet
    try:
        print('Start Downloading...')
        os.system(f"wget {url} -O {parquet_file}")
        print('Download successfully')
    except Exception as e:
        print(e)
    file = pq.ParquetFile(parquet_file)

    # connect to Database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    for table in file.iter_batches(batch_size=chunksize):
        start = time()
        df = table.to_pandas()
        df.to_sql(table_name, con=engine, if_exists='append')
        end = time()
        print(f'successfully pushing {len(df)} data into database... take {round(end - start, 2)} second')

    if del_file in ['yes', 'Y', 'y', 'Yes', 'YES']:
        os.remove('output.parquet')
        print('Remove file successfully')


if __name__ == "__main__":

    parser = arg.ArgumentParser(description="Ingest Parquet to Postgres")

    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

    parser.add_argument('--user', help='user name for postgres',default="root")
    parser.add_argument('--password', help='password name for postgres',default="root")
    parser.add_argument('--host', help='host name for postgres',default="postgres")
    parser.add_argument('--port', help='port name for postgres',default="5432")
    parser.add_argument('--db', help='database name for postgres',default="ny_taxi")
    parser.add_argument('--table_name', help='name of the table where is written result to',default="yellow_taxi_data")
    parser.add_argument('--url', help='url of parquet file',default=URL)
    parser.add_argument('--delete_file', help='Delete Download file',default=None)

    args = parser.parse_args()

    main(args)
