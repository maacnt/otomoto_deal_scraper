from debug_print import debug_print

min_hp = 0
max_hp = 1
min_year = 0
max_year = 1

def search_through_articles(articles_selected):
    for article in articles_selected:
        if not article[0] == "N/A":
            debug_print("[DEBUG] Article with already calculated points got fed, skipping dynamic range calculation for this article.")
        pass
    
    # calculate min and max year that appears in articles
    if int(article[5]) > max_year:
        max_year = int(article[5])
    if int(article[5]) < min_year:
        min_year = int(article[5])

    if int(article[7]) > max_hp:
        max_hp = int(article[7])
    if int(article[7]) < min_hp:
        min_hp = int(article[7])

def get_ranges(articles, damaged_articles):
    min_year = float("inf")
    max_year = float("-inf")
    min_hp = float("inf")
    max_hp = float("-inf")

    for article in articles + damaged_articles:
        # Skip articles that already have points calculated
        if article[0] != "N/A":
            continue

        year = int(article[5])
        if article[7] is not None:
            hp = int(article[7].split()[0])  # change "150 KM" -> 150
        else:
            continue

        min_year = min(min_year, year)
        max_year = max(max_year, year)
        min_hp = min(min_hp, hp)
        max_hp = max(max_hp, hp)


    debug_print(f"[DEBUG] Dynamic ranges calculated: {min_hp} - {max_hp} HP, {min_year} - {max_year} Year")
    return [min_hp, max_hp, min_year, max_year]