import uuid
from django.db import models

class Publishers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)  
    rawg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    games_count = models.IntegerField(default=0)
    background_image = models.CharField(max_length=255, null=True, blank=True)