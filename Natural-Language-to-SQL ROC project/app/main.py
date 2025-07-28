# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chain import agent_executor

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        print("Received query:", request.query)
        print("Invoking agent_executor...")
        response = agent_executor.invoke({"input": request.query})
        print("Response from agent:", response)
        return response
    except Exception as e:
        print("Error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
