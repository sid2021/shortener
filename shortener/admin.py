from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):
    """ModelAdmin class for the URL model."""

    list_display = ("full_url", "short_url", "hits", "created", "modified")


admin.site.register(URL, URLAdmin)
