from django.db import models

# Create your models here.


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024)
    release_date = models.DateField()
    poster = models.URLField(max_length=1024)
    director = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024)
    description = models.TextField()
    reviewer = models.CharField(max_length=1024)
    # This null because user may not give rating
    rating = models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
