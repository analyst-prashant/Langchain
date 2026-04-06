from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
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

st.title("Langchain Ollama Chatbot")
input_question = st.text_input("Enter your question here:")

###Ollama Chatbot
llm = Ollama(model="llama2", temperature=0.7, num_predict=1000, verbose=True)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_question:
    response = chain.invoke({"question": input_question})
    st.write("✅ Answer:", response)