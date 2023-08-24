# Week 2 Prefect

## Prefect
Prefect is a modern workflow management tool designed to orchestrate data stacks by building, running, and monitoring data pipelines. 
It is an open-source tool powered by the Prefect Core workflow engine and serves modern project management.

### Install
Just run `pip install prefect` or you can use `pip install -r requirements.txt`

To ensure everything ok, run `prefect version` after finish installing

### Using
To use, just run python file in virtual environment which have prefect installed. There are prefect decorator to declare
prefect stuff such as `@task` or `@flow` 

Check UI: `prefect orion start`

Some config for db2, postgres and pgadmin (same as week 1)
```env
# DB2
LICENSE=accept
DB2INSTANCE=db2inst1
DB2INST1_PASSWORD=rootadmin
DBNAME=testdb
BLU=false
ENABLE_ORACLE_COMPATIBILITY=false
UPDATEAVAIL=NO
TO_CREATE_SAMPLEDB=false
REPODB=false
IS_OSXFS=false
PERSISTENT_HOME=false
HADR_ENABLED=false
ETCD_ENDPOINT=
ETCD_USERNAME=
ETCD_PASSWORD=

# POSTGRES
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_DB=ny_taxi 

# PGADMIN
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=root
```

### Prefect block
More detail: [Prefect Blocks](https://docs.prefect.io/2.11.4/concepts/blocks/)

Just like I/O Manager, you can use prefect block to connect with third-party technology easily.

In `data_ingestion.py`, i use SqlAlchemyConnector Prefect block to connect with Postgres instead of using
sqlalchemy package itself.

To see block, go to Block at Prefect UI (running above)
