from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title',  'release_date', 'poster', 'director', 'description', 'created_on', 'updated_on']

