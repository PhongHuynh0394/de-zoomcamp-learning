import pandas as pd
from hdfs3 import HDFileSystem

namenode_host='localhost'
port=8020
df = pd.DataFrame([
    {'year': 1994, 'first_name': 'Vova'},
    {'year': 1995, 'first_name': 'Anja'},
    {'year': 1996, 'first_name': 'Vasja'},
    {'year': 1997, 'first_name': 'Petja'},
    {'year': 2000, 'first_name': 'Petja'},
    {'year': 2131, 'first_name': 'Petja'},
])


# # conn.execute("insert into testdb.newtable values",df,settings=dict(use_numpy=True))

# Connect with HaDoop File System
try:
    print('Connecting to HDFS...')
    hdfs = HDFileSystem(namenode_host, port)
    print('Done...')
except Exception as e:
    print(e)

hdfs.put("requirements.txt", "/requirements.txt")
