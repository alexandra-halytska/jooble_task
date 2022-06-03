from django.urls import path

from domains.views import DomainApi, Statistics

urlpatterns = [
    path("post_url/", DomainApi.as_view()),
    path("statistics/", Statistics.as_view())
]

app_name = "domains"
