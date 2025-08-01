from sqlalchemy import create_engine, text

# Replace with your actual credentials
driver = "ODBC Driver 17 for SQL Server"
server = "DESKTOP-S0U7FNV"  # or your Azure SQL Server name
database = "AdventureWorks2022"
username = "read_only"
password = "thisissecureway"

connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver.replace(' ', '+')}"

engine = create_engine(connection_string)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Person.Person"))  # Change to any known table
        for row in result:
            print(row)
        print("✅ Query succeeded.")
except Exception as e:
    print("❌ Query failed.")
    print(e)
