from curl_cffi import requests
import re
import json
import feedparser
from bs4 import BeautifulSoup

# 1. CONSTANTS
limit=10
SUBREDDIT_URL = f"https://www.reddit.com/r/udemyfreeebies/.rss?limit={limit}"

with open("cookies.json", "r", encoding="utf-8") as filp:
    raw_cookies = json.load(filp)

COOKIES = {cookie['name'] : cookie['value'] for cookie in raw_cookies}

PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"  # Case 1: Course Name ... Instructor
    r"(angela.*yu.*100.*days.*code)|"  # Case 2: Instructor ... Course Name
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Case 3: Full Title (No Instructor)
    re.IGNORECASE
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/atom+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

session = requests.Session(impersonate="chrome120")
session.cookies.update(COOKIES)
session.headers.update(HEADERS)

print("--- Scraper Hit Verification ---")
try:
    print(f"Scraping {SUBREDDIT_URL}...")
    response = session.get(SUBREDDIT_URL)
    
    if response.status_code == 429:
        raise Exception("Blocked by Reddit (Too Many Requests). Wait a while.")
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    feed = feedparser.parse(response.content)
    found_count = 0

    for entry in feed.entries[1:]:
        title = entry.title
        html_body = entry.content[0].value if entry.get("content") else ""
        selftext = BeautifulSoup(html_body, "html.parser").get_text("\n", strip=True)
        full_text = f"{title} \n {selftext}"

        print(f"- {title}")

        if PATTERN.search(full_text):
            print("\n" + "=" * 40)
            print("MATCH FOUND!")
            print(f"Title: {title}")
            print(f"Link: {entry.link}")
            print("=" * 40)
            found_count += 1

    if found_count == 0:
        print(f"\nNo matches found in the top {limit} posts.")

except Exception as e:
    print(f"CRITICAL FAILURE: {e}")
