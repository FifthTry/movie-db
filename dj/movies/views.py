import django.http
from .models import Movie, Review
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

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
    items = req.GET.get("items", 10)
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
    movies = Movie.objects.all()[
             (page_number - 1)*items + 1: page_number * items]

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

    d = {
        "name": "Aditi Rai",
        "p_no": page_number,
        "items": items,
        "movies": serializers.serialize('json', movies)
    }
    return django.http.JsonResponse(d, status=200)


@csrf_exempt
def add_movie(req: django.http.HttpRequest):

    if req.method == "GET":
        return django.http.HttpResponse("Wrong Method GET", status=405)

    body = json.loads(req.body.decode('utf-8'))
    movie = Movie.objects.create(
        title=body['title'], release_date=body['release_date'],
        poster=body['poster'], director=body['director'],
        description=body.get('description')
    )

    print(movie)
    # TODO: redirect to movie page
    return django.http.JsonResponse({"movie": movie.id}, status=200)

"""
curl -X POST http://127.0.0.1:8001/add-movie/ \
--data-raw '{
    "title": "Movie Title", 
    "release_date": "2022-12-10", 
    "poster": "M Poster", 
    "director": "Movie Director"
}'
"""


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
