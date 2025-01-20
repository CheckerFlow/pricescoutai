
import re
from tabulate import tabulate

def format_results_as_table(results):
    if isinstance(results, str):
        #print(results)
        return results
    else:
        table = [[item["title"], item["price"], item["url"]] for item in results]
        results = tabulate(table, headers=["Title", "Price", "URL"], tablefmt="pretty")
        #print(results)
        return results

def sort_results_by_price(results):
    def extract_price(price_str):
        price = re.findall(r'\d+,\d+|\d+', price_str.replace('.', '').replace(',', '.'))
        return float(price[0]) if price else 0.0

    if isinstance(results, list):
        results.sort(key=lambda x: extract_price(x["price"]))
    return results