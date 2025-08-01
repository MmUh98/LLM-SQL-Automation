from sqlalchemy import inspect
from app.db import get_database
import os

print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_SERVER:", os.getenv("DB_SERVER"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_DRIVER:", os.getenv("DB_DRIVER"))

engine = get_database()
inspector = inspect(engine)

for schema in inspector.get_schema_names():
    print(f"Schema: {schema}")
    for table in inspector.get_table_names(schema=schema):
        print(f"  - {table}")
