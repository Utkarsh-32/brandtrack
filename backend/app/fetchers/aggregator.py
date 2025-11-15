import datetime
from app.models import Brand, Mention
from app.fetchers.newsapi_fetcher import fetch_news_for_brand
from app.fetchers.reddit_fetcher import fetch_reddit_for_brand
from app.fetchers.rss_fetcher import fetch_rss_for_brand
from app.utils.alerts import detect_spike

def _safe_iso(dt):
    if isinstance(dt, str):
        return dt
    try:
        return dt.isoformat()
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

def ingest_item(brand_obj, item):
    url = item.get("url") or ""
    text = item.get("text") or ""
    if url:
        existing = Mention.objects.filter(brand=brand_obj, url=url).first()
        if existing:
            return
    else:
        if Mention.objects.filter(brand=brand_obj, text__iexact=text).exists():
            return
    pub = item.get("published_at")
    try:
        from dateutil import parser
        published_at = parser.isoparse(pub) if pub else datetime.datetime.now(datetime.timezone.utc)
    except Exception:
        try:
            published_at = datetime.datetime.fromisoformat(pub)
        except Exception:
            published_at = datetime.datetime.now(datetime.timezone.utc)
    Mention.objects.create(
        brand=brand_obj,
        source=item.get("source","agg"),
        author=item.get("author"),
        text=text,
        url=url or "",
        published_at=published_at,
        sentiment=item.get("sentiment","neutral"),
        sentiment_score=item.get("sentiment_score", 0.0)
    )

def fetch_and_ingest_for_brand(brand_obj):
    brand_name = brand_obj.name
    try:
        news = fetch_news_for_brand(brand_name, limit=10) or []
    except Exception as e:
        print("newsapi error", e); news = []
    try:
        reddit = fetch_reddit_for_brand(brand_name, limit=10) or []
    except Exception as e:
        print("reddit error", e); reddit = []
    try:
        rss = fetch_rss_for_brand(brand_name, limit=10) or []
    except Exception as e:
        print("rss error", e); rss = []
    try:
        detect_spike(brand_obj)
    except Exception as e:
        print("alert detect error", e)

    combined = []
    for it in news:
        combined.append(it)
    for it in reddit:
        combined.append(it)
    for it in rss:
        combined.append(it)

    for it in combined:
        try:
            ingest_item(brand_obj, it)
        except Exception as e:
            print("ingest_item error", e)
