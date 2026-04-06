from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is missing. Set it in a .env file or environment variables.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

###Prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that helps users find information about the user queries."),
        ("human", "Question:{question}")
    ]
)

###Streamlit app

st.title("Langchain OpenAI Chatbot")
input_question = st.text_input("Enter your question here:")

###OpenAI Chatbot
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000, verbose=True)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_question:
    response = chain.invoke({"question": input_question})
    st.write("✅ Answer:", response)
