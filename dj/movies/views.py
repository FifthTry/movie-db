import django.http
from .models import Movie, Review
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import requests
from django.shortcuts import render

# Create your views here.


def list_movie(req: django.http.HttpRequest):
    # Request

    """
    optional page_number: default 0
    optional count: default 5
    order by: release_date, rating, updated_on
    optional domain: <domain is for uniquely identify user, constant unique token>
    """
    page_number = req.GET.get("p_no", 1)
    items = req.GET.get("items", 50)
    """
    Pagination Logic
    E.g.: 10 items at every page
    1: 1 10
    2: 11 20
    3: 21 30
    
    st = (pno - 1) * items + 1 to
    end = pno * items
    """

    order_by = req.GET.get("p_no", 0)
    movies = Movie.objects.all()[(page_number - 1) * items + 1: page_number * items]

    return django.http.JsonResponse(
        {
            "p_no": page_number,
            # TODO: Next And Previous both are optional
            "next": "/movies/p_no=1&items=10",
            "previous": "/movies/p_no=1&items=10",
            "items": items,
            "movies": json.loads(serializers.serialize("json", movies)),
        },
        status=200,
    )


@csrf_exempt
def add_movie(request: django.http.HttpRequest):
    all_movies = {}

    if request.method == "GET":
        return django.http.HttpResponse("Wrong Method GET", status=405)

    body = json.loads(request.body.decode("utf-8"))
    movie = Movie.objects.create(
        title=body["title"],
        release_date=body["release_date"],
        poster=body["poster"],
        director=body["director"],
        description=body.get("description"),
    )




    movie.save()

    all_movies = Movie.objects.all().order_by('release_date')

    print(Movie)

    #for i in all_movies:
       # print(i)
    # TODO: redirect to movie page
    return django.http.JsonResponse({"movie": movie.title}, status=200)


"""
curl -X POST http://127.0.0.1:8001/add-movie/ \
--data-raw '{
    "title": "Movie Title", 
    "release_date": "2022-12-10", 
    "poster": "M Poster", 
    "director": "Movie Director"
}'
"""


@csrf_exempt
def get_movie(req: django.http.HttpRequest):

    movie = req.GET.get("title")

    return django.http.JsonResponse(
        {
            "title": movie.title,
            "release_date": movie.release_date,
            "poster": movie.poster,
            "director": movie.director,
            "description": movie.description,
        },
        status=200,
    )


"""
curl -X GET http://127.0.0.1:8001/add-movie/ \
--data-raw '{
    "title": "Movie Title", 
    "release_date": "2022-12-10", 
    "poster": "M Poster", 
    "director": "Movie Director"
}'
"""


all_reviews = {}


@csrf_exempt
def add_review(req: django.http.HttpRequest):
    review_dict = {}
    # Request
    """
    movie_id, title, optional description, reviewer: token, optional rating
    """
    if req.method == "GET":
        return django.http.HttpResponse("Wrong Method GET", status=405)

    body = json.loads(req.body.decode("utf-8"))
    try:
        movie = Movie.objects.get(id=body["movie"])
    except Exception as e:
        print(e)
        # TODO: Redirect to error page with 404 error
        return django.http.HttpResponse("redirect to movie page", status=404)

    review = Review.objects.create(
        movie=movie,
        title=body["title"],
        description=body.get("description"),
        reviewer=body["reviewer"],
        rating=body["rating"],
    )

    reviews = Review.objects.all()



    review.save()

    review_dict = Review.objects.all().order_by('title')
    all_reviews = review_dict


    # TODO: redirect to movie page
    return django.http.JsonResponse(
        {
            "reviews": json.loads(serializers.serialize("json", review_dict))
        },
        status=200)

"""
curl -X POST http://127.0.0.1:8001/add-review/ \
--data-raw '{
    "movie": 1, 
    "title": "Review Title", 
    "description": "Review Description", 
    "reviewer": "Movie Reviewer",
    "rating": 8
}'
"""

@csrf_exempt
def list_review(req: django.http.HttpRequest):

    # Request
    no_of_reviews = req.GET.get("No_of_reviews", 100)
    reviews = Review.objects.all()

    return django.http.JsonResponse(
        {
            "No_of_reviews": no_of_reviews,
            "reviews": json.loads(serializers.serialize("json", reviews)),
        },
        status=200,
    )


@csrf_exempt
def get_movie(request, title):

    body = json.loads(request.body.decode("utf-8"))

    try:
        movie = Movie.objects.get(title=body["movie"])
    except Exception as e:
        print(e)
        # TODO: Redirect to error page with 404 error
        return django.http.HttpResponse("redirect to movie page", status=404)

    movie = Movie.objects.get(id=title)


    print(movie)
    print(Movie)
    # TODO: redirect to movie page
    return django.http.JsonResponse({"movie": movie.title}, status=200)

"""
curl -X GET http://127.0.0.1:8001/title/ \
--data-raw '{
    "title": "Movie Title",
}'
"""

# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
