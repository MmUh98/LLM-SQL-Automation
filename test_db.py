import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

conn_str = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}"
)

print(f"Connecting with: {conn_str}")

try:
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT TOP 1 * FROM INFORMATION_SCHEMA.TABLES"))
        row = result.fetchone()
        print("Connection successful! Example row:", row)
except Exception as e:
    print("Connection failed:", e)

