
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
#2.-Turn on database engine
dbEngine=create_engine('postgresql://postgres:dhaval@127.0.0.1:5432/shacklabs', pool_size=100, max_overflow=120) 

# meta = MetaData(bind=dbEngine)

from sqlalchemy import inspect
inspector = inspect(dbEngine)
schemas = inspector.get_schema_names()

for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print(table_name)

