from django.urls import include, path


urlpatterns = [
    path("", include("ecofem.urls")),
]

handler404 = "ecofem.views.custom_404"
handler500 = "ecofem.views.custom_500"
