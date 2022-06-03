from django.urls import path

from app.views import FirstTask, SecondTask

urlpatterns = [
    path("domain/", FirstTask.as_view()),
    path("statistics/", SecondTask.as_view())
]

app_name = "app"
