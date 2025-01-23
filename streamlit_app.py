# Import the necessary libraries
#from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Import functions from ebay_scraper.py and kleinanzeigen_scraper.py
from ebay_scraper import scrape_ebay_prices
from kleinanzeigen_scraper import scrape_kleinanzeigen_prices
from scrape_results_helpers import sort_results_by_price, format_results_as_table


# Sidebar
st.sidebar.header("Einstellungen")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password", help="Geben Sie Ihren OpenAI API-Schlüssel ein.")
    "[OpenAI API Key erhalten](https://platform.openai.com/account/api-keys)"

# Submit button for API key
if st.sidebar.button("API Key speichern"):
    if not openai_api_key:
        st.sidebar.error("Bitte gib deinen OpenAI API-Schlüssel ein.")
    else:
        st.sidebar.success("API Key gespeichert.")

st.title("Preisanalyse Assistent für eBay und Kleinanzeigen")
st.write("Dieser Assistent unterstützt dich bei der Preisanalyse von Artikeln auf eBay und Kleinanzeigen.")

if not openai_api_key:
    st.info("Bitte gib deinen OpenAI API Key ein um fortzusetzen.")
    st.stop()

st.write("Bitte gib den Namen des Artikels ein.")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Initialize LangChain components
llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=openai_api_key)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# User input form
with st.form(key='user_input_form'):
    user_input = st.text_input("**Artikel**: ", "")
    item_name = user_input
    submit_button = st.form_submit_button(label='Senden')

if submit_button and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})

    # Scrape prices from eBay and Kleinanzeigen
    with st.spinner('Suche bei eBay nach passenden Artikeln...'):
        ebay_prices = format_results_as_table(sort_results_by_price(scrape_ebay_prices(item_name)))
    
    with st.spinner('Suche bei Kleinanzeigen nach passenden Artikeln...'):
        kleinanzeigen_prices = format_results_as_table(sort_results_by_price(scrape_kleinanzeigen_prices(item_name)))    
    
    # Define the role and the question template
    role = """
    Sie sind ein Forscher, der die Preise von Artikeln auf eBay und Kleinanzeigen analysiert. 
    Ihre Aufgaben umfassen:

    1. Scrapen der Preise von Artikeln auf eBay und Kleinanzeigen.
    2. Analysieren der gescrapten Preise.
    3. Geben von Empfehlungen an Benutzer basierend auf den analysierten Preisen.

    Fokussieren Sie sich auf vollständige Artikel und nicht auf Ersatzteile oder einzelne Bestandteile.
    """
    
    question_template = f"""
    Analysieren Sie die folgenden Preise von Artikeln auf eBay und Kleinanzeigen:
    
    Preise für {item_name} auf eBay: 
    {ebay_prices}

    Preise für {item_name} auf Kleinanzeigen: 
    {kleinanzeigen_prices}
    
    Fokussieren Sie sich nur auf vollständige Artikel, nicht auf Ersatzteile oder einzelne Bestandteile.

    Was ist Ihre empfohlene Preisspanne für {item_name}?

    Stelle 5 Links zu den passendsten Artikeln auf eBay und Kleinanzeigen bereit.
    """
    
    # Create a list of messages
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": question_template}
    ]
    
    # Process the messages with the conversation object

    with st.spinner('Generiere Antwort...'):
        try:
            # Process the messages with the conversation object
            response = conversation.predict(input=messages)
            st.session_state['messages'].append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error generating response: {e}")    

# Display chat history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**Du**: {message['content']}")
    else:
        st.write(f"**Assistent**: {message['content']}")