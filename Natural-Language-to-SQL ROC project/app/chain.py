# app/chain.py

import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from app.db import get_database

load_dotenv()

print("Loading AzureChatOpenAI...")
llm = AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
    temperature=0,
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
print("AzureChatOpenAI loaded.")

print("Getting SQLAlchemy engine from db.py...")
db_engine = get_database()
print("Building SQLDatabase object...")
db_uri = str(db_engine.url) if hasattr(db_engine, 'url') else db_engine
# Use SQLDatabase.from_uri to ensure all schemas are introspected
# (include_tables=None means all tables the user can see)
db = SQLDatabase.from_uri(
    db_uri,
    include_tables=None,
    sample_rows_in_table_info=3
)
print("SQLDatabase object created.")

# Add toolkit to allow LLM access to DB schema
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

print("Creating SQL agent...")
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,  # Use the toolkit for schema/tools context
    verbose=True
)
print("SQL agent created.")

# Print tables for debugging
tables = db.get_usable_table_names()
print("Tables in DB:", tables)
