import random
import os
import json
import datetime

os.makedirs("demo_data", exist_ok=True)

BRANDS = ["YourBrand", "AcmeCorp", "HackX", "CoffeeDay"]

TEMPLATES = [
    "{brand} faces outage report from users",
    "Customers praise {brand}'s new feature rollout", 
    "{brand} gets mixed reactions after update",
    "Rumors about {brand} acquisition trending",
    "{brand} recieves backlash for pricing changes"
]

def random_time_within_last(hours=3):
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = datetime.timedelta(
        minutes = random.randint(0, hours * 60)
    )
    return (now - delta).isoformat()

def generate_data(n=300):
    items = []

    for _ in range(n):
        brand = random.choice(BRANDS)
        text = random.choice(TEMPLATES).format(brand=brand)
        sentiment = random.choice(["positive", "negative", "neutral"])

        item = {
            "brand": brand,
            "source": "demo",
            "author": "demo_user",
            "text": text,
            "url": "",
            "published_at": random_time_within_last(),
            "sentiment": sentiment
        }

        items.append(item)
    
    with open("demo_data/demo_mentions.json", "w") as f:
        json.dump(items, f, indent=2)

    print("demo_mentions.json generated!")

if __name__ == "__main__":
    generate_data()