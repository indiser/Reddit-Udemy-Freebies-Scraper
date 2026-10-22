from curl_cffi import requests
import json
import re
import feedparser
from bs4 import BeautifulSoup

with open("cookies.json", "r", encoding="utf-8") as filp:
    raw_cookies = json.load(filp)

COOKIES = {cookie['name'] : cookie['value'] for cookie in raw_cookies}

PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"  # Case 1: Course Name ... Instructor
    r"(angela.*yu.*100.*days.*code)|"  # Case 2: Instructor ... Course Name
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Case 3: Full Title (No Instructor)
    re.IGNORECASE
)

reddit_url="https://www.reddit.com/r/udemyfreeebies/.rss"

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

response = session.get(reddit_url)
feed = feedparser.parse(response.content)
entry = next(e for e in feed.entries if "Udemy Free Courses" in e.title)
soup = BeautifulSoup(entry.content[0].value, "html.parser")
lines = [f"# {entry.title}", ""]
for li in soup.find_all("li"):
    a = li.find("a")
    if not a:
        continue
    url = a["href"]
    a.extract()
    title = li.get_text(" ", strip=True)
    title = title.replace("[", r"\[").replace("]", r"\]")
    lines.append(f"* {title} [REDEEM OFFER]({url})")


data = "\n".join(lines)

with open("courses.txt", "w", encoding="utf-8") as filp:
    filp.write(data)

print("--- Scraper Hit Verification ---")
matches = [line for line in lines if PATTERN.search(line)]
if matches:
    for m in matches:
        print(f"Match found: {m.strip()}")
else:
    print("No match found")
