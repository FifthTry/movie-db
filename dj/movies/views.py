import django.http

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

    # Request
    """
    get from request body
    title, release_date, poster, director, description, rating, review_count
    """

    """
    Create a row in Movie model
    """

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
