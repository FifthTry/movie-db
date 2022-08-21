import django.http
from models import Movie, Review
import json

# Create your views here.


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

    d = {"name": "Aditi Rai"}
    return django.http.JsonResponse(d, status=200)


def add_movie(req: django.http.HttpRequest):
    body = json.loads(req.body.decode('utf-8'))
    movie = Movie.objects.create(
        title=body['title'], release_date=body['release_date'],
        poster=body['poster'], director=body['director'],
        description=body.get('description')
    )
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
    body = json.loads(req.body.decode('utf-8'))
    try:
        movie = Movie.objects.get(body["movie_id"])
    except Exception as e:
        print(e)
        # Redirect to error page with 404 error

    review = Review.objects.create(
        movie=movie, title=body["title"], descrption=body.get("description"),
        reviewer=body["reviewer"], rating=body["rating"]
    )
    return django.http.JsonResponse("redirect to movie page", status=200)


# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
