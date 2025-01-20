from bs4 import BeautifulSoup
import requests

# Import functions from scrape_results_helpers.py
from scrape_results_helpers import  format_results_as_table, sort_results_by_price

def scrape_ebay_prices(item_name):
    url = f"https://www.ebay.de/sch/i.html?_nkw={item_name}&LH_Complete=1&LH_Sold=1&_ipg=240"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.select(".s-item")
    results = []
    for item in items:
        title = item.select_one(".s-item__title").text if item.select_one(".s-item__title") else "No title found"
        price = item.select_one(".s-item__price").text if item.select_one(".s-item__price") else "No price found"
        item_url = item.select_one(".s-item__link")["href"] if item.select_one(".s-item__link") else "No URL found"
        results.append({"title": title, "price": price, "url": item_url})
    return results if results else "No items found."

# Usage
# results = scrape_ebay_prices("Lego Ritterburg 6080")
# sorted_results = sort_results_by_price(results)
# print_results_as_table(sorted_results)