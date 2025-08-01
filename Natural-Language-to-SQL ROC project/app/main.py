# app/main.py

from fastapi import FastAPI, HTTPException
from app.schemas import QueryRequest
from app.chain import get_langgraph_agent
import traceback
from fastapi.concurrency import run_in_threadpool

print("[FastAPI] main.py module loaded.")

app = FastAPI()


# Initialize the agent once at startup
print("Initializing LangGraph agent at startup...")
agent = get_langgraph_agent()
print("LangGraph agent is ready.")


@app.post("/ask")
async def ask_question(request: QueryRequest):
    print("[FastAPI] ask_question endpoint called.")
    try:
        print("[FastAPI] Received query:", request.query)
        print("[FastAPI] Invoking agent...")
        state = await run_in_threadpool(agent.invoke, {"input": request.query})
        print("[FastAPI] Agent returned state:", state)
        return {
            "query": request.query,
            "sql": state.get("sql"),
            "result": state.get("result")
        }
    except Exception as e:
        print("[FastAPI] Exception:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
def root():
    print("[FastAPI] Root endpoint called.")
    return {"message": "FastAPI is running"}
