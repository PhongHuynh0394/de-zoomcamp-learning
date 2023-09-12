import hdfs3
import pandas as pd

host='localhost'
port=8020
print('connect')
hdfs = hdfs3.HDFileSystem(host, port)
print('successfully connect')

hdfs_path = '/phong_huynh/abc.txt'
local_path = './b.txt'
# hdfs.mkdir('/phong_huynh/')
# hdfs.put(local_path, hdfs_path)
print(hdfs.ls('/'))
with hdfs.open(hdfs_path) as file:
    data = file.read()
print(data)

print('get file')

hdfs.get(hdfs_path, 'hdfs.txt')
# choice = input('upload ? y/n:')
# if choice == 'y':
#     try:
#         if not hdfs.exists('/user/phong_huynh'):
#             hdfs.mkdir('/user/phong_huynh/')
#             print(f'Create new dir {hdfs_path}')

#         hdfs.put(local_path, hdfs_path)
#         print(f'upload {local_path} successfully')
#     except Exception as e:
#         print(e)

# if hdfs.isfile(hdfs_path):
#     print(f'{hdfs_path} already exists')
#     print('print the content of file')
#     try:
#         with hdfs.open(hdfs_path) as file:
#             content = file.read(1000)
#         print(content)
#         print(len(content))

#         print('----finish printing----')
#     except Exception as e:
#         print(e)

# with open('b.txt', 'r') as file:
#     content = file.read()
# print(content)
