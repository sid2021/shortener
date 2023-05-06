from django.db import models

from config.mixins import TimeStampedModel, UUIDPrimaryKeyAbstractModel


class URL(UUIDPrimaryKeyAbstractModel, TimeStampedModel):
    """Model storing information on shortened URLs."""

    full_url = models.URLField(unique=True)
    short_url = models.URLField(unique=True)
    hits = models.BigIntegerField(default=1)

    def __str__(self):
        return f"URL {self.full_url}"
