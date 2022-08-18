from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=1024)
    release_date = models.DateField()
    poster = models.CharField(max_length=1024)
    director = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)


class Review(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField()
    reviewer = models.CharField(max_length=1024)
    # This null because user may not give rating
    rating = models.IntegerField(null=True)
