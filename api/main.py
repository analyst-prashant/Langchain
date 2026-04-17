from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables before configuring LangChain providers.
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Create the FastAPI application that exposes the LangChain routes.
app = FastAPI(
    title="Langchain API",
    description="API for Langchain with OpenAI and Ollama",
    version="1.0.0",
)

# OpenAI model used for the capital lookup endpoint.
openai_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000, verbose=True)
# Local Ollama model used for the description endpoint.
ollama_model = Ollama(model="llama2", temperature=0.7, num_predict=1000, verbose=True)

# Prompt template for returning a country's capital.
prompt1 = ChatPromptTemplate.from_template("What is the capital of {country}?")
# Prompt template for generating a short country description.
prompt2 = ChatPromptTemplate.from_template("Write a short description of {country}?")

# Expose an endpoint that answers capital-city questions through OpenAI.
add_routes(
    app,
    prompt1 | openai_model | StrOutputParser(),
    path="/capital",
)

# Expose an endpoint that returns a country description through Ollama.
add_routes(
    app,
    prompt2 | ollama_model | StrOutputParser(),
    path="/description",
)

# Optional: Add Ollama route if needed
# add_routes(
#     app,
#     prompt1 | ollama_model | StrOutputParser(),
#     path="/ollama/capital",
# )

if __name__ == "__main__":
    # Start the local development server on port 8001.
    uvicorn.run(app, host="localhost", port=8001)