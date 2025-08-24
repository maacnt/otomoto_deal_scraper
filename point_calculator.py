from debug_print import debug_rating_print
from shared import data


year_from = data.get("year_from")
year_to = data.get("year_to")
price_from = data.get("price_from")
price_to = data.get("price_to")
mileage_from = data.get("mileage_from")
mileage_to = data.get("mileage_to")
fuel_types = data.get("fuel_types")

#ik this probably could be done better but that's for later
if (mileage_to is None):
    print("[!] No max Mileage filter set for ranking, assuming max for 350000, change it for your use case (NOTE FOR DEFAULT MILEAGE: It will still Rank cars with higher mileage, but anything past 350000 will have 0 points for mileage)")
    mileage_to = 350000
if (year_to is None):
    print("[!] No max Year filter set for ranking, assuming max for 2025, change it for your use case")
    year_to = 2025
if (year_from is None):
    if year_to is not None:
        print("[!] No min Year filter set for ranking, assuming min -10 years of max year, change it for your use case")
        year_from = year_to - 10
    else:
        print("[!] No min Year filter set for ranking, assuming min for 1998, change it for your use case")
        year_from = 1998
elif (year_from is None and year_to is not None):
    print("[!] No min Year filter set for ranking, assuming min -15 years of max year, change it for your use case")
    year_from = year_to - 15
if (price_to is None):
    print("[!] No max Price filter set for ranking, assuming max for 30000, change it for your use case (NOTE FOR DEFAULT PRICE: It will still Rank cars with higher price, but anything past 30000 will have 0 points)")
    price_to = 30000
if (price_from is None):
    print("[!] No min Price filter set for ranking, assuming min for 0, change it for your use case")
    price_from = 0
if (mileage_from is None):
    print("[!] No min Mileage filter set for ranking, assuming min for 0, change it for your use case")
    mileage_from = 0

def calculate_points(mileage, price, fuel_type, gearbox, year, engine_hp):
    points = 0

    # mileage pointing
    max_mileage = int(str(mileage_to).replace(" ", "").replace("km", "").replace("‎", ""))
    min_mileage = int(str(mileage_from).replace(" ", "").replace("km", "").replace("‎", ""))
    try:
        mileage_val = int(str(mileage).replace(" ", "").replace("km", "").replace("‎", ""))
        if mileage_val < min_mileage or mileage_val > max_mileage:
            mileage_score = 0
        else:
            mileage_score = max(0, int(((max_mileage - mileage_val) / (max_mileage - min_mileage)) * 85))
    except Exception as e:
        print(f"[!] Exception Occurred: {e}")
        mileage_score = 0

    debug_rating_print("[RATING DEBUG] Mileage:", mileage, "->", mileage_val, "points:", mileage_score)
    points += mileage_score
    
    # price pointing
    
    max_price = int(str(price_to).replace(" ", "").replace("zł", "").replace("‎", ""))
    min_price = int(str(price_from).replace(" ", "").replace("zł", "").replace("‎", ""))
    try:
        price_val = int(str(price).replace(" ", "").replace("zł", "").replace("‎", ""))
        if price_val <= min_price:
            price_score = 110
        elif price_val >= max_price:
            price_score = 0
        else:
            price_score = max(0, int(((max_price - price_val) / (max_price - min_price)) * 110))
    except Exception as e:
        print(f"[!] Exception Occurred: {e}")
        price_score = 0
    debug_rating_print("[RATING DEBUG] Price:", price, "->", price_val, "points:", price_score)
    points += price_score

    if (fuel_type == "Diesel"):
        points += 15
        debug_rating_print("[RATING DEBUG] Fuel Type: Diesel -> points:", 15)
    elif (fuel_type == "Benzyna"):
        points += 13
        debug_rating_print("[RATING DEBUG] Fuel Type: Benzyna -> points:", 13)
    elif (fuel_type == "Benzyna+LPG"):
        points += 7
        debug_rating_print("[RATING DEBUG] Fuel Type: Benzyna+LPG -> points:", 7)
    elif (fuel_type == "LPG"):
        points += 5
        debug_rating_print("[RATING DEBUG] Fuel Type: LPG -> points:", 5)

    if (gearbox == "Manualna"):
        points += 5
        debug_rating_print("[RATING DEBUG] Gearbox: Manualna -> points:", 5)
    elif (gearbox == "Automatyczna"):
        points += 2
        debug_rating_print("[RATING DEBUG] Gearbox: Automatyczna -> points:", 2)

    max_year = int(str(year_to).replace(" ", "").replace("r.", "").replace("‎", ""))
    min_year = int(str(year_from).replace(" ", "").replace("r.", "").replace("‎", ""))
    try:
        year_val = int(str(year).replace(" ", "").replace("r.", "").replace("‎", ""))
        if year_val < min_year or year_val > max_year:
            year_score = 0
        else:
            year_score = max(0, 35 - int(((max_year - year_val) / (max_year - min_year)) * 35))
    except Exception as e:
        print(f"[!] Exception Occurred: {e}")
        year_score = 0

    debug_rating_print("[RATING DEBUG] Year:", year, "->", year_val, "points:", year_score)
    points += year_score

    # engine_hp pointing
    try:
        engine_hp_val = int(str(engine_hp).replace(" ", "").replace("KM", "").replace("‎", ""))
        # okay so for the engine horsepower, i have no idea how to make it dynamically calculate min and max so it will just remain like this
        min_engine_hp = 105
        max_engine_hp = 310
        if engine_hp_val < min_engine_hp or engine_hp_val > max_engine_hp:
            engine_hp_score = 0
        else:
            engine_hp_score = max(0, int(((engine_hp_val - min_engine_hp) / (max_engine_hp - min_engine_hp)) * 15))
    except Exception as e:
        print(f"[!] Exception Occurred: {e}")
        engine_hp_score = 0
    debug_rating_print("[RATING DEBUG] Engine HP:", engine_hp, "->", engine_hp_val, "points:", engine_hp_score)
    points += engine_hp_score

    debug_rating_print("[RATING DEBUG] Total Points:", points)
    debug_rating_print("===================================")

    return points
