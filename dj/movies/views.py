import math

import django.http
from .models import Movie, Review
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .forms import SearchForm, ReviewForm

# from django.core.paginator import Paginator


# Create your views here.

# Create your views here.


@csrf_exempt
def list_movie(req: django.http.HttpRequest):
    # Request

    """
    optional page_number: default 0
    optional count: default 5
    order by: release_date, rating, updated_on
    optional domain: <domain is for uniquely identify user, constant unique token>
    """

    items = int(req.GET.get("items", 8))
    total_movies = 0
    page_number = req.GET.get("p_no", 1)
    p_number = int(page_number)
    """
    Pagination Logic
    E.g.: 10 items at every page
    1: 1 10
    2: 11 20
    3: 21 30
    
    st = (pno - 1) * items + 1 to
    end = pno * items
    """
    all_movies = Movie.objects.all()
    for i in all_movies:
        total_movies += 1

    last_pno = math.ceil(total_movies / 8)
    movie_list = Movie.objects.all()[(p_number - 1) * items : p_number * items]
    list_of_top_movies = []

    for movie in movie_list:
        rating = give_rating(movie.id)
        item = {
            "title": movie.title,
            "url": f"-/movie-db/movie/?id={movie.id}",
            "average": str(rating[0]),
            "total_reviews": str(rating[1]),
            "release_date": str(movie.release_date),
            "poster": {"light": movie.poster, "dark": movie.poster},
            "director": movie.director,
            "description": movie.description,
        }
        list_of_top_movies.append(item)

    if p_number - 1 > 0:
        previous_page_number = p_number - 1
    else:
        previous_page_number = last_pno

    if p_number + 1 > last_pno:
        next_page_number = 1

    else:
        next_page_number = p_number+1

    return django.http.JsonResponse(
        {
            "p_no": p_number,
            "next_pno": p_number + 1,
            "previous_pno": previous_page_number,
            "last_pno": last_pno,
            "first": f"/-/movie-db/?p_no={1}&items={items}",
            "next": f"/-/movie-db/movies/?p_no={next_page_number}&items={items}",
            "previous": f"/-/movie-db/movies/?p_no={previous_page_number}&items={items}",
            "movies": list_of_top_movies,
        },
        status=200,
        safe=False,
    )


@csrf_exempt
def search_movie(req: django.http.HttpRequest):

    body = json.loads(req.body.decode("utf-8"))
    target_movie_name = body["title"]

    form = SearchForm(json.loads(req.body.decode("utf-8")))

    if not form.is_valid():
        # TODO: with helper this would look like: `return ftd_django.form_error(form)`
        # Note: we are returning status 200 because if we return say 400, browser
        #       will show a popup saying "Failed to load resource". This is not
        #       what we want.
        return django.http.JsonResponse({"errors": form.errors})

    return django.http.JsonResponse(
        {"redirect": "/search/?search_movie=" + str(target_movie_name)}, status=200
    )


@csrf_exempt
def search_page(req: django.http.HttpRequest):
    search_for = req.GET.get("movie", None)
    searched_movie_list = Movie.objects.filter(title__startswith=search_for).order_by(
        "-updated_on"
    )

    list_of_searched_movies = []
    for movie in searched_movie_list:
        rating = give_rating(movie.id)
        item = {
            "title": movie.title,
            "url": "movie/?id=" + str(movie.id),
            "average": str(rating[0]),
            "total_reviews": str(rating[1]),
            "poster": {"light": movie.poster, "dark": movie.poster},
        }
        list_of_searched_movies.append(item)

    return django.http.JsonResponse(
        {
            "movies": list_of_searched_movies,
        },
        status=200,
        safe=False,
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

    return django.http.HttpResponseRedirect("/movie/?id=" + str(movie.id))


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
    movie_get_id = req.GET.get("id")
    movie_id = int(movie_get_id.rstrip("/"))
    try:
        movie = Movie.objects.get(id=movie_id)
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


"""
curl -X GET http://127.0.0.1:8001/movie/
"""


@csrf_exempt
def add_review(req: django.http.HttpRequest):
    body = json.loads(req.body.decode("utf-8"))
    movie_get_id = body["id"]
    movie_id = int(movie_get_id.rstrip("/"))

    form = ReviewForm(json.loads(req.body.decode("utf-8")))

    if not form.is_valid():
        # TODO: with helper this would look like: `return ftd_django.form_error(form)`
        # Note: we are returning status 200 because if we return say 400, browser
        #       will show a popup saying "Failed to load resource". This is not
        #       what we want.
        return django.http.JsonResponse({"errors": form.errors})

    name_set = set()
    # Request
    """
    movie_id, title, optional description, reviewer: token, optional rating
    """
    if req.method == "GET":
        return django.http.HttpResponse("Wrong Method GET", status=405)

    try:
        movie = Movie.objects.get(id=movie_id)

    except Exception as e:
        print(e)
        # TODO: Redirect to error page with 404 error
        return django.http.HttpResponse("redirect to movie page", status=404)

    Review.objects.create(
        movie=movie,
        title=body["title"],
        description=body.get("description"),
        reviewer=body["reviewer"],
        rating=body["rating"],
    )

    # TODO: restrict invalid ratings
    return django.http.HttpResponseRedirect("/movie/?id=" + str(movie_id))
    # TODO: redirect to movie page
    # return django.http.JsonResponse(
    #     {
    #         "redirect": ,
    #         "other": {"review": review.id, "movie": movie.id}
    #     },
    #     status=200,
    # )


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


def give_rating(id):
    count_reviews = 0
    total = 0
    try:
        reviews = Review.objects.filter(movie__pk=id)
        for review in reviews:
            if review.rating <= 10 or review.rating >= 0:
                count_reviews += 1
                total += review.rating

        if count_reviews == 0:
            average_rating = "Nil"
            count_reviews = "No"
        else:
            average_rating = round(total / count_reviews, 2)
            if average_rating > 10:
                average_rating = 10
            elif average_rating < 0:
                average_rating = 0

    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": err,
            },
            status=404,
        )

    return (average_rating, count_reviews)


def get_ratings(req: django.http.HttpRequest):
    movie_get_id = req.GET.get("id")
    movie_id = int(movie_get_id.rstrip("/"))
    count_reviews = 0
    total = 0
    try:
        reviews = Review.objects.filter(movie__pk=movie_id)
        for review in reviews:
            count_reviews += 1
            total += review.rating

        if count_reviews == 0:
            count_reviews = "No "
            average_rating = "Nil"
        else:
            average_rating = round(total / count_reviews, 2)

            if average_rating > 10:
                average_rating = 10
            elif average_rating < 0:
                average_rating = 0

        return django.http.JsonResponse(
            {"average": str(average_rating), "count_reviews": str(count_reviews)},
            status=200,
            safe=False,
        )

    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": err,
            },
            status=404,
        )


@csrf_exempt
def get_review(req: django.http.HttpRequest):
    movie_get_id = req.GET.get("id")
    movie_id = int(movie_get_id.rstrip("/"))
    print(f"insdie getting the actual review {movie_id}")
    global average
    global count_reviews
    total = 0
    try:
        reviews = Review.objects.filter(movie__pk=movie_id)
        name_set = set()
        filtered_reviews = []
        for review in reviews:
            item = {
                "title": review.title,
                "reviewer_name": review.reviewer,
                "rating": str(review.rating),
                "description": review.description,
            }
            filtered_reviews.append(item)

        return django.http.JsonResponse(filtered_reviews, status=200, safe=False)

    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": err,
            },
            status=404,
        )


# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
