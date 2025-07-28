import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

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
    response = llm.invoke("Hello, who are you?")
    print("LLM response:", response)
except Exception as e:
    print("LLM connection failed:", e)

