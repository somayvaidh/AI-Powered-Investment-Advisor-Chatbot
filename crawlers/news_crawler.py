import pandas as pd
import feedparser
import json
import time
import os
import re
import requests
from bs4 import BeautifulSoup

# Function to remove HTML tags from a string
def clean_html(html_text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", html_text)

def get_symbol_name_mapping():
    df = pd.read_csv("models/ind_nifty500list.csv")
    return dict(zip(df["Symbol"], df["Company Name"]))

def fetch_news_google(company_name, max_results=5):
    query = company_name.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_results]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": clean_html(entry.summary),  # Clean the summary
            "symbol": company_name
        })
    return articles

import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

import re

def get_detailed_summary(url, symbol):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the article
        text = soup.get_text(separator="\n")
        text = re.sub(r"\n+", "\n", text).strip()  # Remove excessive newlines

        # Split into blocks by line or paragraph
        blocks = text.split("\n")

        # Filter blocks that mention the symbol and are at least 250 characters long
        filtered = [blk.strip() for blk in blocks if len(blk.strip()) >= 250]

        if not filtered:
            return "Could not fetch detailed summary"

        # Join all filtered paragraphs
        return "\n\n".join(filtered)

    except Exception as e:
        print(f"Error fetching article {url}: {e}")
        return "Could not fetch detailed summary"

def crawl_and_save_news(symbols, mapping, max_results=5, output_file="semantic_cache/news_cache.json"):
    all_articles = []

    for symbol in symbols:
        company = mapping.get(symbol, symbol)
        print(f"📡 Crawling news for {company}")
        articles = fetch_news_google(company, max_results=max_results)

        for article in articles:
            detailed_summary = get_detailed_summary(article["link"], symbol)  # Pass symbol here
            article["detailed_summary"] = detailed_summary
            all_articles.append(article)

        time.sleep(1)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write all articles to JSON file in readable format
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    mapping = get_symbol_name_mapping()
    symbols = list(mapping.keys())[:5]  # First 5 symbols for testing
    crawl_and_save_news(symbols, mapping)

