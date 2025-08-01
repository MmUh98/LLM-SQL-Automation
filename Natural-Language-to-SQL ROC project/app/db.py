# app/db.py

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_database():
    print("DB_USER:", os.getenv("DB_USER"))
    print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
    print("DB_SERVER:", os.getenv("DB_SERVER"))
    print("DB_NAME:", os.getenv("DB_NAME"))
    print("DB_DRIVER:", os.getenv("DB_DRIVER"))

    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Properly encode the driver for the connection string
    driver_enc = DB_DRIVER.replace(' ', '+')
    conn_str = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={driver_enc}"
    return create_engine(conn_str)
