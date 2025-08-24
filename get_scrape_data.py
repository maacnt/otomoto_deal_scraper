from shared import articles, headers, random, requests, BeautifulSoup, debug_mode, damaged_articles
from point_calculator import calculate_points

def getscrapingdata(pages, include_damaged_vehicles, link_to_look):
    from debug_print import debug_print
    
    if debug_mode and True: # Change to False if you still want to look through all pages
        pages = 2
        
    debug_print(f"[DEBUG] Received link as {link_to_look}")
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        if page == 1:
            header = headers[random.randint(0, len(headers) - 1)]
            first_page = requests.get(link_to_look, headers={"User-Agent": header})
            soup = BeautifulSoup(first_page.text, "html.parser")
        else:
            header = headers[random.randint(0, len(headers) - 1)]
            next_page = requests.get(f"{link_to_look}&page={page}", headers={"User-Agent": header})
            soup = BeautifulSoup(next_page.text, "html.parser")

        for article in soup.find_all("article"):
            mileage = article.find("dd", {"data-parameter": "mileage"})
            fuel_type = article.find("dd", {"data-parameter": "fuel_type"})
            gearbox = article.find("dd", {"data-parameter": "gearbox"})
            year = article.find("dd", {"data-parameter": "year"})
            price = article.find("h3", class_="efzkujb1 ooa-1qiba3v")
            title = article.find("h2", class_="etydmma0 ooa-iasyan")
            link = article.find("a")
            extra_data = article.find("p", class_="e1afgq2j0 ooa-pr7t48")
            engine_l = engine_hp = extra_data_text = ""
            
            if extra_data is not None:
                extra_data_text = extra_data.text.strip()
                parts = [part.strip() for part in extra_data_text.split("•")]
                engine_l = parts[0] if len(parts) > 0 else ""
                engine_hp = parts[1] if len(parts) > 1 else ""
                extra_data_text = parts[2] if len(parts) > 2 else ""
                

            if mileage and price and fuel_type and gearbox and year: #after all data is collected
                
                # Mileage fix for mileages that aren't in thousands (example: 500 km -> 500 000 km)
                mileage_val = int(str(mileage.text.strip()).capitalize().replace(" ", "").replace("km", ""))
                mileage = mileage.text.strip()
                if mileage_val < 1000:
                    mileage = mileage.replace(" km", " 000 km")

                # Calculate points based on the collected data
                # Refer to point_calculator.py for the calculate_points function
                points = calculate_points(
                    mileage,
                    price.text.strip(),
                    fuel_type.text.strip(),
                    gearbox.text.strip(),
                    year.text.strip(),
                    engine_hp
                )

                # Prepare data for extraction for csv by appending the array
                mileage_value = mileage.replace(" ", "‎ ")
                price_value = price.text.strip() + "zł"

                if not include_damaged_vehicles:
                    articles.append([
                        points,
                        mileage_value,
                        price_value,
                        fuel_type.text.strip(),
                        gearbox.text.strip(),
                        year.text.strip(),
                        engine_l,
                        engine_hp,
                        extra_data_text,
                        title.text.strip(),
                        link["href"] if link else ""
                    ])
                else:
                    damaged_articles.append([
                        points,
                        mileage_value,
                        price_value,
                        fuel_type.text.strip(),
                        gearbox.text.strip(),
                        year.text.strip(),
                        engine_l,
                        engine_hp,
                        extra_data_text,
                        "[D]! " + title.text.strip(),
                        link["href"] if link else ""
                    ])

    return