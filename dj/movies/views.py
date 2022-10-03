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
    items = req.GET.get("items", 8)
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
    movies = Movie.objects.all()[(page_number - 1) * items + 1 : page_number * items]

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
def add_movie(req: django.http.HttpRequest):

    if req.method == "GET":
        return django.http.HttpResponse("Wrong Method GET", status=405)

    body = json.loads(req.body.decode("utf-8"))
    movie = Movie.objects.create(
        title=body["title"],
        release_date=body["release_date"],
        poster=body["poster"],
        director=body["director"],
        description=body.get("description"),
    )

    print(movie)
    # TODO: redirect to movie page
    # from django.shortcuts import redirect
    # return redirect("/", permanent=True)
    return django.http.JsonResponse({"data": {"url": "/movie/?id="+str(movie.id)}}, status=200)


"""
curl -X POST http://127.0.0.1:8000/add-movie/ \
-H 'Content-Type: application/json' \
--data '{
    "title": "Movie Title", 
    "release_date": "2022-12-10", 
    "poster": "M Poster", 
    "director": "Movie Director"
}'
"""


@csrf_exempt
def get_movie(req: django.http.HttpRequest):

    movie_id = req.GET.get("id")
    print(movie_id)
    try:
        movie = Movie.objects.get(id=movie_id)
        print("Movie details", movie)
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
    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": "Movie with id not found",
            },
            status=404,
        )

    # from django.shortcuts import redirect

    # return redirect("https://www.google.com", permanent=True)


"""
curl -X GET http://127.0.0.1:8001/movie/
"""


@csrf_exempt
def add_review(req: django.http.HttpRequest):
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
    # TODO: redirect to movie page
    return django.http.JsonResponse(
        {"review": review.id, "movie": movie.id}, status=200
    )


"""
curl -X POST http://127.0.0.1:8001/add-review/ \
-H 'Content-Type: application/json' \
--data '{
    "movie": 1, 
    "title": "Review Title", 
    "description": "Review Description", 
    "reviewer": "Movie Reviewer",
    "rating": 8
}'
"""

@csrf_exempt
def get_review(req: django.http.HttpRequest):

    movie_id = req.GET.get("id")
    print(movie_id)
    try:
        review = Review.objects.get(id=movie_id)
        print("Review details", review)
        return django.http.JsonResponse(
            {
                "title": review.title,
                "reviewer": review.reviewer,
                "rating": review.rating,
                "description": review.description,
            },
            status=200,
        )
    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": "Movie with id not found",
            },
            status=404,
        )



# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
