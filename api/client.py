import requests
import streamlit as st

def get_capital_response(country):
    url = "http://localhost:8001/capital/invoke"
    payload = {"input": {"country": country}}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['output']
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None
    

def get_description_response(country):
    url = "http://localhost:8001/description/invoke"
    payload = {"input": {"country": country}}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['output']
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None

#streamlit app
st.title("Langchain API Client")
input_country = st.text_input("Enter a country name:")
input_topic = st.text_input("Enter a topic:")

if input_country:
    capital = get_capital_response(input_country)
    if capital:
        st.write("✅ Capital:", capital)
    
if input_topic:
    description = get_description_response(input_topic)
    if description:
        st.write("✅ Description:", description)