import os
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from app.models import Brand
from app.fetchers.newsapi_fetcher import fetch_news_for_brand

def job_fetch_all_brands():
    print("Scheduler tick: fetching mentions...")

    brands = Brand.objects.all()

    for brand in brands:
        try:
            fetch_news_for_brand(brand.name)
        except Exception as e:
            print(f"Error fetching for {brand.name}: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_fetch_all_brands, "interval", seconds=60)
    scheduler.start()
    print("Scheduler started press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()