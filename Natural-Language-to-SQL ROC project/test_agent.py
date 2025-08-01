# test_agent.py
from app.chain import get_agent_executor

agent = get_agent_executor()
response = agent.invoke({"input": "List first 5 employee names from HumanResources.Employee"})
print(response)
