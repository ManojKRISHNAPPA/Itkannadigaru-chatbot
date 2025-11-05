import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
import os

st.title('ITKannadigaru ChatBot')

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'Hey you are an AI guy, give proper answers'),
        ('user', 'Question: {question}')
    ]
)

st.sidebar.title('Settings')
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
tokens = st.sidebar.slider("Max Token", 50, 500, 100)
engine = st.sidebar.selectbox("Select engine", ["gpt-5",'gpt-5-mini',"gpt-4o-mini", "gpt-4-turbo"])

def generate_response(question, api_key, temperature, tokens, engine):
    
    chat_model = ChatOpenAI(
        api_key=api_key,  
        model=engine,
        temperature=temperature,
        max_tokens=tokens
    )

    parser = StrOutputParser()
    chain = prompt | chat_model | parser
    response = chain.invoke({"question": question})
    return response

st.write("Enter your question")
user_input = st.text_input("Ask anything you want:")

if user_input and api_key:
    try:
        answer = generate_response(user_input, api_key, temperature, tokens, engine)
        st.write(answer)
    except Exception as e:
        st.error(f"Error: {e}")
elif user_input:
    st.warning("Please enter your API key")
else:
    st.write('Please provide user input')
