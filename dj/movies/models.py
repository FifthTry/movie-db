from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=1024)
    release_date = models.DateField()
    poster = models.URLField(max_length=1024)
    director = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=1024)
    description = models.TextField()
    reviewer = models.CharField(max_length=1024)
    # This null because user may not give rating
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)])
    created_on = models.DateTimeField(auto_now_add=True)
