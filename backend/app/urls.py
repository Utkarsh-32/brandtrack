from django.urls import path
from .views import CreateBrand, MentionsView, SummaryView

urlpatterns = [
    path("brands/", CreateBrand.as_view()),
    path("mentions/", MentionsView.as_view()),
    path("summary/", SummaryView.as_view())
]