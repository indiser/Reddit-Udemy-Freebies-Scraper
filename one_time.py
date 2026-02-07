import requests
import json
import html
import re

PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"  # Case 1: Course Name ... Instructor
    r"(angela.*yu.*100.*days.*code)|"  # Case 2: Instructor ... Course Name
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Case 3: Full Title (No Instructor)
    re.IGNORECASE
)

reddit_url="https://www.reddit.com/r/udemyfreeebies/.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response=requests.get(url=reddit_url,headers=headers)

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
