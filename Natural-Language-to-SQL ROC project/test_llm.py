from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
    temperature=0,
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

print(llm.invoke("Hello!"))

