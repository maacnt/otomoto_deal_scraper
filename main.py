# LIB IMPORT
import math
import requests
from bs4 import BeautifulSoup # type: ignore
# for some reason i have to ignore the import error for bs4 /shrug 
import random
import webbrowser
import os

# FILE IMPORT
import shared
from get_scrape_data import getscrapingdata
from shared import headers,link_to_look,articles,include_damaged_vehicles,damaged_articles,use_csv_instead
from filter_articles import filter_articles
from debug_print import debug_print
from data_from_link import change_damaged_vehicles_param
from write_to_output import write_to_js,write_to_csv
from get_ranges_from_articles import get_ranges
from point_calculator import calculate_article_points

def send_request():
    from shared import link_to_look
    print("Sending the request...")
    try:
        header = headers[random.randint(0, len(headers) - 1)]
        request = requests.get(shared.link_to_look, headers={"User-Agent": header})
    except Exception as e:
        print("\n\n\n\n\n[!] An error occured with the provided link, double check if it's correct and if continues create an issue on the github repo")
        debug_print("[DEBUG] Exception occurred while sending request:", e)
        return

    if (request.status_code != 200):
        print("================ [!] Cannot access website [!] ================")
        print("If you see this error, please check your internet connection (turning off your VPN if you have one) or check the website status.")
        print("If the issue persists, try changing the headers in shared.py file")
        print("The link might be invalid or might have changed")
        print("If all all the above steps fail, create an issue on github and i'll look into it")
        return
    print("================ Request successful =================")


    soup = BeautifulSoup(request.text, "html.parser")
    print("Website loaded")

    #total_articles = soup.find("b").text # they had to change it :skull:
    total_articles = soup.find("p", class_="ooa-1h4mewe").text
    total_articles = [int(s) for s in total_articles.split() if s.isdigit()]
    total_articles = sum(total_articles)
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

    # Get dynamic ranges for pointing and then go and point every vehicle
    dynamic_variables = [min_hp := 0, max_hp := 0, min_year := 0, max_year := 0]
    dynamic_variables = get_ranges(articles, damaged_articles)
    
    # Calculate points with dynamic ranges
    calculate_article_points(articles, damaged_articles, *dynamic_variables)

    # Filter articles
    debug_print(f"[DEBUG] Filtering articles in main {len(articles)} of articles and {len(damaged_articles)} damaged articles")
    articles = filter_articles(articles,damaged_articles)
    debug_print(f"[DEBUG] Filtered articles in main: {len(articles)}")
    
    # Write articles array to CSV
    if not use_csv_instead:
        debug_print("[DEBUG] Writing articles to .js file")
        write_to_js(articles)

    if use_csv_instead:
        debug_print("[DEBUG] Writing articles to CSV")
        write_to_csv(articles)

    print("================ Scraping completed. check output.csv for results ================")
    
    # Open the website for viewing
    if not use_csv_instead:
        html_file_path = os.path.abspath("website/index.html")
        webbrowser.open(f"file://{html_file_path}")


if __name__ == "__main__":
    main()