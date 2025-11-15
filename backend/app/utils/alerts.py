from django.utils import timezone
from app.models import Mention, Alert
import statistics

def detect_spike(brand_obj, window_minutes=10, baseline_minutes=120, z_thresh=2.0):
    now = timezone.now()
    window_start = now - timezone.timedelta(minutes=window_minutes)
    baseline_start = now - timezone.timedelta(minutes=baseline_minutes)

    counts = []
    for m in range(baseline_minutes // window_minutes):
        s = baseline_start + timezone.timedelta(minutes=m*window_minutes)
        e = s + timezone.timedelta(minutes=window_minutes)
        c = Mention.objects.filter(brand=brand_obj, published_at__gte=s, published_at__lt=e).count()
        counts.append(c)

    if not counts or len(counts) < 2:
        return None

    mean = statistics.mean(counts)
    stdev = statistics.pstdev(counts) if statistics.pstdev(counts) > 0 else 0.0

    recent_count = Mention.objects.filter(brand=brand_obj, published_at__gte=window_start).count()

    
    if stdev == 0:
        if recent_count > mean * 3 and recent_count >= 5:
            msg = f"Spike: {recent_count} mentions in last {window_minutes} min (baseline {mean:.1f})"
            a, created = Alert.objects.get_or_create(brand=brand_obj, type="Spike", message=msg)
            return a
        return None

    z = (recent_count - mean) / stdev
    if z >= z_thresh and recent_count >= 5:
        msg = f"Spike: {recent_count} mentions in last {window_minutes} min (z={z:.1f})"
        a, created = Alert.objects.get_or_create(brand=brand_obj, type="Spike", message=msg)
        return a
    return None
