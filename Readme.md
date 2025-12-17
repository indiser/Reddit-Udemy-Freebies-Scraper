# Reddit Udemy Freebies Scraper

A Python-based web scraper that monitors Reddit's r/udemyfreeebies subreddit to automatically detect and notify you about **"100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu"** when it becomes available for free.

## Overview

This project scrapes the r/udemyfreeebies subreddit using the Reddit JSON API and searches for posts matching specific course patterns. When a match is found, it displays the post details including the title and direct link.

## Features

✅ **Automated Reddit Scraping** - Fetches latest posts from r/udemyfreeebies  
✅ **Flexible Pattern Matching** - Detects multiple variations of course names and instructor names  
✅ **Case-Insensitive Search** - Matches regardless of text case  
✅ **Error Handling** - Gracefully handles rate limiting and connection errors  
✅ **User-Agent Headers** - Prevents blocking by Reddit's anti-bot measures  
✅ **Formatted Output** - Clean, easy-to-read match notifications

## Files

| File | Purpose |
|------|---------|
| `main.py` | Main scraper script with real-time verification |
| `one_time.py` | One-time data collection script (legacy) |
| `courses.txt` | Output file storing course data |
| `data.json` | JSON formatted course data (optional) |

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Dependencies

Install required packages:

```bash
pip install requests beautifulsoup4
```

## Usage

### Run the Main Scraper

```bash
python main.py
```

**Output Example:**
```
--- Scraper Hit Verification ---
Scraping https://www.reddit.com/r/udemyfreeebies/.json?limit=5...

========================================
🔥 MATCH FOUND!
Title: [100 Days of Code: The Complete Python Pro Bootcamp by Angela Yu]
Link: https://www.udemy.com/course/...
========================================
```

### Run One-Time Collection

```bash
python one_time.py
```

This script scrapes all available courses and saves them to `courses.txt` for filtering.

## How It Works

1. **Fetches Posts** - Connects to Reddit's JSON API endpoint
2. **Parses Data** - Extracts post titles and descriptions
3. **Pattern Matching** - Uses regex to search for matching course names
4. **Displays Results** - Prints matched posts with clickable links

### Pattern Matching Logic

The scraper searches for these variations (all case-insensitive):

```
✓ "100 Days of Code" + "Angela Yu" (in any order)
✓ "100 Days of Code: The Complete Python Pro Bootcamp"
✓ Both text and title variations
```

## Technical Details

### Regex Patterns Used

```python
PATTERN = re.compile(
    r"(100.*days.*code.*angela.*yu)|"              # Course ... Instructor
    r"(angela.*yu.*100.*days.*code)|"              # Instructor ... Course
    r"(100\s*days\s*of\s*code.*python\s*pro\s*bootcamp)", # Full Title
    re.IGNORECASE
)
```

### API Endpoint

- **URL**: `https://www.reddit.com/r/udemyfreeebies/.json`
- **Method**: GET
- **Rate Limit**: 60 requests/minute (with proper User-Agent)

## Error Handling

The script handles:
- **429 Status Code** - Rate limiting by Reddit (waits before retry)
- **Connection Errors** - Network failures
- **Invalid JSON** - Malformed API responses
- **Missing Fields** - Posts without expected data structure

## Customization

### Change Target Course

Edit the `PATTERN` variable in `main.py`:

```python
PATTERN = re.compile(
    r"your.*course.*name.*here",
    re.IGNORECASE
)
```

### Adjust Search Limit

Modify the URL in `main.py`:

```python
SUBREDDIT_URL = "https://www.reddit.com/r/udemyfreeebies/.json?limit=100"  # Get 100 latest posts
```

### Add Email Notifications

Extend the script to send emails when matches are found:

```python
if PATTERN.search(full_text):
    send_email_notification(title, url)  # Add your email logic
```

## Limitations

⚠️ **Rate Limiting** - Reddit allows ~60 requests/minute  
⚠️ **Subreddit Availability** - Relies on r/udemyfreeebies being active  
⚠️ **Course Availability** - Udemy courses may not always be free  
⚠️ **Manual Monitoring** - Currently doesn't auto-monitor periodically

## Future Enhancements

- [ ] Scheduled background monitoring using `schedule` library
- [ ] Email/Discord notifications on match found
- [ ] Database storage for historical data
- [ ] Web dashboard for viewing matches
- [ ] Multiple course tracking
- [ ] Price drop detection

## Dependencies

- **requests** - HTTP library for API calls
- **beautifulsoup4** - HTML parsing (optional, for content extraction)

## License

This project is for educational purposes. Ensure compliance with Reddit's Terms of Service and Udemy's policies.

## Disclaimer

This tool is provided as-is. The author is not responsible for:
- Account bans due to excessive API requests
- Missed course opportunities
- Changes to Reddit/Udemy APIs
- Course availability accuracy

## Contact & Support

For issues or questions, ensure you have:
- ✓ Latest Python version installed
- ✓ All dependencies installed (`pip install -r requirements.txt`)
- ✓ Valid internet connection
- ✓ Reddit is not blocked by your network

---

**Last Updated:** December 2025  
**Status:** ✅ Active & Maintained