import django.http
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



# Create your views here.




@api_view(['GET','POST'])
def list_movie(req: django.http.HttpRequest):
    # Request

    """
    optional page_number: default 0
    optional count: default 5
    order by: release_date, rating, updated_on
    optional domain: <domain is for uniquely identify user, constant unique token>
    """

    # Response

    """
    page_number
    count: default value: 3, or from request
    previous: /movie/?p_no=<page_number-1>&count=<count>
    next: /movie/?p_no=<page_number>&count=<count>
    movies
        get the list of movies by request filters
        default order by: release_date
    """
    if req.method == 'GET':
        Movies = Movie.objects.all()
        serializer = MovieSerializer(Movies, many = True)
        return django.http.JsonResponse({'Movie Details':serializer.data}, status=200)

    if req.method == 'POST':
        serializer = MovieSerializer(Movies, many = True)
        if serializer.is_valid():
            serializer.save()
            return django.http.JsonResponse({serializer.data}, status=status.HTTP_201_CREATED)




@api_view(['GET','POST'])
def add_movie(req: django.http.HttpRequest):

    # Request
    """
    get from request body
    title, release_date, poster, director, description, rating, review_count
    """

    """
    Create a row in Movie model
    """
    try:
        Movies = Movie.objects.get()
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == 'GET':
        serializer = MovieSerializer(Movie)
        return Response(serializer.data)

    elif req.method == 'PUT':
        serializer = MovieSerializer(Movies, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    elif req.method == 'DELETE':
        Movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    return django.http.JsonResponse("{redirect to movie page}", status=200)


def add_review(req: django.http.HttpRequest):
    # Request
    """
    movie_id:
    title:
    optional description:
    reviewer: token
    optional rating
    """

    """
    Check if movie_id present or not
    Create a row in Review Model
    """


    return django.http.JsonResponse("redirect to movie page", status=200)


# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
