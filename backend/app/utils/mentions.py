from django.utils import timezone
from app.models import Brand, Mention
from app.utils.sentiment import analyze_sentiment

def create_mention(brand_name, source, text, url=None, author=None, published_at=None):
    if published_at is None:
        published_at = timezone.now()
    
    brand, _ = Brand.objects.get_or_create(brand_name)
    score, label = analyze_sentiment(text)

    mention = Mention.objects.create(
        brand=brand,
        source=source,
        text=text,
        url=url,
        author=author,
        sentiment = label,
        sentiment_score=score,
        published_at=published_at
    )
    
    return mention