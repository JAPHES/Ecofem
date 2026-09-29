from django.urls import path

from . import views


app_name = "ecofem"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("innovation/", views.innovation, name="innovation"),
    path("impact/", views.impact, name="impact"),
    path("team/", views.team_list, name="team_list"),
    path("updates/", views.update_list, name="update_list"),
    path("updates/<slug:slug>/", views.update_detail, name="update_detail"),
    path("contact/", views.contact, name="contact"),
]
