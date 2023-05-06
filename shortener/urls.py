from django.urls import path

from .views import GetFullUrl, GetShortUrl, ListUrls

urlpatterns = [
    path("get-short/", GetShortUrl.as_view(), name="get-short"),
    path("get-full/", GetFullUrl.as_view(), name="get-full"),
    path("get-urls/", ListUrls.as_view(), name="get-urls"),
]
