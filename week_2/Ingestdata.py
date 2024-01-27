from sqlalchemy import create_engine
from time import time

engine = create_engine('postgresql://root:root@postgres:5432/ny_taxi') #need to chang localhost to postgres cause in docker network
engine.connect()

green_taxi_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
chunk_size = 100_000
df = pd.read_csv(green_taxi_url, dtype={'store_and_fwd_flag': "string"}, chunksize=chunk_size)

for i, chunk in enumerate(df):
    # Some simple cleaning
    chunk.lpep_pickup_datetime = pd.to_datetime(chunk.lpep_pickup_datetime)
    chunk.lpep_dropoff_datetime = pd.to_datetime(chunk.lpep_dropoff_datetime)

    # Push into psql
    try:
        start = time()
        chunk.to_sql(name='green_taxi_data', con=engine, if_exists='append')
        end = time()
        print(f"Chunk {i+1}: Successfully Ingesting {len(chunk)} into PSQL... take {round(end-start,2)} Sec")
    except Exception as e:
        print(e)
        print(f"Failed at chunk {i}, skip...")

zone_url = "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
df = pd.read_csv(zone_url, chunksize=chunk_size)
table = "zone"
for i, chunk in enumerate(df):
    # Push into psql
    try:
        start = time()
        chunk.to_sql(name=table, con=engine, if_exists='append')
        end = time()
        print(f"Chunk {i+1}: Successfully Ingesting {len(chunk)} into PSQL... take {round(end-start,2)} Sec")
    except Exception as e:
        print(e)
        print(f"Failed at chunk {i}, skip...")
