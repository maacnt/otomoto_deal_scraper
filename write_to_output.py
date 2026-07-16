import csv

def write_to_csv(articles):
    print("[:] Data Scraped\n[:] Writing to CSV...")
    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Scored Points", "Mileage", "Price", "Fuel Type", "Gearbox", "Year", "Engine L", "Engine HP", "Extra Data", "Title Offer", "Link"])
        for row in articles:
            writer.writerow(row)
            
def write_to_js(articles):
    print("[:] Data Scraped\n[:] Writing to JS to view on the website...")
    with open("output.js", "w", encoding="utf-8") as jsfile:
        jsfile.write("const articles = [\n")
        for row in articles:
            # remove '' from all string values (breaks the website if someone decides to add it)
            if isinstance(row, str):
                row = [value.strip("'") for value in row]

            jsfile.write("    {\n")
            jsfile.write(f"        scoredPoints: {row[0]},\n")
            jsfile.write(f"        mileage: '{row[1]}',\n")
            jsfile.write(f"        price: '{row[2]}',\n")
            jsfile.write(f"        fuelType: '{row[3]}',\n")
            jsfile.write(f"        gearbox: '{row[4]}',\n")
            jsfile.write(f"        year: '{row[5]}',\n")
            jsfile.write(f"        engineL: '{row[6]}',\n")
            jsfile.write(f"        engineHP: '{row[7]}',\n")
            jsfile.write(f"        extraData: '{row[8]}',\n")
            jsfile.write(f"        titleOffer: '{row[9]}',\n")
            jsfile.write(f"        link: '{row[10]}',\n")
            jsfile.write(f"        carImage: '{row[11]}'\n")
            jsfile.write("    },\n")
        jsfile.write("];\n")