import uuid
from django.db import models

class Genres(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    rawg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    games_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
