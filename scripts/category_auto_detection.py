async def category_auto_detection(answer):
    for item in answer.split(" "):
        for year in item.split("-"):
            if year.isdigit() and int(year) > 1916:
                return "1"
    return "9"
