# app/chain.py

import os

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup LLM with Azure
print("Loading AzureChatOpenAI...")
llm = AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
    temperature=0,
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
print("AzureChatOpenAI loaded.")

# Setup Database
print("Building DB URI...")
# You can use your .env or hardcode the connection string as needed
# Example for trusted connection:
# Build the connection string from .env

db_uri = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
print("DB URI:", db_uri)

print("Creating SQLDatabase object...")
db = SQLDatabase.from_uri(db_uri)
print("SQLDatabase object created.")

# Create Agent
print("Creating SQL agent...")
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",  # or "openai-functions"
    verbose=True
)
print("SQL agent created.")
