import os
import json
import django
import datetime
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Brand, Mention

with open("demo_data/demo_mentions.json") as f:
    items = json.load(f)

for item in items:
    brand, _ = Brand.objects.get_or_create(name=item["brand"])

    Mention.objects.create(
        brand=brand,
        source=item["source"],
        author=item["author"],
        text=item["text"],
        url=item["url"],
        published_at=datetime.datetime.fromisoformat(item["published_at"]),
        sentiment=item["sentiment"],
        sentiment_score=0.0
    )

print("Loaded demo data into DB!")