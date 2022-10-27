import math

import django.http
from .models import Movie, Review
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

current_page_number = 1
items_per_page = 8
last_pno = 3


# Create your views here.

@csrf_exempt
def list_movie(req: django.http.HttpRequest):
    # Request
    global current_page_number

    """
    optional page_number: default 0
    optional count: default 5
    order by: release_date, rating, updated_on
    optional domain: <domain is for uniquely identify user, constant unique token>
    """

    items = int(req.GET.get("items", 8))
    total_movies = 0
    page_number = req.GET.get("p_no", current_page_number)
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

    # order_by = req.GET.get("p_no", 0)
    movie_list = Movie.objects.all()[(p_number - 1) * items: p_number * items]

    list_of_top_movies = []

    for movie in movie_list:
        rating = give_rating(movie.id)
        item = {
            "title": movie.title,
            "url": "movie/?id=" + str(movie.id),
            "average": str(rating[0]),
            "total_reviews": str(rating[1]),
            "release_date": str(movie.release_date),
            "poster": {'light': movie.poster, 'dark': movie.poster},
            "director": movie.director,
            "description": movie.description,
        }
        list_of_top_movies.append(item)

    if p_number - 1 > 0:
        previous_page_number = p_number - 1
    else:
        previous_page_number = 1

    final_page_data = {
        "p_no": p_number,
        "next": f"api/movies/?p_no={p_number + 1}&items={items}",
        "previous": f"api/movies/?p_no={previous_page_number}&items={items}",
        "movies": list_of_top_movies,
    }

    return django.http.JsonResponse(
        final_page_data,
        status=200,
        safe=False,
    )


@csrf_exempt
def search_movie(req: django.http.HttpRequest):
    body = json.loads(req.body.decode("utf-8"))
    target_movie_name = body['movie']

    return django.http.JsonResponse({"data": {"url": "/search/?search_movie=" + str(target_movie_name)}}, status=200)


@csrf_exempt
def search_page(req: django.http.HttpRequest):
    search_for = req.GET.get("movie", None)
    searched_movie_list = Movie.objects.filter(title__startswith=search_for).order_by("-updated_on")

    list_of_searched_movies = []
    for movie in searched_movie_list:
        rating = give_rating(movie.id)
        item = {
            "title": movie.title,
            "url": "movie/?id=" + str(movie.id),
            "average": str(rating[0]),
            "total_reviews": str(rating[1]),
            "poster": {'light': movie.poster, 'dark': movie.poster},
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
def change_page(req: django.http.HttpRequest):
    # Request
    global current_page_number
    """
    optional page_number: default 0
    optional count: default 5
    order by: release_date, rating, updated_on
    optional domain: <domain is for uniquely identify user, constant unique token>
    """
    total_movies = 0
    all_movies = Movie.objects.all()
    for i in all_movies:
        total_movies += 1

    last_pno = math.ceil(total_movies / 8)
    body = json.loads(req.body.decode("utf-8"))
    items = int(req.GET.get("items", 8))

    total_movies = 0

    page_number = req.GET.get("p_no", current_page_number)
    p_number = int(page_number)

    mode = body.get("mode", "next")

    change_to_next = True if mode == "next" else False

    current_page_number = p_number
    if change_to_next:
        current_page_number = current_page_number + 1

        if current_page_number > last_pno:
            current_page_number = last_pno
    else:
        current_page_number = current_page_number - 1 if current_page_number - 1 > 0 else 1

    return django.http.JsonResponse(
        {
            "data": {"reload": True}

        },
        status=200,
        safe=False,
    )


@csrf_exempt
def page_details(req: django.http.HttpRequest):
    return django.http.JsonResponse(
        {
            "curr_pno": current_page_number,
            "no_items": items_per_page,
            "last_pno": last_pno
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

    # print(movie)
    # TODO: redirect to movie page
    # from django.shortcuts import redirect
    # return redirect("/", permanent=True)
    return django.http.JsonResponse({"data": {"url": "/movie/?id=" + str(movie.id)}}, status=200)


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

    # from django.shortcuts import redirect

    # return redirect("https://www.google.com", permanent=True)


"""
curl -X GET http://127.0.0.1:8001/movie/
"""


@csrf_exempt
def add_review(req: django.http.HttpRequest):
    body = json.loads(req.body.decode("utf-8"))
    movie_id = body["id"]
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

    norm_rating = int(body["rating"])

    if norm_rating > 10:
        norm_rating = 10

    elif norm_rating < 0:
        norm_rating = 0

    review = Review.objects.create(
        movie=movie,
        title=body["title"],
        description=body.get("description"),
        reviewer=body["reviewer"],
        rating=norm_rating,
    )




    # TODO: Checking one review per reviewer
    # reviews = Review.objects.filter(movie__pk=movie_id)
    # name_set = set()
    # for review in reviews:
    #     if (body["rating"]>10 or body["rating"]<0):
    #         return django.http.HttpResponse("Invalid rating, nigga", status=404)
    #     if review.reviewer not in name_set:
    #         name_set.add(review.reviewer)
    #     else:
    #         return django.http.HttpResponse("You have already reviewed the movie!", status=404)

    # TODO: restrict invalid ratings

    # TODO: redirect to movie page
    return django.http.JsonResponse(
        {
            "data": {"success": True,
                     "reload": True},
            "other": {"review": review.id, "movie": movie.id}
        },
        status=200,
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
    movie_id = req.GET.get("id")
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
            {
                "average": str(average_rating),
                "count_reviews": str(count_reviews)

            },
            status=200,
            safe=False
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
    movie_id = req.GET.get("id")
    global average
    global count_reviews
    total = 0
    try:
        reviews = Review.objects.filter(movie__pk=movie_id)
        name_set = set()
        filtered_reviews = []
        for review in reviews:
            item = {"title": review.title,
                    "reviewer_name": review.reviewer,
                    "rating": str(review.rating),
                    "description": review.description}
            filtered_reviews.append(item)

        return django.http.JsonResponse(
            filtered_reviews,
            status=200,
            safe=False
        )

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


@csrf_exempt
def get_list(req: django.http.HttpRequest):
    try:
        movie = Movie.objects.all()
        movie_list = []

        for movie in Movie:
            print(movie)
            item = {
                "title": movie.title,
                "release_date": movie.release_date,
                "poster": movie.poster,
                "director": movie.director,
                "description": movie.description,
            }
            movie_list.append(item)

        return django.http.JsonResponse(
            movie_list,
            status=200,
            safe=False
        )
    except Exception as err:
        print(err)
        return django.http.JsonResponse(
            {
                "message": "Movies not found",
            },
            status=404,
        )

# Optional Query. Sort: [release-date, rating, updated_on]
