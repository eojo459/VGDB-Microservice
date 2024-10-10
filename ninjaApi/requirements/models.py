import uuid
from django.db import models

class Requirements(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    platform = models.ManyToManyField('platforms.Platforms', blank=True, null=True)
    game = models.ManyToManyField('games.Games', blank=True, null=True, related_name='games')
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    minimum_requirements = models.TextField(blank=True, null=True)
    recommended_requirements = models.TextField(blank=True, null=True)