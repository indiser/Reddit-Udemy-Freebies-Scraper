# Reddit Udemy Freebies Scraper

A Python-based web scraper that monitors Reddit's r/udemyfreeebies subreddit to automatically detect and notify you about **"100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu"** when it becomes available for free.

## Overview

This project scrapes the r/udemyfreeebies subreddit using Reddit's JSON API and searches for posts matching specific course patterns. When a match is found, it displays the post details including the title and direct link.

> ⚠️ **Important:** Reddit's unauthenticated `.json` API is no longer publicly accessible — it returns a login wall or error for anonymous requests. This scraper requires you to provide your own Reddit session cookies via a `cookies.json` file (see setup below).

## Features

✅ **Authenticated Scraping** - Uses your Reddit session cookies to bypass the login wall  
✅ **TLS Fingerprint Spoofing** - Uses `curl_cffi` to impersonate a real Chrome browser  
✅ **Flexible Pattern Matching** - Detects multiple variations of course names and instructor names  
✅ **Case-Insensitive Search** - Matches regardless of text case  
✅ **Error Handling** - Gracefully handles rate limiting and connection errors  
✅ **Formatted Output** - Clean, easy-to-read match notifications

## Files

| File | Purpose |
|------|---------|
| `main.py` | Main scraper script with real-time verification |
| `one_time.py` | One-time data collection script (legacy) |
| `cookies.json` | Your Reddit session cookies (required — see setup below) |
| `courses.txt` | Output file storing course data |

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- A Reddit account (free)
- [Cookie Editor](https://cookie-editor.com/) browser extension

### Dependencies

Install required packages:

```bash
pip install curl_cffi
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

## Cookie Setup (Required)

Reddit blocked unauthenticated access to the `.json` API. You must supply your own session cookies.

1. Install the **[Cookie Editor](https://cookie-editor.com/)** extension for your browser (available for Chrome and Firefox)
2. Log in to [reddit.com](https://www.reddit.com) in your browser
3. Navigate to [r/udemyfreeebies](https://www.reddit.com/r/udemyfreeebies/)
4. Click the Cookie Editor extension icon
5. Click **Export → Export as JSON**
6. Save the exported content as `cookies.json` in the project root directory (replacing the existing placeholder file)

> ⚠️ Cookies expire periodically. If you get a `403` or login-wall response, repeat the export steps above to refresh `cookies.json`.

## Usage

### Run the Main Scraper

```bash
python main.py
```

**Output Example:**
```
--- Scraper Hit Verification ---
Scraping https://www.reddit.com/r/udemyfreeebies/.json?limit=10...

• [Course Title 1]
• [Course Title 2]

========================================
🔥 MATCH FOUND!
Title: 100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu
Link: https://www.udemy.com/course/...
========================================
```

### Run One-Time Collection

```bash
python one_time.py
```

Scrapes the subreddit and saves course data to `courses.txt` for manual filtering.

## How It Works

1. **Loads Cookies** - Reads `cookies.json` and injects them into the session
2. **Fetches Posts** - Connects to Reddit's JSON API as an authenticated browser session
3. **Parses Data** - Extracts post titles and body text
4. **Pattern Matching** - Uses regex to search for matching course names
5. **Displays Results** - Prints matched posts with links

### Pattern Matching Logic

```
✓ "100 Days of Code" + "Angela Yu" (in any order)
✓ "100 Days of Code: The Complete Python Pro Bootcamp"
```

## Technical Details

### Regex Pattern

```python
PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"              # Course ... Instructor
    r"(angela.*yu.*100.*days.*code)|"              # Instructor ... Course
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Full Title
    re.IGNORECASE
)
```

### Why `curl_cffi`?

Reddit detects and blocks standard `requests` library calls based on TLS fingerprinting. `curl_cffi` impersonates a real Chrome browser at the TLS level, making requests indistinguishable from a normal browser visit.

### API Endpoint

- **URL**: `https://www.reddit.com/r/udemyfreeebies/.json?limit=10`
- **Auth**: Session cookies from `cookies.json`
- **Rate Limit**: ~60 requests/minute

## Error Handling

- **403 / Login wall** - Cookies are missing, expired, or invalid — re-export from Cookie Editor
- **429 Status Code** - Rate limited by Reddit — wait before retrying
- **Connection Errors** - Network failures
- **Invalid JSON** - Malformed API responses

## Customization

### Change Target Course

Edit the `PATTERN` variable in `main.py`:

```python
PATTERN = re.compile(r"your.*course.*name.*here", re.IGNORECASE)
```

### Adjust Search Limit

```python
limit = 25  # top of main.py
```

### Add Email Notifications

```python
if PATTERN.search(full_text):
    send_email_notification(title, url)  # add your email logic
```

## Limitations

⚠️ **Cookie Expiry** - Reddit session cookies expire; you'll need to re-export periodically  
⚠️ **Rate Limiting** - Reddit allows ~60 requests/minute  
⚠️ **Subreddit Availability** - Relies on r/udemyfreeebies being active  
⚠️ **Manual Monitoring** - Doesn't auto-monitor periodically

## Future Enhancements

- [ ] Scheduled background monitoring using `schedule` library
- [ ] Email/Discord notifications on match found
- [ ] Auto cookie refresh via browser automation
- [ ] Multiple course tracking

## Dependencies

- **curl_cffi** - HTTP library with Chrome TLS fingerprint impersonation

## License

This project is for educational purposes. Ensure compliance with Reddit's Terms of Service and Udemy's policies.

## Disclaimer

This tool is provided as-is. The author is not responsible for:
- Account bans due to excessive API requests
- Missed course opportunities
- Changes to Reddit/Udemy APIs
- Cookie expiry causing missed results

## Contact & Support

For issues, ensure you have:
- ✓ Latest Python version installed
- ✓ `curl_cffi` installed (`pip install curl_cffi`)
- ✓ Fresh `cookies.json` exported from Cookie Editor
- ✓ Valid internet connection

---

**Last Updated:** September 2026
**Status:** ✅ Active & Maintained
