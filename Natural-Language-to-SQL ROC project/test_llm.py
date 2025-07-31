import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from app.db import get_database

load_dotenv()

print("Testing AzureChatOpenAI connection...")

llm = AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
    temperature=0,
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

try:
    print("Testing DB connection...")
    db_engine = get_database()
    db = SQLDatabase.from_uri(str(db_engine.url))
    print("Tables in DB:", db.get_usable_table_names())
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    print("LLM and DB connection successful!")
    # Optionally, test a simple query
    result = agent_executor.invoke({"input": "List all tables in the database"})
    print("Agent output:", result)
except Exception as e:
    print("LLM or DB connection failed:", e)
