from debug_print import debug_print

def filter_articles(articles, damaged_articles):
    filtered = []
    
    debug_print("[DEBUG] Filtering Articles")
    # remove duplicates
    seen = set()
    for article in articles:
        if article[10] not in seen:
            filtered.append(article)
            seen.add(article[10])

    # remove non-damaged vehicles from damaged articles and append to filtered array
    if damaged_articles != []:
        for article in damaged_articles:
            if article[10] not in seen:
                filtered.append(article)
                seen.add(article[10])

    if (len(articles)+len(damaged_articles) - len(filtered) != 0 or len(filtered) != len(articles)+len(damaged_articles)):
        print(f"[:] Found {len(articles)+len(damaged_articles) - len(filtered)} duplicate articles, they got removed and there are {len(filtered)} unique articles remaining.")
        print("that is a weird issue with the website that i can't fix ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    debug_print(f"[DEBUG] Unfiltered Articles Count: {len(articles)}")
    debug_print(f"[DEBUG] Filtered Articles Count: {len(filtered)}")


    # sort by points, highest first
    filtered.sort(key=lambda x: x[0], reverse=True)
    debug_print(f"[DEBUG] Returning filtered articles")
    return filtered