from django.urls import include, path, re_path

from ecofem import views


urlpatterns = [
    re_path(r"^admin(?:/.*)?$", views.custom_404, name="blocked_admin"),
    path("", include("ecofem.urls")),
]

handler404 = "ecofem.views.custom_404"
handler500 = "ecofem.views.custom_500"
