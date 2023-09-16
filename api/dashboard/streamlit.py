import streamlit as st
import requests
import json



st.title("Welcome to the VisualAI Demo")

input = st.text_input("Enter the FastAPI response:")

if st.button("Run"):
    requests.get("http://127.0.0.1:8000/visualai", input)
    
