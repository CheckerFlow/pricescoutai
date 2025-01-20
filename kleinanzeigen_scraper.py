import re
from bs4 import BeautifulSoup
import requests

# Import functions from scrape_results_helpers.py
from scrape_results_helpers import format_results_as_table, sort_results_by_price

def scrape_kleinanzeigen_prices(item_name):
    url = f"https://www.kleinanzeigen.de/s-suchanfrage.html?keywords={item_name}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.select(".aditem")
    results = []
    for item in items:
        title = item.select_one(".ellipsis").text.strip() if item.select_one(".ellipsis") else "No title found"
        price = item.select_one(".aditem-main--middle--price-shipping--price").text.strip() if item.select_one(".aditem-main--middle--price-shipping--price") else "No price found"
        item_url_element = item.select_one(".ellipsis")
        item_url = item_url_element["href"] if item_url_element and "href" in item_url_element.attrs else "No URL found"
        results.append({"title": title, "price": price, "url": f"https://www.kleinanzeigen.de{item_url}" if item_url != "No URL found" else item_url})
    return results if results else "No items found."

# Usage
#results = scrape_kleinanzeigen_prices("Lego Ritterburg 6080")
#sorted_results = sort_results_by_price(results)
#format_results_as_table(sorted_results)