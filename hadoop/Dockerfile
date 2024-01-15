FROM apache/hadoop:3

# COPY ./namenode-format.sh /opt/

# ENTRYPOINT sh /opt/namenode-format.sh

RUN hdfs namenode -format

EXPOSE 8020 9870