import pprint

# Import the necessary libraries
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Import functions from ebay_scraper.py and kleinanzeigen_scraper.py
from ebay_scraper import scrape_ebay_prices
from kleinanzeigen_scraper import scrape_kleinanzeigen_prices
from scrape_results_helpers import sort_results_by_price, format_results_as_table

# Load environment variables from .env file
load_dotenv()

# Initialize the ChatOpenAI model with the specified model name.
model = ChatOpenAI(model="gpt-4o-mini")

# Define the item name
#item_name = "Lego Ritterburg 6080"
item_name = "Bosch Rotak 43 Li"
#item_name = "Bosch AHS 55-24 Li"
#item_name = "Bosch AHS 70-34"
#item_name = "Bosch VeroAroma 300"
#item_name = "Lenovo ThinkPad T15"

#  Scrape prices from eBay and Kleinanzeigen
ebay_prices = format_results_as_table(sort_results_by_price(scrape_ebay_prices(item_name)))
kleinanzeigen_prices = format_results_as_table(sort_results_by_price(scrape_kleinanzeigen_prices(item_name)))

# Print the prices from eBay and Kleinanzeigen
# print(f"eBay prices: {ebay_prices}")
# print(f"Kleinanzeigen prices: {kleinanzeigen_prices}")

# Define the system and user templates
system_template = """Sie sind ein Forscher, der die Preise von Artikeln auf eBay und Kleinanzeigen analysiert. 
                  Sie haben zwei Funktionen, die die Preise von Artikeln von eBay und Kleinanzeigen scrapen.
                  Sie geben Empfehlungen an Benutzer basierend auf den Preisen der Artikel."""

user_template = """
                Analysieren Sie die folgenden Preise von Artikeln auf eBay und Kleinanzeigen:
                
                Preise für {item_name} auf eBay: 
                {ebay_prices}

                Preise für {item_name} auf Kleinanzeigen: 
                {kleinanzeigen_prices}

                Fokussiere nur auf vollständige Artikel, nicht auf Ersatzteile oder einzelne Bestandteile.

                Was ist Ihre empfohlene Preisspanne für {item_name}?"""

prompt_template = ChatPromptTemplate([
    ("system", system_template),
    ("user", user_template)
])

prompt = prompt_template.invoke({
    "item_name": item_name,
    "ebay_prices": ebay_prices,
    "kleinanzeigen_prices": kleinanzeigen_prices
})

result = prompt.to_messages()

response = model.invoke(prompt)

# Pretty-print the response content
pprint.pprint(response.content)


# SystemMessage: 
# You are a researcher who is analyzing the prices of items on eBay and Kleinanzeigen.
# You have two functions that scrape the prices of items from eBay and Kleinanzeigen.
# You provide recommendations to users based on the prices of items.

# HumanMessage: 
# Analyze the following prices of items on eBay and Kleinanzeigen:
# What is the price range for the provided item?
# What is the average price for the provided item?
# Which platform has the best deals for the provided item?
# Provide recommendations based on the prices of items on eBay and Kleinanzeigen
