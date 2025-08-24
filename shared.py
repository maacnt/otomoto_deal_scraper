import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
from data_from_link import data_from_link


link_to_look = ""

debug_mode = False # will scan only 2 pages and will print out extra information
debug_mode_rating = False # will print out extra information for rating calculations (CAN SPAM OUT THE CONSOLE). Doesn't need debug_mode to be on to work


# ====================================== DO NOT CHANGE ANYTHING BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING ======================================


include_damaged_vehicles = False # DO NOT CHANGE!!!!!!! if you don't want crashed vehicles to be included just change it in the filters on the site
# the variable is for only when you do not have a filter for damaged/undamaged vehicles and will look for both undamaged and damaged vehicles
# separately to rank them appropriately in the CSV file, changing the variable to true will break the script (most likely)

if link_to_look == "":
    print("==================================================")
    link_to_look = input("Paste in the link with already applied filters to look for a car (the link can be set as static under the 'shared.py' file in line 9)\n-> ")
    if link_to_look == "" or link_to_look.isspace():
        print("[!] No link provided, exiting...")
        exit()

data = data_from_link(link_to_look)


# List of user-agent headers to randomize requests (not necessary but helps avoid detection)
headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.48 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Safari/605.1.15"
]

articles = []
damaged_articles = []