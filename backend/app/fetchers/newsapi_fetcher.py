import os
import requests
import datetime
from app.models import Brand, Mention
from app.utils.sentiment import analyze_sentiment

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def fetch_news_for_brand(brand_name, limit=10):
    if not NEWS_API_KEY:
        return
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": brand_name,
        "apiKey": NEWS_API_KEY,
        "pagesize": limit,
        "sortBy": "publishedAt",
        "language": "en"
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    articles = data.get("articles", [])

    brand_obj = Brand.objects.filter(name=brand_name).first()
    if not brand_obj:
        return
    
    for art in articles:
        title = art.get("title") or ""
        desc = art.get("description") or ""
        text = f"{title} {desc}".strip()
        score, label = analyze_sentiment(text)
        published_at = art.get("publishedAt") or datetime.datetime.now(datetime.timezone.utc).isoformat()

        Mention.objects.get_or_create(
            brand=brand_obj,
            url=art.get("url"),
            defaults={
                "source": "newsapi",
                "author": art.get("source", {}).get("name"),
                "text": text,
                "published_at": published_at,
                "sentiment": label,
                "sentiment_score": score
            }
        )
    