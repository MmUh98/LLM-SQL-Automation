# app/db.py

import os
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv



load_dotenv()

def get_database():
    params = urllib.parse.quote_plus(
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
