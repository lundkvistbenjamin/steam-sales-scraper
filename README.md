# Steam Sales Scraper 🚀

A Python-based web scraper that collects discounted game data from the **Steam store** and saves it as a CSV file for analysis.

## Features
✅ Scrapes discounted games from multiple Steam store pages
✅ Extracts game details (title, rating, reviews, discount, price, release date, platforms)
✅ Saves data as a structured **CSV file**
✅ Works in **Google Colab**

## Requirements
- Python 3.x
- `requests`
- `beautifulsoup4`
- `pandas`

You can install the required libraries using:
```bash
pip install requests beautifulsoup4 pandas
```

## Usage
### Run in Google Colab
1. Open **Google Colab**
2. Upload the notebook or create a new one
3. Copy-paste the script and run

### Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/lundkvistbenjamin/steam-sales-scraper.git
   cd steam-sales-scraper
   ```
2. Run the script:
   ```bash
   python steam_scraper.py
   ```
3. The scraped data will be saved in `steam_sales.csv`.

## Output Example
```
| Game Title       | Rating         | # Reviews | Discount % | Final Price | Original Price | Release Date | Win | Lin | OSX |
|------------------|---------------|-----------|------------|-------------|---------------|--------------|-----|-----|-----|
| Cyberpunk 2077  | Very Positive  | 694,555   | 50%        | 29.99€      | 59.99€        | 10 Dec, 2020 | 1   | 0   | 0   |
```
 
## License
MIT License
