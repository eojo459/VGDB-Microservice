import uuid
from django.db import models

class Games(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    rawg_id = models.IntegerField(unique=True)
    bg_image = models.CharField(max_length=255, null=True, blank=True)
    tba = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    rating = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    rating_top = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    ratings_count = models.IntegerField(default=0)
    reviews_text_count = models.IntegerField(default=0)
    released = models.DateField(null=True, blank=True)
    metacritic = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    playtime = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    esrb_rating = models.CharField(max_length=30, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    platforms = models.ManyToManyField('platforms.Platforms', blank=True)
    requirements = models.ManyToManyField('requirements.Requirements', blank=True)
    archived = models.BooleanField(default=False)