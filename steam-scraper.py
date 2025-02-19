import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd
import os

pages_html = ""
for page_number in range(1, 6):
    res = requests.get(f"https://store.steampowered.com/search/?supportedlang=english&specials=1&page={page_number}&ndl=1")
    pages_html += res.text

soup = BeautifulSoup(pages_html, "html.parser")
game_containers = soup.find_all("div", {"class": "responsive_search_name_combined"})

titles = [
    game.find("span", {"class": "title"}).text if game.find("span", {"class": "title"}) else None
    for game in game_containers
]

rating_system = ["Overwhelmingly Negative", "Very Negative", "Negative", "Mostly Negative",
                 "Mixed", "Mostly Positive", "Positive", "Very Positive", "Overwhelmingly Positive"]

ratings, reviews = [], []
for game in game_containers:
    rating_span = game.find("span", {"class": "search_review_summary"})
    if rating_span:
        data_tooltip = rating_span["data-tooltip-html"]
        rating = data_tooltip.split("<br>")[0]
        ratings.append(rating_system.index(rating))
        reviews.append(data_tooltip.split("<br>")[1].split(" ")[3])
    else:
        ratings.append(None)
        reviews.append(None)

def parse_price(price_str):
    if price_str:
        clean_price = re.sub(r"[^\d.,]", "", price_str)
        return float(clean_price.replace(",", "."))
    return None

discounts = [
    int(game.find("div", {"class": "discount_pct"}).text.strip("%"))
    if game.find("div", {"class": "discount_pct"}) else None
    for game in game_containers
]

prices = [
    parse_price(game.find("div", {"class": "discount_final_price"}).text)
    if game.find("div", {"class": "discount_final_price"}) else None
    for game in game_containers
]

original_prices = [
    parse_price(game.find("div", {"class": "discount_original_price"}).text)
    if game.find("div", {"class": "discount_original_price"}) else None
    for game in game_containers
]

release_dates = [
    game.find("div", {"class": "search_released"}).text.strip()
    if len(game.find("div", {"class": "search_released"}).text) > 2 else None
    for game in game_containers
]

win, lin, osx = [], [], []
for game in game_containers:
    platforms = [platform["class"][1] for platform in game.find_all("span", {"class": "platform_img"})]
    win.append(1 if "win" in platforms else 0)
    lin.append(1 if "linux" in platforms else 0)
    osx.append(1 if "mac" in platforms else 0)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
fetch_times = [current_time for _ in game_containers]

data = {
    "Game Name": titles,
    "Rating": ratings,
    "#Reviews": reviews,
    "Discount%": discounts,
    "Price (€)": prices,
    "Original Price (€)": original_prices,
    "Release Date": release_dates,
    "Windows": win,
    "Linux": lin,
    "MacOS": osx,
    "Fetched At": fetch_times
}

steam_sales = pd.DataFrame(data)
filtered_steam_sales = steam_sales.dropna()

file_path = "steam_sales.csv"
if not os.path.exists(file_path):
    filtered_steam_sales.to_csv(file_path, index=False)
else:
    filtered_steam_sales.to_csv(file_path, mode="a", index=False, header=False)

print(f"Data saved to {file_path}")
