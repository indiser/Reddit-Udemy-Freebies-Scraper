import requests
import html
import re
import time

# 1. CONSTANTS
SUBREDDIT_URL = "https://www.reddit.com/r/udemyfreeebies/.json?limit=5"

PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"  # Case 1: Course Name ... Instructor
    r"(angela.*yu.*100.*days.*code)|"  # Case 2: Instructor ... Course Name
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Case 3: Full Title (No Instructor)
    re.IGNORECASE
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("--- Scraper Hit Verification ---")
try:
    print(f"Scraping {SUBREDDIT_URL}...")
    response = requests.get(url=SUBREDDIT_URL, headers=headers)
    
    if response.status_code == 429:
        raise Exception("Blocked by Reddit (Too Many Requests). Wait a while.")
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    data = response.json()
    posts = data["data"]["children"]
    
    found_count = 0

    for post in posts:
        post_data = post["data"]
        
        title = html.unescape(post_data.get("title", ""))
        selftext = html.unescape(post_data.get("selftext", ""))
        full_text = f"{title} \n {selftext}"

        if PATTERN.search(full_text):
            print("\n" + "="*40)
            print(f"🔥 MATCH FOUND!")
            print(f"Title: {title}")
            print(f"Link: {post_data.get('url')}")
            print("="*40)
            found_count += 1

    if found_count == 0:
        print("\nNo matches found in the top 5 posts.")

except Exception as e:
    print(f"CRITICAL FAILURE: {e}")