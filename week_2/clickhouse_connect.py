from clickhouse_driver import Client
import pandas as pd
import clickhouse_driver as ch
from sqlalchemy import create_engine

import clickhouse_connect

# client = clickhouse_connect.get_client(host='k4qih6l05v.asia-southeast1.gcp.clickhouse.cloud', port=8443, username='default', password='tWlN69j7B.qdB')
# client = Client('localhost')
# # print(conn.execute('show databases'))
# print(client.execute('show databases'))
hostlocal = 'localhost'
hostcloud = "k4qih6l05v.asia-southeast1.gcp.clickhouse.cloud"
passcloud="tWlN69j7B.qdB" 
db="default"
username='default'
port=8123
uri=f"clickhouse+native://{hostlocal}/{db}"

engine = create_engine(uri)
# engine = create_engine(f"clickhouse://{username}:{passcloud}@{hostlocal}:{port}/{db}")
engine.connect()



df = pd.DataFrame([
    {'year': 1994, 'first_name': 'Vova'},
    {'year': 1995, 'first_name': 'Anja'},
    {'year': 1996, 'first_name': 'Vasja'},
    {'year': 1997, 'first_name': 'Petja'},
])

df.to_sql('test_table', engine, if_exists='append')

# query = 'insert into "test_table" values'
# client.insert_dataframe(query, df)
# client.execute('select * from test_table')
# host='k4qih6l05v.asia-southeast1.gcp.clickhouse.cloud'
# port=8443
# user='default'
# password='tWlN69j7B.qdB'
# # print(help(Client))
# # ch.connection.Connection(host=host, port=port, user=user, password=password)

# client = Client(host, port, user, password)
# client.execute('show tables')
