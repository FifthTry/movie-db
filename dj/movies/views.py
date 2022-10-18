import math

import django.http
from .models import Movie, Review
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


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
    # p_number = int(page_number)
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

    last_pno = math.ceil(total_movies/8)




    # order_by = req.GET.get("p_no", 1)
    # movies = Movie.objects.all()[(p_number - 1) * items + 1: p_number * items + 1]
    movies = Movie.objects.all()
    p = Paginator(Movie.objects.all().order_by("id"), items)

    movie_list = p.get_page(page_number)
    list_of_top_movies = []

    for movie in movie_list:
        rating = give_rating(movie.id)
        item = {
            "title": movie.title,
            "url": "http://127.0.0.1:8000/movie/?id=" + str(movie.id),
            "average": str(rating[0]),
            "total_reviews": str(rating[1]),
            "release_date": str(movie.release_date),
            "poster": {'light': movie.poster, 'dark': movie.poster},
            "director": movie.director,
            "description": movie.description,
        }
        list_of_top_movies.append(item)

    if movie_list.has_previous():
        previous_page_number = {movie_list.previous_page_number()}
        # previous_page_number = p_number - 1
    else:
        previous_page_number = 1

    if movie_list.has_next():
        next_page_number = {movie_list.next_page_number}
    else:
        next_page_number = {movie_list.paginator.num_pages}

    last_page_number = {movie_list.paginator.num_pages}


    return django.http.JsonResponse(
        {
            "p_no": movie_list.number,
            # TODO: Next And Previous both are optional
            # "next": "api/movies/?p_no="+str(page_number + 1)+"&items="+str(items),
            # "previous": "api/movies/?p_no="+str(previous_page_number)+"&items="+str(items),
            "next": f"api/movies/?p_no={next_page_number}&items={items}",
            "previous": f"api/movies/?p_no={previous_page_number}&items={items}",
            "first": f"api/movies/?p_no={1}&items={items}",
            "last": f"api/movies/?p_no={last_page_number}&items={items}",

            "movies": list_of_top_movies,

        },
        status=200,
        safe=False,
    )


@csrf_exempt
def search_movie(req: django.http.HttpRequest):
    # if req.method == "GET":
    #     return django.http.HttpResponse("Wrong Method GET", status=405)

    body = json.loads(req.body.decode("utf-8"))
    target_movie_id = None
    target_movie_name = body['movie']
    # print(f"you are searching for this movie (lowercase) -> {target_movie_name.lower()}")

    all_movies = Movie.objects.all()
    for movie in all_movies:
        # print(movie.title.lower())

        if movie.title.lower() == target_movie_name.lower():
            # print("Found matching movie")
            # print(movie.id)
            target_movie_id = movie.id
            break

    # print(f"Hello found movie id = {target_movie_id}")

    return django.http.JsonResponse({"data": {"url": "/movie/?id=" + str(target_movie_id)}}, status=200)



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
        # print("Movie details", movie)
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

    review = Review.objects.create(
        movie=movie,
        title=body["title"],
        description=body.get("description"),
        reviewer=body["reviewer"],
        rating=body["rating"],
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
    count_reviews= 0
    total = 0
    try:
        reviews = Review.objects.filter(movie__pk=id)
        for review in reviews:
            if review.rating <= 10 or review.rating >= 0:
                count_reviews += 1
                total += review.rating

        if count_reviews == 0:
            average_rating = 0
        else:
            average_rating = round(total/count_reviews, 2)

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
            if review.rating <= 10 or review.rating >= 0:
                count_reviews += 1
                total += review.rating

        if count_reviews == 0:
            average_rating = 0
        else:
            average_rating = round(total/count_reviews, 2)

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
        # print("Movie details", movie)
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
