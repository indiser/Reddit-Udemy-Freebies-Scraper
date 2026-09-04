from curl_cffi import requests
import json
import html
import re

with open("cookies.json", "r", encoding="utf-8") as filp:
    raw_cookies = json.load(filp)

COOKIES = {cookie['name'] : cookie['value'] for cookie in raw_cookies}

PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"  # Case 1: Course Name ... Instructor
    r"(angela.*yu.*100.*days.*code)|"  # Case 2: Instructor ... Course Name
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Case 3: Full Title (No Instructor)
    re.IGNORECASE
)

reddit_url="https://www.reddit.com/r/udemyfreeebies/.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

session = requests.Session(impersonate="chrome120")
session.cookies.update(COOKIES)
session.headers.update(HEADERS)

# response=requests.get(url=reddit_url,impersonate="chrome120", cookies=COOKIES, headers=HEADERS)
response = session.get(reddit_url)

data=html.unescape(response.json()["data"]["children"][1]["data"]["selftext"])

with open("courses.txt", "w", encoding="utf-8") as filp:
    filp.write(data)

print("--- Scraper Hit Verification ---")
for course in data:
    if re.search(PATTERN, course):
        print(f"Match found: {course.strip()}")
    else:
        print("No match found")
        break
