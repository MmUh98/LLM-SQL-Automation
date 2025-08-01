# app/chain.py

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langgraph.graph import StateGraph
from app.db import get_database
from typing import TypedDict, Optional

load_dotenv()

class StateSchema(TypedDict, total=False):
    input: str
    sql: str
    result: Optional[str]

def get_langgraph_agent():
    print("Setting up LangGraph agent...")

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
        model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
        temperature=0,
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    db = SQLDatabase(get_database())

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that translates natural language to SQL queries."),
        ("user", "Translate the following question into SQL for the AdventureWorks2022 database: {input}")
    ])

    translate_chain = prompt | llm

    def translate(state):
        print("[LangGraph] Entering translate node with state:", state)
        result = translate_chain.invoke({"input": state["input"]})
        print("[LangGraph] LLM returned SQL:", result.content)
        return {"sql": result.content, "input": state["input"]}

    def query_database(state):
        print("[LangGraph] Entering query_database node with state:", state)
        try:
            result = db.run(state["sql"])
            print("[LangGraph] DB returned result:", result)
        except Exception as e:
            result = f"Error executing query: {str(e)}"
            print("[LangGraph] Exception during DB query:", e)
        return {"result": result, "input": state["input"], "sql": state["sql"]}

    builder = StateGraph(StateSchema)

    builder.add_node("Translate", translate)
    builder.add_node("QueryDB", query_database)

    builder.set_entry_point("Translate")
    builder.add_edge("Translate", "QueryDB")
    builder.set_finish_point("QueryDB")

    graph = builder.compile()

    print("LangGraph agent setup complete.")
    return graph
