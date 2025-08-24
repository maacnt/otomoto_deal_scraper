import math
import requests
from bs4 import BeautifulSoup
import csv
import random
from get_scrape_data import getscrapingdata
from shared import headers,link_to_look,articles,include_damaged_vehicles,damaged_articles
import shared
from filter_articles import filter_articles
from debug_print import debug_print
from data_from_link import change_damaged_vehicles_param


def send_request():
    from shared import link_to_look
    header = headers[random.randint(0, len(headers) - 1)]
    request = requests.get(shared.link_to_look, headers={"User-Agent": header})
    print("Sending the request...")
    

    if (request.status_code != 200):
        print("================ [!] Cannot access website [!] ================")
        print("If you see this error, please check your internet connection (turning off your VPN if you have one) or check the website status.")
        print("If the issue persists, try changing the headers in shared.py file")
        print("The link might be invalid or might have changed")
        print("If all all the above steps fail, try using a minimalistic scraping script to debug the issue.")
        return
    print("================ Request successful =================")


    soup = BeautifulSoup(request.text, "html.parser")
    print("Website loaded")

    total_articles = soup.find("b").text
    print("[:] Found total articles:", total_articles)

    should_be_pages = math.ceil(int(total_articles) / 32)
    pages = 1
    if soup.find("li", class_="ooa-6ysn8b"):
        pages = soup.find("li", class_="ooa-6ysn8b").text

    if (pages != should_be_pages):
        print("[!] Page count mismatch between scraped from website and calculated from the amount of results:", pages, "!=", should_be_pages)
        print("[:] Adjusting pages to match expected:", should_be_pages)
        pages = should_be_pages
    elif (pages > should_be_pages):
        print("[!] Found more pages on the website than expected from the calculations of all results:", pages, ">", should_be_pages)
        print("[:] Adjusting pages:", pages)
        pages = should_be_pages
    else:
        print("[:] Found pages:", pages)

    return pages

def write_to_csv(articles):
    print("[:] Data Scraped\n[:] Writing to CSV...")
    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Scored Points", "Mileage", "Price", "Fuel Type", "Gearbox", "Year", "Engine L", "Engine HP", "Extra Data", "Title Offer", "Link"])
        for row in articles:
            writer.writerow(row)

def main():
    from shared import link_to_look
    pages = send_request()
    
    if pages is None:
        print("[!] Failed to retrieve pages")
        debug_print("[DEBUG] Pages is None!!!!!")
        return
    
    global articles
    articles.clear()
    print("Scraping articles...")

    

    # Get all articles and put them into array (refer to get_scraping_data for code)
    getscrapingdata(pages, False, shared.link_to_look)

    if articles is None:
        print("[!] Failed to retrieve articles")
        debug_print("[DEBUG] Articles is None!!!!!")
        return

    debug_print(f"[DEBUG] include_damaged_vehicles: {shared.include_damaged_vehicles}")
    if shared.include_damaged_vehicles:
        print("[:] Reenacting scraping process for damaged vehicles (they will be included with [D]). If you do not wish to include them, set your filters to undamaged only")
        shared.link_to_look = change_damaged_vehicles_param(shared.link_to_look, "1")
        pages = send_request()
        getscrapingdata(pages, True, shared.link_to_look)

        if pages is None:
            print("[!] Failed to retrieve pages")
            debug_print("[DEBUG] Pages is None!!!!!")
            return
        
        print("[:] Second scraping done...")

    # Filter articles
    debug_print(f"[DEBUG] Filtering articles in main {len(articles)} of articles and {len(damaged_articles)} damaged articles")
    articles = filter_articles(articles,damaged_articles)
    debug_print(f"[DEBUG] Filtered articles in main: {len(articles)}")

    # Write articles array to CSV
    debug_print("[DEBUG] Writing articles to CSV")
    write_to_csv(articles)

    print("================ Scraping completed. check output.csv for results ================")


if __name__ == "__main__":
    main()