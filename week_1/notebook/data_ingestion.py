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
    chunksize = 100_000

    parquet_file = 'output.parquet'

    #dowload parquet
    os.system(f"wget {url} -O {parquet_file}")

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

if __name__ == "__main__":

    parser = arg.ArgumentParser(description="Ingest Parquet to Postgres")

    # User, password, localhost, port, database
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password name for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port name for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where is written result to')
    parser.add_argument('--url', help='url of parquet file')

    args = parser.parse_args()

    main(args)