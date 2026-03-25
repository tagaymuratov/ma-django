from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
  path("register_for_event/<int:event_id>/", views.register_for_event, name="register_for_event"),
  path("event/<int:event_id>/attend/<int:user_id>/", views.mark_attendance, name="mark_attendance"),
]
