import feedparser
import datetime
from app.utils.sentiment import analyze_sentiment

def fetch_rss_for_brand(brand_name, limit=10):
    feeds = [
        f"https://news.google.com/rss/search?q={brand_name}&hl=en-US&gl=US&ceid=US:en",
    ]
    items = []
    for feed_url in feeds:
        try:
            parsed = feedparser.parse(feed_url)
            for e in parsed.entries[:limit]:
                published = None
                if hasattr(e, 'published'):
                    try:
                        pp = e.get("published_parsed")
                        published = datetime.datetime(*pp[:6], tzinfo=datetime.timezone.utc)
                    except Exception:
                        published = datetime.datetime.now(datetime.timezone.utc)
                else:
                    published = datetime.datetime.now(datetime.timezone.utc)
                title = e.get("title") or ""
                summary = e.get("summary") or ""
                text = f"{str(title)} {str(summary)}".strip()
                score, label = analyze_sentiment(text)
                items.append({
                    "url": e.get("link", ""),
                    "author": e.get("author", ""),
                    "text": text,
                    "published_at": published.isoformat(),
                    "sentiment": label,
                    "sentiment_score": score,
                    "source": "rss"
                })
        except Exception as ex:
            print("RSS fetch error", feed_url, ex)
    
    return items