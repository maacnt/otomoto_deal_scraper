from shared import re
from urllib.parse import urlencode, urlparse, parse_qs



def data_from_link(link):
    import shared
    from debug_print import debug_print
    from shared import debug_mode, include_damaged_vehicles, link_to_look
    from urllib.parse import urlencode, urlunparse

    parsed_url = urlparse(link)
    params = parse_qs(parsed_url.query)

    
    # Add 'search[filter_enum_damaged]' if not present to later look for damaged and non-damaged vehicles separately
    if "search[filter_enum_damaged]" not in params:
        print("[!] You have not set a filter if the car was damaged or not, both undamaged and damaged cars will be shown, with the damaged being marked with a '[D]!' symbol")
        shared.include_damaged_vehicles = True
        debug_print(f"[DEBUG] Adding 'search[filter_enum_damaged]' parameter with value of 0")
        link = change_damaged_vehicles_param(link, "0")
        shared.link_to_look = link

    possible_year_from = None
    match = re.search(r'/od-(\d{4})', parsed_url.path)
    if match:
        possible_year_from = match.group(1)

    # Extract values from the link itself
    year_from = params.get("search[filter_float_year:from]", [None])[0]
    if year_from is None and possible_year_from is not None:
        print("[:] Using oldest year from URL path instead of parameters of the link (weird link problem):", possible_year_from)
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

    if debug_mode:
        print("[DEBUG] Parsed URL:", parsed_url)
        print("[DEBUG] Extracted parameters:", params)
        print(f"[DEBUG] Parameters variables:\n year_from: {year_from}\n year_to: {year_to}\n price_from: {price_from}\n price_to: {price_to}\n mileage_from: {mileage_from}\n mileage_to: {mileage_to}\n fuel_types: {fuel_types} \n[DEBUG]")

    return {
        "year_from": year_from,
        "year_to": year_to,
        "price_from": price_from,
        "price_to": price_to,
        "mileage_from": mileage_from,
        "mileage_to": mileage_to,
        "fuel_types": fuel_types
    }
    
def change_damaged_vehicles_param(link, value):
    changed_link = link
    parsed_url = urlparse(link)
    from debug_print import debug_print
    from urllib.parse import urlencode, urlunparse
    params = parse_qs(parsed_url.query)

    debug_print(f"[DEBUG] changing 'search[filter_enum_damaged]' parameter to {value}")
    params["search[filter_enum_damaged]"] = [value]
    # Rebuild the query string
    new_query = urlencode(params, doseq=True)
    # Rebuild the link with the new query
    changed_link = urlunparse(parsed_url._replace(query=new_query))
    debug_print(f"[DEBUG] changed_link: {changed_link}")
    parsed_url = urlparse(changed_link)
    params = parse_qs(parsed_url.query)

    return changed_link