# Import the necessary libraries
from dotenv import load_dotenv

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Import functions from ebay_scraper.py and kleinanzeigen_scraper.py
from ebay_scraper import scrape_ebay_prices
from kleinanzeigen_scraper import scrape_kleinanzeigen_prices
from scrape_results_helpers import sort_results_by_price, format_results_as_table

# Load environment variables from .env file
load_dotenv()

# Custom CSS to change font size
custom_css = """
<style>
body {
    font-size: 26px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Preisanalyse Assistent für eBay und Kleinanzeigen")
st.write("Dieser Assistent unterstützt Sie bei der Preisanalyse von Artikeln auf eBay und Kleinanzeigen.")

st.write("Bitte geben Sie den Namen des Artikels ein, dessen Preise Sie analysieren möchten.")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Initialize LangChain components
llm = ChatOpenAI(model_name="gpt-4o-mini")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# User input
user_input = st.text_input("**Du**: ", "")

item_name = user_input

#  Scrape prices from eBay and Kleinanzeigen
ebay_prices = format_results_as_table(sort_results_by_price(scrape_ebay_prices(item_name)))
kleinanzeigen_prices = format_results_as_table(sort_results_by_price(scrape_kleinanzeigen_prices(item_name)))

#if user_input:
#    st.session_state['messages'].append({"role": "user", "content": user_input})
#    response = conversation.predict(input=user_input)
#    st.session_state['messages'].append({"role": "assistant", "content": response})

if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Define the role and the question template
    role = """
    Sie sind ein Forscher, der die Preise von Artikeln auf eBay und Kleinanzeigen analysiert. 
    Sie haben zwei Funktionen, die die Preise von Artikeln von eBay und Kleinanzeigen scrapen.
    Sie geben Empfehlungen an Benutzer basierend auf den Preisen der Artikel.
    """
    
    question_template = f"""
    Analysieren Sie die folgenden Preise von Artikeln auf eBay und Kleinanzeigen:
    
    Preise für {item_name} auf eBay: 
    {ebay_prices}

    Preise für {item_name} auf Kleinanzeigen: 
    {kleinanzeigen_prices}

    Fokussiere nur auf vollständige Artikel, nicht auf Ersatzteile oder einzelne Bestandteile.

    Was ist Ihre empfohlene Preisspanne für {item_name}?

    Stelle 5 Links zu den passendsten Artikeln auf eBay und Kleinanzeigen bereit.
    """
    
    # Create a list of messages
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": question_template}
    ]
    
    # Process the messages with the conversation object
    response = conversation.predict(input=messages)
    st.session_state['messages'].append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**Du**: {message['content']}")
    else:
        st.write(f"**Assistent**: {message['content']}")