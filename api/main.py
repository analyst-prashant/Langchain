from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

app = FastAPI(
    title="Langchain API",
    description="API for Langchain with OpenAI and Ollama",
    version="1.0.0",
)

# Define models
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000, verbose=True)
llm = Ollama(model="llama2", temperature=0.7, num_predict=1000, verbose=True)

# Define prompts
prompt1 = ChatPromptTemplate.from_template("What is the capital of {country}?")
prompt2 = ChatPromptTemplate.from_template("Write a short description of {country}?")

# Add routes for OpenAI chains
add_routes(
    app,
    prompt1 | model | StrOutputParser(),
    path="/capital",
)

add_routes(
    app,
    prompt2 | llm | StrOutputParser(),
    path="/description",
)

# Optional: Add Ollama route if needed
# add_routes(
#     app,
#     prompt1 | llm | StrOutputParser(),
#     path="/ollama/capital",
# )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)