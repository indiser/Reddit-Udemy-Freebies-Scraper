# Reddit Udemy Freebies Scraper

A Python scraper that monitors r/udemyfreeebies to detect when **"100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu"** is posted for free.

## Why RSS Instead of the JSON API?

Reddit's `.json` API endpoint is **completely dead for unauthenticated requests** — it returns a login wall regardless of headers or user-agent spoofing. Even with authentication, it's unreliable and heavily rate-limited.

This scraper uses Reddit's **RSS feed** (`.rss`) instead, which:
- Still returns structured post data
- Works with session cookie authentication via `curl_cffi`
- Is parsed cleanly using `feedparser` + `BeautifulSoup`

> ⚠️ The RSS feed also requires authentication. You must supply your Reddit session cookies via `cookies.json` (see setup below).

## Files

| File | Purpose |
|------|---------|
| `main.py` | Main scraper — scans latest posts and prints any matches |
| `one_time.py` | One-time script — finds the megathread and saves all courses to `courses.txt` |
| `cookies.json` | Your Reddit session cookies (required — see setup below) |
| `courses.txt` | Output file written by `one_time.py` |
| `requirements.txt` | Python dependencies |

## Installation

### Prerequisites
- Python 3.7+
- A Reddit account (free)
- [Cookie Editor](https://cookie-editor.com/) browser extension

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install curl_cffi feedparser beautifulsoup4
```

## Cookie Setup (Required)

Both scripts load `cookies.json` to authenticate with Reddit. Without valid cookies, the RSS feed returns a login wall.

1. Install the **[Cookie Editor](https://cookie-editor.com/)** extension (Chrome or Firefox)
2. Log in to [reddit.com](https://www.reddit.com)
3. Navigate to [r/udemyfreeebies](https://www.reddit.com/r/udemyfreeebies/)
4. Click the Cookie Editor extension icon
5. Click **Export → Export as JSON**
6. Save the file as `cookies.json` in the project root, replacing the existing placeholder

> ⚠️ Cookies expire periodically. If you get a `403` or empty feed, re-export from Cookie Editor.

## Usage

### `main.py` — Scan Latest Posts for a Match

Fetches the latest posts from the RSS feed and checks each one against the pattern.

```bash
python main.py
```

**Output Example:**
```
--- Scraper Hit Verification ---
Scraping https://www.reddit.com/r/udemyfreeebies/.rss?limit=10...

- Udemy Free Courses - June 2025
- 100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu

========================================
MATCH FOUND!
Title: 100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu
Link: https://www.udemy.com/course/100-days-of-code/
========================================
```

### `one_time.py` — Extract All Courses from the Megathread

Finds the pinned "Udemy Free Courses" megathread, parses all course links from the post body, and saves them to `courses.txt`.

```bash
python one_time.py
```

Output is written to `courses.txt` in markdown format:
```
# Udemy Free Courses - June 2025

* Course Name [REDEEM OFFER](https://udemy.com/...)
* ...
```

## How It Works

### `main.py`
1. Loads `cookies.json` and injects cookies into a `curl_cffi` session (impersonating Chrome 120)
2. Fetches `https://www.reddit.com/r/udemyfreeebies/.rss?limit=10`
3. Parses the Atom feed with `feedparser`
4. For each entry, strips HTML from the post body using `BeautifulSoup`
5. Runs the regex pattern against the title + body text
6. Prints any matches with their Udemy link

### `one_time.py`
1. Same cookie + session setup as `main.py`
2. Fetches the RSS feed and finds the entry titled "Udemy Free Courses"
3. Parses all `<li>` elements from the post HTML
4. Extracts course titles and Udemy URLs
5. Writes everything to `courses.txt`

## Pattern Matching

```python
PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"               # Course ... Instructor
    r"(angela.*yu.*100.*days.*code)|"               # Instructor ... Course
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)",  # Full title
    re.IGNORECASE
)
```

Matches any of:
- `"100 Days of Code"` + `"Angela Yu"` in any order
- `"100 Days of Code: The Complete Python Pro Bootcamp"` (no instructor needed)

## Technical Details

### Why `curl_cffi`?

Reddit blocks the standard `requests` library via TLS fingerprinting. `curl_cffi` impersonates Chrome 120 at the TLS level, making the request indistinguishable from a real browser.

### Feed Endpoint

- **URL**: `https://www.reddit.com/r/udemyfreeebies/.rss?limit=10`
- **Format**: Atom XML (parsed by `feedparser`)
- **Auth**: Session cookies from `cookies.json`

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `403` / login wall | Cookies missing, expired, or invalid | Re-export `cookies.json` from Cookie Editor |
| `429` | Rate limited by Reddit | Wait and retry |
| `CRITICAL FAILURE` | Network error or unexpected response | Check internet connection |
| Empty feed / no entries | Cookie issue or subreddit unavailable | Verify cookies are fresh |

## Customization

### Track a Different Course

Edit `PATTERN` in `main.py` or `one_time.py`:

```python
PATTERN = re.compile(r"your.*course.*name", re.IGNORECASE)
```

### Change the Post Limit

```python
limit = 25  # top of main.py
```

## Limitations

- **Cookie Expiry** — Reddit cookies expire; re-export periodically
- **Rate Limiting** — ~60 requests/minute
- **Manual Execution** — No built-in scheduler; run manually or via cron/Task Scheduler

## Future Enhancements

- [ ] Periodic auto-monitoring with `schedule`
- [ ] Email or Discord notification on match
- [ ] Auto cookie refresh via browser automation
- [ ] Track multiple courses simultaneously

## Dependencies

| Package | Purpose |
|---------|---------|
| `curl_cffi` | HTTP requests with Chrome TLS fingerprint impersonation |
| `feedparser` | Parses Reddit's Atom RSS feed |
| `beautifulsoup4` | Strips HTML from post body content |

## License

For educational purposes. Ensure compliance with Reddit's Terms of Service and Udemy's policies.

---

**Status:** ✅ Active — using RSS feed (`.json` API is dead)
