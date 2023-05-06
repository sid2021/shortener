from typing import Dict

from rest_framework import serializers

from .models import URL


class URLSerializer(serializers.ModelSerializer):
    """Serializer for the URL model."""

    def create(self, validated_data: Dict) -> URL:
        """Create a new URL object using validate data."""
        return URL.objects.create(**validated_data)

    def update(self, instance: URL, validated_data: Dict) -> URL:
        """Update existing URL object incrementing hits counter."""
        instance.full_url = validated_data.get("full_url", instance.full_url)
        instance.short_url = validated_data.get("short_url", instance.short_url)
        instance.hits = validated_data.get("hits", instance.hits + 1)
        instance.save()
        return instance

    class Meta:
        model = URL
        fields = ["full_url", "short_url", "hits"]
