import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
from data_from_link import data_from_link


link_to_look = "https://www.otomoto.pl/osobowe/bmw/seria-3/seg-coupe--seg-sedan/od-1998?search%5Bfilter_enum_generation%5D%5B0%5D=gen-e46-1998-2007&search%5Bfilter_enum_generation%5D%5B1%5D=gen-e90-2005-2012&search%5Bfilter_float_price%3Ato%5D=30000&search%5Bfilter_float_year%3Ato%5D=2013&search%5Border%5D=created_at%3Adesc"

if link_to_look == "":
    link_to_look = input("Paste in the link with already applied filters to look for a car (the link can be set as static under the 'shared.py' file in line 9)\n")
    if link_to_look == "":
        print("[!] No link provided, exiting...")
        exit()

data = data_from_link(link_to_look)


# List of user-agent headers to randomize requests (not necessary but helps avoid detection)
headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.48 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
]

articles = []