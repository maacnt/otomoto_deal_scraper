from shared import data

year_from = data.get("year_from")
year_to = data.get("year_to")
price_from = data.get("price_from")
price_to = data.get("price_to")
mileage_from = data.get("mileage_from")
mileage_to = data.get("mileage_to")
fuel_types = data.get("fuel_types")

if (mileage_to is None):
    print("[!] No max Mileage filter set for pointing, assuming max for 350000, change it for your use case (NOTE FOR DEFAULT MILEAGE: It will still Rank cars with higher mileage, but anything past 350000 will have 0 points)")
    mileage_to = 350000
if (year_to is None):
    print("[!] No max Year filter set for pointing, assuming max for 2025, change it for your use case")
    year_to = 2025
if (year_from is None):
    print("[!] No min Year filter set for pointing, assuming min for 1998, change it for your use case")
    year_from = 1998
elif (year_from is None and year_to is not None):
    print("[!] No min Year filter set for pointing, assuming min -15 years of max year, change it for your use case")
    year_from = year_to - 15
if (price_to is None):
    print("[!] No max Price filter set for pointing, assuming max for 30000, change it for your use case (NOTE FOR DEFAULT PRICE: It will still Rank cars with higher price, but anything past 30000 will have 0 points)")
    price_to = 30000
if (price_from is None):
    print("[!] No min Price filter set for pointing, assuming min for 0, change it for your use case")
    price_from = 0
if (mileage_from is None):
    print("[!] No min Mileage filter set for pointing, assuming min for 0, change it for your use case")
    mileage_from = 0

def calculate_points(mileage, price, fuel_type, gearbox, year, engine_hp):
    points = 0

    # mileage pointing
    max_mileage = mileage_to
    try:
        mileage_val = int(str(mileage).capitalize().replace(" ", "").replace("km", "").replace("‎", ""))
        if mileage_val <= 0:
            mileage_score = 0
        elif mileage_val >= max_mileage:
            mileage_score = 0
        else:
            mileage_score = max(0, 90 - int((mileage_val / max_mileage) * 90))
    except Exception:
        mileage_score = 0

    points += mileage_score
    
    # price pointing
    
    max_price = int(str(price_to).replace(" ", "").replace("zł", "").replace("‎", ""))
    min_price = int(str(price_from).replace(" ", "").replace("zł", "").replace("‎", ""))
    try:
        price_val = int(str(price).capitalize().replace(" ", "").replace("zł", "").replace("‎", ""))
        if price_val <= min_price:
            price_score = 120
        elif price_val >= max_price:
            price_score = 0
        else:
            price_score = max(0, int(((max_price - price_val) / (max_price - min_price)) * 120))
    except Exception as e:
        print(f"[!] Exception Occurred: {e}")
        price_score = 0
    points += price_score

    if (fuel_type == "Diesel"):
        points += 15
    elif (fuel_type == "Benzyna"):
        points += 13
    elif (fuel_type == "Benzyna+LPG"):
        points += 7
    elif (fuel_type == "LPG"):
        points += 5

    if (gearbox == "Manual"):
        points += 5
    elif (gearbox == "Automatic"):
        points += 2

    max_year = year_to
    min_year = year_from
    try:
        year_val = int(str(year).capitalize().replace(" ", "").replace("r.", "").replace("‎", ""))
        if year_val < min_year or year_val > max_year:
            year_score = 0
        else:
            year_score = max(0, 35 - int(((max_year - year_val) / (max_year - min_year)) * 35))
    except Exception:
        year_score = 0
    points += year_score

    # engine_hp pointing
    try:
        engine_hp_val = int(str(engine_hp).capitalize().replace(" ", "").replace("KM", "").replace("‎", ""))
        # okay so for the engine horsepower, i have no idea how to make it dynamically calculate it so it will just remain like this
        min_engine_hp = 105
        max_engine_hp = 310
        if engine_hp_val < min_engine_hp or engine_hp_val > max_engine_hp:
            engine_hp_score = 0
        else:
            engine_hp_score = max(0, int(((engine_hp_val - min_engine_hp) / (max_engine_hp - min_engine_hp)) * 15))
    except Exception:
        engine_hp_score = 0
    points += engine_hp_score

    return points
