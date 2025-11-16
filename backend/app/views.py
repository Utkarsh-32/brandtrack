from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Brand, Mention, Alert
from .serializers import BrandSerializer, MentionSerializer, AlertSerializer
from django.db.models import Count
from django.utils import timezone
from rest_framework import generics

class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        obj, _ = Brand.objects.get_or_create(name=name)
        from app.fetchers.aggregator import fetch_and_ingest_for_brand
        try:
            fetch_and_ingest_for_brand(obj)
        except Exception as e:
            print("Auto-ingest failed:", e)
        return Response(BrandSerializer(obj).data)

class MentionsView(APIView):
    def get(self, request):
        brand = request.query_params.get("brand")
        if not brand:
            return Response({"error": "brand required"}, status=400)
        b = Brand.objects.filter(name=brand).first()
        if not b:
            return Response([])
        mentions = Mention.objects.filter(brand=b).order_by("-published_at")[:200]
        return Response(MentionSerializer(mentions, many=True).data)

class SummaryView(APIView):
    def get(self, request):
        brand = request.query_params.get("brand")
        if not brand:
            return Response({"error": "brand required"}, status=400)
        b = Brand.objects.filter(name=brand).first()
        if not b:
            return Response({})

        now = timezone.now()
        two_hours = now - timezone.timedelta(days=7)
        mentions = Mention.objects.filter(brand=b)

        buckets = {}
        for m in mentions:
            minute_key = m.published_at.replace(second=0, microsecond=0).isoformat()
            buckets[minute_key] = buckets.get(minute_key, 0) + 1
        sentiment_counts = list(
            mentions.values("sentiment").annotate(count=Count("id"))
        )

        top_mentions = Mention.objects.filter(brand=b).order_by("-published_at")[:10]
        alerts = Alert.objects.filter(brand=b, resolved=False).order_by("-detected_at")[:10]

        return Response({
            "buckets": buckets,
            "sentiment": sentiment_counts,
            "top_mentions": MentionSerializer(top_mentions, many=True).data,
            "alerts": AlertSerializer(alerts, many=True).data
        })