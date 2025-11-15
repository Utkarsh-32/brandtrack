import requests
import datetime
from app.utils.sentiment import analyze_sentiment

HEADERS = {"User-Agent": "brandtrack-hack/0.1 by demo"}

def fetch_reddit_for_brand(brand_name, limit=10):
    url = "https://www.reddit.com/search.json"
    params = {"q": brand_name, "sort": "new", "limit": limit}
    items = []
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        for child in data.get("data", {}).get("children", []):
            d = child.get("data", {})
            text = (d.get("title", "") + " " + (d.get("selftext") or "")).strip()
            published = datetime.datetime.fromtimestamp(d.get("created_utc")).isoformat()
            score, label = analyze_sentiment(text)
            items.append({
                "url": "https://reddit.com" + d.get("permalink", ""),
                "author": d.get("author"),
                "text": text,
                "published_at": published,
                "sentiment": label,
                "sentiment_score": score,
                "source": "reddit",
            })
    except Exception as ex:
        print("Reddit fetch error", ex)
    return items