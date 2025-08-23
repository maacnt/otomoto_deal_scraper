import math
import requests
from bs4 import BeautifulSoup
import csv
import random
from get_scrape_data import getscrapingdata
from shared import headers,link_to_look,articles

header = headers[random.randint(0, len(headers) - 1)]
request = requests.get(link_to_look, headers={"User-Agent": header})
print("Sending the request...")


def write_to_csv(articles):
    print("Data Scraped\nWriting to CSV...")
    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Scored Points", "Mileage", "Price", "Fuel Type", "Gearbox", "Year", "Engine L", "Engine HP", "Extra Data", "Title Offer", "Link"])
        for row in articles:
            writer.writerow(row)

def main():
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

    global articles
    articles.clear()
    print("Scraping articles...")

    # Get all articles and put them into array (refer to get_scraping_data for code)
    getscrapingdata(pages)

    # Write articles array to CSV
    write_to_csv(articles)

    print("================ Scraping completed. check output.csv for results ================")

if __name__ == "__main__":
    main()