# Import the necessary libraries
from dotenv import load_dotenv

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

st.title("Chatbot with Streamlit and LangChain")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Initialize LangChain components
llm = ChatOpenAI(model_name="gpt-4o-mini")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# User input
user_input = st.text_input("You: ", "")

if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    response = conversation.predict(input=user_input)
    st.session_state['messages'].append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Assistant: {message['content']}")