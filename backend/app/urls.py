from django.urls import path
from .views import BrandListCreateView, MentionsView, SummaryView

urlpatterns = [
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("mentions/", MentionsView.as_view()),
    path("summary/", SummaryView.as_view())
]