from django.urls import path

from . import views

app_name = "games"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.ScoresView.as_view(), name="scores"),
    path("sms/", views.process_sms, name="sms"),
]
