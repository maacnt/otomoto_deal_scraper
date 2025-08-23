from shared import re
from urllib.parse import urlparse, parse_qs

def data_from_link(link):
    parsed_url = urlparse(link)
    params = parse_qs(parsed_url.query)

    possible_year_from = None
    match = re.search(r'/od-(\d{4})', parsed_url.path)
    if match:
        possible_year_from = match.group(1)

    # Extract values from the link itself
    year_from = params.get("search[filter_float_year:from]", [None])[0]
    if year_from is None and possible_year_from is not None:
        print("[!] Using oldest year from URL path instead of parameters of the link (weird link problem):", possible_year_from)
        year_from = possible_year_from
    year_to = params.get("search[filter_float_year:to]", [None])[0]
    price_from = params.get("search[filter_float_price:from]", [None])[0]
    price_to = params.get("search[filter_float_price:to]", [None])[0]
    mileage_from = params.get("search[filter_float_mileage:from]", [None])[0]
    mileage_to = params.get("search[filter_float_mileage:to]", [None])[0]

    # Fuel types: handle both array and indexed keys
    fuel_types = []
    for k, v in params.items():
        if k.startswith("search[filter_enum_fuel_type]"):
            fuel_types.extend(v)

    return {
        "year_from": year_from,
        "year_to": year_to,
        "price_from": price_from,
        "price_to": price_to,
        "mileage_from": mileage_from,
        "mileage_to": mileage_to,
        "fuel_types": fuel_types
    }